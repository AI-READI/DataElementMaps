# Unit lookup

Scripts to fill `MEASUREMENT.unit_concept_id` from the AI-READI concept map (`../_ai_readi_redcap_value_set_mapping_common.csv`). Databricks / Spark SQL.

| File | What it does |
|---|---|
| `USAGE.md` | **Step-by-step usage** |
| `00_load_concept_map.sql` | Loads the mapping file as `concept_map` (only needed for option B; set the file path) |
| `unit_concept_lookup.csv` | **The ready-made lookup table** (114 rows): load it and skip building it |
| `unit_concept_lookup_extended.csv` | **Reference view** of the 89 field keys (v1.8.2): per measurement field, its measurement (target) concept (ID, name, vocabulary, code) and its unit concept (ID, name, unit text), with the concept map lines they come from. Not needed by the join; rebuilt with `build_unit_concept_lookup_extended.py` |
| `imported_field_concept_lookup.csv` | **Imported form, one row per field** (v1.8.6): the 65 mapped questions of the REDCap `imported` form (31 imported labs, MoCA, interview age, education), keyed by the REDCap field name (`field_id`), with the target concept (ID, name, domain, vocabulary, code), the `SRC_CODE` of the map (the LOINC code for the labs), the unit and the map line numbers. Join imported records on `field_id`; no need to edit `SRC_CODE` in the concept map. Rebuilt with `build_imported_field_concept_lookup.py` |
| `01a_load_unit_concept_lookup_csv.sql` | Option A: creates `unit_lookup` from `unit_concept_lookup.csv` |
| `01_create_unit_lookup.sql` | Option B: **one query** that builds `unit_lookup` from the concept map (same 114 rows) |
| `02_view_unit_lookup.sql` | Review `unit_lookup`: counts, field and unit-text lists, duplicate check |
| `03_left_join_unit_lookup_template.sql` | **The LEFT JOIN** to add to the ETL (replace the placeholders) |
| `04_example_omop_survey_measurement.sql` | The same join, ready to run on `omop_survey.measurement` |
| `05_check_no_fanout.sql` | Checks that the join adds no rows |
| `06_check_units_after_etl.sql` | Checks units in MEASUREMENT after the ETL re-run |
| `../ai_readi_redcap_value_set_mapping.metadata.json` | **Map version metadata** (v1.8.6): map version, repository release, row count and MD5 of each mapping file, and the values to record in OMOP (`cdm_source.source_description`, `metadata`). Written by `../../scripts/identify_map_version.py --write-metadata` |
| `09_validate_units_and_value_ranges.sql` | Read-only data review of the delivered OMOP survey data (v1.8.5): unit coverage and fan-out, unit concepts, unit text vs assigned unit, value distributions, value-range flags, waist/hip, refraction, dates and age, repeated entries, zeros by year and monthly drift. Baselines from the 2026-10-28 check are in the comments |
| `medication_route_lookup.csv`, `07_`, `07a_`, `08_` | Medication route lookup for `DRUG_EXPOSURE.route_concept_id` (see the end of this file) |

## Extended lookup (`unit_concept_lookup_extended.csv`)

One row per field key of `unit_concept_lookup.csv` (89 rows), for review and for joining units to measurement concepts. The target concept columns cover every measurement field with a unit: labs, CBC, vital signs, autorefractor and MoCA.

| Column | Meaning |
|---|---|
| `lookup_key` | Measurement field name (REDCap field ID), the same key as `unit_concept_lookup.csv` |
| `form_name` | REDCap form |
| `source_concept_name` | REDCap label (imported labs: the short label, e.g. `HbA1c`) |
| `target_concept_id`, `target_concept_name`, `target_vocabulary_id`, `target_concept_code` | Measurement concept of the field's question row (`measurement_concept_id`) |
| `unit_concept_id`, `unit_concept_name`, `unit_source_value` | Unit concept of the field's unit row (`unit_concept_id`) |
| `map_line_lab`, `map_line_unit` | Line numbers of those rows in the concept map |
| `note` | The LDL exception (unit field `import_ldl_cholesterol_u`) |

Rebuild after any change to the concept map: `python redCapDataDictionaryWithExtension/value-set-mapping-common/scripts/build_unit_concept_lookup_extended.py .` (from the repository root).

## Usage

```sql
SELECT m.*,
       COALESCE(f.unit_concept_id, u.unit_concept_id, 0)   AS unit_concept_id,
       COALESCE(f.unit_source_value, NULLIF(TRIM(m.<unit_text_column>), '')) AS unit_source_value
FROM <your_measurement_table> m
LEFT JOIN unit_lookup f
       ON f.key_type = 'field'  AND f.lookup_key = TRIM(m.<field_name_column>)
LEFT JOIN unit_lookup u
       ON u.key_type = 'string' AND u.lookup_key = TRIM(m.<unit_text_column>);
```

- `<field_name_column>`: the REDCap field name, e.g. `lbscat_rbc`. In `omop_survey.measurement` it is the text before the first comma of `measurement_source_value`.
- `<unit_text_column>`: the unit text on the record, if any, e.g. `mEq/L`. It can be NULL.
- The unit is taken by field name first, then by unit text, otherwise 0 (OMOP: no matching concept).
- `unit_lookup` has exactly one row per `key_type` + `lookup_key`, so the joins never add rows. Check: the row count before and after the join must be equal (`05_check_no_fanout.sql`).

## What is in unit_lookup

| key_type | lookup_key | Rows | Source in the concept map |
|---|---|---|---|
| `field` | measurement field name | 89 | Unit rows named `<field>_u`: the imported-lab unit fields (e.g. `import_potassium_u`) and the v1.4 fixed-unit rows for fields with no unit field (CBC, physical assessment, autorefractor, globulin, bilirubin, urine albumin/creatinine, MoCA scores and times; v1.6: the BUN/creatinine, A/G and waist/hip ratios; v1.7: `import_bun_creatinine_ratio`). The v1.7 NRBC unit row (`lbscat_nrbc_u`) has `Map_to_OMOP` = No since v1.8.1 (NRBC is not collected) and is not in the lookup. Plus `import_ldl_cholesterol_calculation`, whose unit field has a different name (`import_ldl_cholesterol_u`). |
| `string` | unit text | 25 | Generic Unit rows (blank `FIELD_ID`) plus `s`, `second`, `score` |

Notes:
- Matching is exact text. The micro sign in `x10E3/µL` and `x10E6/µL` is U+00B5.
- MoCA: score fields → 44777566 (score), time fields → 8555 (second).
- Do not join on all Unit rows of the concept map by `SRC_CODE`: the same text appears in several rows (e.g. `g/dL` in 6), which would multiply measurement rows. `unit_lookup` avoids this.

### key_type = 'field' (89 rows)

| lookup_key | unit_concept_id | unit_source_value |
|---|---|---|
| `bmi_vsorres` | 9531 | kg/m2 |
| `bp1_diabp_vsorres` | 8876 | mmHg |
| `bp1_sysbp_vsorres` | 8876 | mmHg |
| `bp2_diabp_vsorres` | 8876 | mmHg |
| `bp2_sysbp_vsorres` | 8876 | mmHg |
| `clock_visuospatial_executive` | 44777566 | score |
| `clock_visuospatial_executive_time` | 8555 | s |
| `cube_visuospatial_executive` | 44777566 | score |
| `cube_visuospatial_executive_time` | 8555 | s |
| `delayed_recall_with_no_clue` | 44777566 | score |
| `delayed_recall_with_no_clue_time` | 8555 | s |
| `digitspan` | 44777566 | score |
| `digitspan_time` | 8555 | s |
| `fluency_language` | 44777566 | score |
| `fluency_language_time` | 8555 | s |
| `height_vsorres` | 8582 | cm |
| `hip_vsorres` | 8582 | cm |
| `import_ag_ratio` | 8523 | ratio |
| `import_albumin` | 8713 | g/dL |
| `import_alkaline_phosphatase` | 8923 | IU/L |
| `import_alt_got` | 8923 | IU/L |
| `import_ast_got` | 8923 | IU/L |
| `import_bilirubin_total` | 8840 | mg/dL |
| `import_bun` | 8840 | mg/dL |
| `import_bun_creatinine_ratio` | 8523 | ratio |
| `import_buncreatinineratio` | 8523 | ratio |
| `import_c_peptide` | 8842 | ng/mL |
| `import_calcium` | 8840 | mg/dL |
| `import_carbon_dioxide_total` | 9557 | mEq/L |
| `import_chloride` | 9557 | mEq/L |
| `import_creatinine` | 8840 | mg/dL |
| `import_crp_hs` | 8751 | mg/L |
| `import_globulin_total_norc` | 8713 | g/dL |
| `import_glucose` | 8840 | mg/dL |
| `import_hba1c` | 8554 | % |
| `import_hdl_cholesterol` | 8840 | mg/dL |
| `import_insulin` | 8842 | ng/mL |
| `import_ldl_cholesterol` | 8840 | mg/dL |
| `import_ldl_cholesterol_calculation` | 8840 | mg/dL |
| `import_nt_probnp` | 8845 | pg/mL |
| `import_potassium` | 9557 | mEq/L |
| `import_protein_total` | 8713 | g/dL |
| `import_sodium` | 9557 | mEq/L |
| `import_total_cholesterol` | 8840 | mg/dL |
| `import_triglycerides` | 8840 | mg/dL |
| `import_troponin_t` | 8725 | ng/L |
| `import_uarc` | 8723 | mg/g |
| `import_urine_albumin` | 8840 | mg/dL |
| `import_urine_creatinine` | 8840 | mg/dL |
| `lbscat_a1c` | 8713 | g/dL |
| `lbscat_hct` | 8554 | % |
| `lbscat_mch` | 8564 | pg |
| `lbscat_mchc` | 8713 | g/dL |
| `lbscat_mcv` | 8583 | fL |
| `lbscat_plt` | 8848 | x10E3/µL |
| `lbscat_rbc` | 8815 | x10E6/µL |
| `lbscat_rdw` | 8554 | % |
| `lbscat_wbc` | 8848 | x10E3/µL |
| `lettera` | 44777566 | score |
| `lettera_time` | 8555 | s |
| `memory_trial1` | 44777566 | score |
| `memory_trial1_time` | 8555 | s |
| `memory_trial2` | 44777566 | score |
| `memory_trial2_time` | 8555 | s |
| `moca_abstraction` | 44777566 | score |
| `moca_abstraction_time` | 8555 | s |
| `moca_combined_mis_score` | 44777566 | score |
| `moca_orientation` | 44777566 | score |
| `moca_orientation_time` | 8555 | s |
| `moca_total_score` | 44777566 | score |
| `naming` | 44777566 | score |
| `naming_time` | 8555 | s |
| `pulse_vsorres` | 8541 | bpm |
| `pulse_vsorres_2` | 8541 | bpm |
| `repetition` | 44777566 | score |
| `repetition_time` | 8555 | s |
| `subtraction` | 44777566 | score |
| `subtraction_time` | 8555 | s |
| `trails_visuospatial_executive` | 44777566 | score |
| `trails_visuospatial_executive_time` | 8555 | s |
| `viaodaxi` | 9484 | degree |
| `viaodcyl` | 9291 | diopter |
| `viaodsph` | 9291 | diopter |
| `viaosaxi` | 9484 | degree |
| `viaoscyl` | 9291 | diopter |
| `viaossph` | 9291 | diopter |
| `waist_vsorres` | 8582 | cm |
| `weight_vsorres` | 9529 | kilograms |
| `whr_vsorres` | 8523 | ratio |

### key_type = 'string' (25 rows)

| lookup_key | unit_concept_id |
|---|---|
| `%` | 8554 |
| `IU/L` | 8923 |
| `bpm` | 8541 |
| `cm` | 8582 |
| `degree` | 9484 |
| `diopter` | 9291 |
| `fL` | 8583 |
| `g/dL` | 8713 |
| `kg` | 9529 |
| `kg/m2` | 9531 |
| `kilograms` | 9529 |
| `mEq/L` | 9557 |
| `mg/L` | 8751 |
| `mg/dL` | 8840 |
| `mg/g` | 8723 |
| `mmHg` | 8876 |
| `ng/L` | 8725 |
| `ng/mL` | 8842 |
| `pg` | 8564 |
| `pg/mL` | 8845 |
| `s` | 8555 |
| `score` | 44777566 |
| `second` | 8555 |
| `x10E3/µL` | 8848 |
| `x10E6/µL` | 8815 |

## Example result (04, sample rows)

| measurement_source_value (field) | unit text on record | unit_concept_id | unit_source_value |
|---|---|---|---|
| lbscat_rbc | (none) | 8815 | x10E6/µL |
| import_globulin_total_norc | N/A | 8713 | g/dL |
| import_potassium | mEq/L | 9557 | mEq/L |
| import_potassium | (none) | 9557 | mEq/L |
| import_ldl_cholesterol_calculation | mg/dL | 8840 | mg/dL |
| height_vsorres | (none) | 8582 | cm |
| other field | x10E3/µL | 8848 | x10E3/µL |
| naming (MoCA score) | (none) | 44777566 | score |
| naming_time (MoCA time) | (none) | 8555 | s |

Rows in: 9. Rows out: 9.

# Medication route lookup

Fills `DRUG_EXPOSURE.route_concept_id` from the medication route question `cmroute` ("How is it taken?"). This is a **protected** field, so it applies to the protected / controlled-access release.

| File | What it does |
|---|---|
| `medication_route_lookup.csv` | **The ready-made lookup table** (26 rows): load it and skip building it |
| `07a_load_medication_route_lookup_csv.sql` | Option A: creates `medication_route_lookup` from the CSV |
| `07_create_medication_route_lookup.sql` | Option B: **one query** that builds the same table from the concept map |
| `08_left_join_medication_route_template.sql` | **The LEFT JOIN** for the drug exposure ETL (replace the placeholders) |

`medication_route_lookup` has one row per `key_type` + `lookup_key`:
- `key_type = 'code'`: the REDCap answer code (13 rows).
- `key_type = 'string'`: the answer label, e.g. `Oral` (13 rows). The join compares labels case-insensitively.

| Answer code | Label | route_concept_id | Concept (SNOMED Route) |
|---|---|---|---|
| `1` | Intralesional | **4157758** | Intralesional |
| `2` | Intramuscular | **4302612** | Intramuscular |
| `3` | Intraocular | **4157760** | Intraocular |
| `4` | Intraperitoneal | **4243022** | Intraperitoneal |
| `5` | Nasal | **4262914** | Nasal |
| `6` | Oral | **4132161** | Oral |
| `7` | Rectal | **4290759** | Rectal |
| `8` | Inhalation | **40486069** | Respiratory tract |
| `9` | Subcutaneous | **4142048** | Subcutaneous |
| `10` | Topical | **4263689** | Topical |
| `11` | Transdermal | **4262099** | Transdermal |
| `12` | Vaginal | **4057765** | Vaginal |
| `888` | Other | **0** | no matching concept |

Usage:
```sql
SELECT d.*,
       COALESCE(c.route_concept_id, s.route_concept_id, 0)         AS route_concept_id,
       COALESCE(c.route_source_value, s.route_source_value,
                d.<cmroute_label_column>)                          AS route_source_value
FROM <your_drug_exposure_table> d
LEFT JOIN medication_route_lookup c
       ON c.key_type = 'code'   AND c.lookup_key = TRIM(CAST(d.<cmroute_code_column> AS STRING))
LEFT JOIN medication_route_lookup s
       ON s.key_type = 'string' AND LOWER(s.lookup_key) = LOWER(TRIM(d.<cmroute_label_column>));
```

Route by answer code first, then by label, otherwise 0. Example: code `6` → 4132161 (Oral); label `Inhalation` → 40486069 (Respiratory tract); code `888` (Other) → 0. 6 rows in, 6 rows out.
