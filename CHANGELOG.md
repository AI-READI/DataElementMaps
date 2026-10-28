# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Where to find the mapping files

- **Working version (use for ETL):** `redCapDataDictionaryWithExtension/value-set-mapping-common/_ai_readi_redcap_value_set_mapping_common.csv`. This file is actively maintained and may change after each release.
- **Frozen release version:** `manuscript-tvst2026/ai_readi_redcap_value_set_mapping_common.csv` (with frozen SSSOM and LinkML copies), matching release `v1.0-tvst` and the TVST 2026 manuscript.

## [Unreleased]

## [v1.8.4] - 2026-10-28

Custom concepts with a standard equivalent move to the standard concept, and one missing answer is added. The candidates came from the vocabulary review of v1.8.3 against `omop_vocab` (`validate_concept_map_vocab.sql` V8 and a name search ignoring case and punctuation); each target's class, standard status and validity were confirmed in `omop_vocab`. Seven rows are edited in place and one is appended (line 2144), so every existing line number is the same as in v1.8.3. The ETL must apply these changes (OBSERVATION and CONDITION_OCCURRENCE concepts).

### Changed — custom → standard

| Line | Row | v1.8.3 | v1.8.4 |
|---|---|---|---|
| 929 | `pxne16` question "The crime rate in my neighborhood makes it unsafe to go on walks during the day…" | 2005200121 (custom) | **40192414** (PPI `ips_16`, Question, standard; same wording), exactMatch 1 |
| 957, 964 | `pxne4`, `pxne5` answer 88 "Does not apply to my neighborhood" | 2005200268 (custom) | **40192520** (PPI `SDOH_9`, Answer, standard; same wording), exactMatch 1 |
| 1869 | `mh_a1c` "Yes" (Condition) "Elevated A1C levels (elevated blood sugars)" | 2005200547 (custom) | **4214376** *Hyperglycemia* (SNOMED 80394007, Condition, standard), closeMatch 0.75 |
| 1849 | `mh_a1c` question `MODIFIER` | 2005200547 | 4214376 (follows line 1869, as for the v1.5 health-history conditions) |

- `TARGET_DOMAIN_ID` of the two answer rows stays *Meas Value*: the answer is written as `value_as_concept_id` of the OBSERVATION. The vocabulary domain of 40192520 is Observation (PPI answers), so `validate_concept_map_vocab.sql` V2 lists these two rows as a deliberate domain override.
- `mh_a1c` "Yes" now writes a standard CONDITION_OCCURRENCE (hyperglycemia) that OHDSI cohorts can find. closeMatch 0.75: the answer reports elevated A1C (blood sugar), which `mhterm_predm` and `mhterm_dm2` complement as separate items.
- The custom concepts 2005200121, 2005200268 and 2005200547 are no longer referenced by the map but are kept in `concept_manual.csv` (IDs are never reused).
- Reviewed and not changed: the other `pxne*` items (PPI `ips_1`–`ips_7` are non-standard and map to the PhenX LOINC questions the map already uses; `pxne8`–`pxne15` and `pxne17` have no PPI question); the insurance block `pxhic1`–`pxhic7` (All of Us models insurance as one non-standard question, `basics_11a`, with the insurance types as answers, so `cope_a_193` *Medicare* is an Answer, not a question concept); `viaomthd` *EVA* (the same-name standard concept 42066053 is a Geography place); `pxhic*` *Covered* (SNOMED 255334000 is a general qualifier, not insurance coverage); `mhoccur_circ`, `mhoccur_cvdot` (compound answers; only very broad standard parents exist).

### Added

- `eos_dsvst` answer 3 "Devices Returned" (line 2144) → **2005200589** *Device returned* (existing AI-READI custom concept, as used for `dcvgmenyn` and `dvenvenyn`), exactMatch 1, in the format of line 267. Stages 0–2 were mapped and stage 3 was not; the current data has 3 records with stage 3.

### Changed — metadata

- `SRC_CODE` filled for the two imported ratio questions that had it blank: line 554 `import_buncreatinineratio` → 31045-8, line 584 `import_ag_ratio` → 1759-0 (the LOINC code, as for the other imported labs). The ETL and the unit lookup match on `FIELD_ID`, so this changes nothing in the data.

### Added — release check script

- `redCapDataDictionaryWithExtension/scripts/validate_concept_map_against_data.sql` (read-only, Databricks): checks the map against the OMOP survey data and the vocabulary, alongside `validate_concept_map_vocab.sql`. Row count; targets non-standard, invalid or missing in `omop_vocab`; answer and question fan-out (one value row per REDCap answer); the v1.8.x changes in place; data fields with no map row; answer codes in the data with no map row; unit coverage, no fan-out and Unit-domain units; question rows pointing at Answer-class concepts and the reverse. Each check states its expected result.

### Changed — master REDCap data dictionary

- Eight master rows take the new values (`Origin` = Changed, `Date_of_Variable_Modification` 10/28/2026), including the existing `eos_dsvst` 3 row (now `Map_to_OMOP` = Yes). 3,150 rows; every concept map row has a master row with the same values.

### Regenerated

- map2omop (2,113 rows) and open-source public (1,998) versions, SSSOM (2,068 rows; 75 incomplete) and LinkML (2,143 records). `unit_concept_lookup.csv` and `unit_concept_lookup_extended.csv` unchanged.
- Counts: standard 1,519 (403 concepts); custom 486 (339); mapped 2,005 (69.0%, 742); designated but unmapped 138; not designated 763. SNOMED 172/75; PPI 8/7. Standard predicates: exact 1,258; close 259 (170 at 1, 89 at 0.75); related 2. Audit A7 (custom Condition targets) 3 → 2. `count_concept_map.sql` expected values and `validate_concept_map_vocab.sql` V0 (2,143) updated.

## [v1.8.3] - 2026-10-27

Two lab unit rows are corrected to the units the data is reported in. A check of the delivered OMOP survey data against the v1.8.2 unit lookup found that the unit text in the data and the value ranges disagree with the map for C-peptide and urine albumin; the field key (which the join applies first) would have labeled C-peptide 1,000× and urine albumin 10× off. Two rows are edited in place, so every line number is the same as in v1.8.2. The ETL must apply this change (`MEASUREMENT.unit_concept_id`).

### Fixed — unit rows

| Line | Unit row | v1.8.2 | v1.8.3 | Evidence (current OMOP data) |
|---|---|---|---|---|
| 514 | `import_c_peptide_u` | 8725 *nanogram per liter* (`ng/L`) | **8842** *nanogram per milliliter* (`ng/mL`) | unit text `ng/mL`; 3,981 values, median 2.64 (p05 0.86, p95 7.39): ng/mL range (ng/L would be about 1,000× higher) |
| 613 | `import_urine_albumin_u` | 8751 *milligram per liter* (`mg/L`) | **8840** *milligram per deciliter* (`mg/dL`) | unit text `mg/dL`; 3,984 values, median 0.54 (p95 9.6) |

- `SRC_CODE`, `SRC_CD_DESCRIPTION`, `TARGET_CONCEPT_NAME` and `TARGET_CONCEPT_CODE` follow the new unit. The other imported lab units were checked against the data's unit text and agree (e.g. insulin `ng/mL`, median 0.60; urine creatinine `mg/dL`, median 66.8; troponin T `ng/L`; NT-proBNP `pg/mL`; CRP-HS `mg/L`).
- `unit_concept_lookup.csv`: field keys `import_c_peptide` → 8842 `ng/mL` and `import_urine_albumin` → 8840 `mg/dL` (still 114 rows; `01_create_unit_lookup.sql` gives the same result). The unit-text keys `ng/L` and `mg/L` are unchanged (generic rows). `unit_concept_lookup_extended.csv` rebuilt; scripts README updated.
- Not changed: the vision and monofilament measurements (BCVA, MARS contrast sensitivity, monofilament; 26 fields) have no unit rows: logMAR and log contrast sensitivity are dimensionless, the others are letter counts or scores; `unit_concept_id` stays 0.

### Changed — master REDCap data dictionary

- The two unit rows (master records 2844 and 2939) take the new values; `Origin` = Changed, `Date_of_Variable_Modification` 10/27/2026. 3,150 rows; every concept map row has a master row with the same values.

### Regenerated

- map2omop (2,112 rows) and open-source public (1,997) versions, SSSOM (2,067 rows; 75 incomplete) and LinkML (2,142 records). Counts unchanged from v1.8.2 (UCUM 132/40: 8725 and 8751 are still used by troponin T and CRP-HS).

## [v1.8.2] - 2026-10-27

The new BUN/creatinine field holds BUN ÷ creatinine, so it moves to the BUN/creatinine LOINC code. The data team confirmed the values (for example BUN 15 mg/dL, creatinine 0.77 mg/dL → ratio 19.5; BUN 37, creatinine 1.01 → 36.6). One row is edited in place, so every line number is the same as in v1.8.1. The ETL must apply this change: the field's MEASUREMENT concept changes. Also added: an extended unit lookup that pairs each measurement field's concept with its unit concept.

### Changed — target concept

| Line | Field | v1.8.1 | v1.8.2 |
|---|---|---|---|
| 2125 | `import_bun_creatinine_ratio` | 3033837 *Creatinine/Urea nitrogen [Mass Ratio] in Serum or Plasma* (LOINC 31045-8) | **3018311** *Urea nitrogen/Creatinine [Mass Ratio] in Serum or Plasma* (LOINC 3097-3), exactMatch 1 |

- `SRC_CODE` 31045-8 → 3097-3 (the LOINC code, as for the other imported labs); `SRC_CODE_ID` and `SRC_CD_DESCRIPTION` "Creatinine/BUN ratio" → "BUN/Creatinine ratio".
- Unit row `import_bun_creatinine_ratio_u` (line 2126, 8523 *ratio*) unchanged; `unit_concept_lookup.csv` unchanged (114 rows).
- Not changed: line 554, `import_buncreatinineratio` (the original field), stays 3033837 *Creatinine/Urea nitrogen*: its stored values are creatinine ÷ BUN (all 3,981 current values; median 0.053). Its `MODIFIER` still says to remap it to 3018311 if that field's formula and values are corrected.
- This replaces the v1.7 decision that both fields map to creatinine ÷ BUN.

### Added — extended unit lookup

- `value-set-mapping-common/scripts/unit_concept_lookup_extended.csv` (89 rows): one row per field key of `unit_concept_lookup.csv`, with the field's measurement concept (`lab_concept_id`, name, vocabulary, code, from its question row) and unit concept (`unit_concept_id`, name, unit text, from its unit row), the REDCap form and label, and the concept map line numbers. Reference only: the ETL join still uses `unit_concept_lookup.csv`. `import_ldl_cholesterol` (key from the unit field `import_ldl_cholesterol_u`) carries the LDL calculation concept, with a note.
- `build_unit_concept_lookup_extended.py`: rebuilds it from the concept map and `unit_concept_lookup.csv` (checks that every unit matches the lookup and every concept is in the Measurement domain). Scripts README: file list and column definitions.

### Changed — master REDCap data dictionary

- The `import_bun_creatinine_ratio` row takes the new values; `Origin` = Changed, `Date_of_Variable_Modification` 10/27/2026. 3,150 rows; every concept map row has a master row with the same values.

### Regenerated

- map2omop (2,112 rows) and open-source public (1,997) versions, SSSOM (2,067 rows; 75 incomplete) and LinkML (2,142 records) from the v1.8.2 common file.
- Counts: standard 1,515 (400 concepts, +1: 3018311 is new and 3033837 is still used by line 554); custom 489 (342); mapped 2,004 (69.0%, 742 concepts); designated but unmapped 138; not designated 764. LOINC 1,190/277. `count_concept_map.sql` expected values updated to v1.8.2; `validate_concept_map_vocab.sql` V0 comment (2,142 rows).

## [v1.8.1] - 2026-10-26

NRBC is switched off: it is not collected. The data team confirmed that the Labcorp *CBC, Platelet, No Differential* reports returned to AI-READI do not include NRBC, and that no REDCap field will be added ("We do not collect data for NRBC. This value is not provided in the reports returned to us from LabCorp."). A redacted Labcorp report (UAB) lists exactly 9 results: WBC, RBC, hemoglobin, hematocrit, MCV, MCH, MCHC, RDW and platelets. Two rows are edited in place, so every line number is the same as in v1.8. No concept changes; the ETL is not affected (the field matches no data).

### Changed — Map_to_OMOP

- `lbscat_nrbc` (line 2127, → 40761514) and its unit row `lbscat_nrbc_u` (line 2128, → 8554): `Map_to_OMOP` Yes → No and `transferred_to_fairhub_REDCap_dataset` Yes → No, so the transferred rows match the fields FAIRhub receives. The rows are kept (as for the superseded MoCA unit rows); the v1.7 note under *Added — NRBC* is superseded.

### Reviewed and not changed — CBC LOINC codes

The 9 CBC fields on the report map to the Labcorp test 028142 LOINC codes (v1.7), all standard Measurement concepts confirmed in `omop_vocab`, exactMatch 1; the report units match the unit rows (lines 2032–2040; the report writes "uL" for "µL").

| Line | Field | LOINC | Concept |
|---|---|---|---|
| 672 | `lbscat_wbc` WBC (x10E3/µL) | 6690-2 | 3000905 *Leukocytes [#/volume] in Blood by Automated count* |
| 673 | `lbscat_rbc` RBC (x10E6/µL) | 789-8 | 3020416 *Erythrocytes [#/volume] in Blood by Automated count* |
| 674 | `lbscat_a1c` Hemoglobin (g/dL) | 718-7 | 3000963 *Hemoglobin [Mass/volume] in Blood* |
| 675 | `lbscat_hct` Hematocrit (%) | 4544-3 | 3023314 *Hematocrit [Volume Fraction] of Blood by Automated count* |
| 676 | `lbscat_mcv` MCV (fL) | 787-2 | 3023599 *MCV [Entitic mean volume] in Red Blood Cells by Automated count* |
| 677 | `lbscat_mch` MCH (pg) | 785-6 | 3012030 *MCH [Entitic mass] by Automated count* |
| 678 | `lbscat_mchc` MCHC (g/dL) | 786-4 | 3009744 *MCHC [Entitic Mass/volume] in Red Blood Cells by Automated count* |
| 679 | `lbscat_rdw` RDW (%) | 788-0 | 3019897 *Erythrocyte [DistWidth] in Red Blood Cells by Automated count* |
| 680 | `lbscat_plt` Platelets (x10E3/µL) | 777-3 | 3024929 *Platelets [#/volume] in Blood by Automated count* |

### Changed — scripts

- `unit_concept_lookup.csv`: 114 rows (field 89, string 25); `lbscat_nrbc` removed.
- `01_create_unit_lookup.sql`: uses only `Map_to_OMOP` = Yes rows, so a switched-off unit row never enters the lookup (the result equals the CSV). Row counts updated in `01a_`, `02_`, the scripts' README and USAGE.
- `count_concept_map.sql`: the two NRBC rows are reported as designated-but-unmapped, "Not collected (NRBC)"; expected values updated to v1.8.1. `validate_concept_map_vocab.sql`: V0 comment (2,142 rows, unchanged).

### Changed — master REDCap data dictionary

- The two NRBC rows (master records 3138–3139) take the new values; `Origin` = Changed, `Date_of_Variable_Modification` 10/26/2026. Every concept map row still has a master row with the same values; 3,150 rows.

### Regenerated

- map2omop (2,112 rows) and open-source public (1,997) versions, SSSOM (2,067 rows; 75 incomplete) and LinkML (2,142 records) from the v1.8.1 common file.
- Counts: standard 1,515 (399 concepts); custom 489 (342); mapped 2,004 (69.0%, 741 concepts); designated but unmapped 138 (+2 "Not collected (NRBC)"); not designated 764. LOINC 1,190/276; UCUM 132/40. Standard predicates: exact 1,255; close 258 (170 at 1, 88 at 0.75); related 2.

## [v1.8] - 2026-10-25

Corrections from the review of the concept map against the REDCap codebook (2026-10-25), checked against the delivered OMOP survey data, an ECG procedure row, four protected fields that had no row, and the master REDCap data dictionary brought in line with the concept map. 15 rows are appended at the end of the file (lines 2129–2143) and the other changes are in place, so every existing line number is the same as in v1.7. Concept IDs and names were confirmed in `omop_vocab`.

### Fixed — Capsule dose unit (line 1692)

- `cmdosu` 2 *Capsule* had no concept (0, with the `MODIFIER` note "No matching unit concept"). UCUM has no capsule unit (Tablet has `{tbl}` 9431), but SNOMED 428641000 *Capsule - unit of product usage* (4176621, non-standard) **Maps to** **32912** *Generic unit for indivisible thing* (UCUM `1`, standard, Unit). Line 1692 → 32912, closeMatch 0.75 (the target is a count of items and does not say capsule); `MODIFIER` cleared. Capsule is a dose form, not a route: the route is `cmroute` (6 *Oral* → 4132161, `route_concept_id`), and the product form comes with the RxNorm drug (`cmtrt`).

### Fixed — answer codes

| Lines | Field | v1.7 | v1.8 | Evidence |
|---|---|---|---|---|
| 133–135, 137–140 | `dvamwenhand`, `dvamwendhand` | `SRC_CODE` held the code ID (`dvamwenhand_1` …), so no answer matched | `SRC_CODE` 1–4, `SRC_CODE_ID` `<field>_<code>` | REDCap choices 1–4; all 7,905 data rows have `value_as_concept_id` 0 |
| 1993 | `sumrjfr` *Prefer not to say* | 999 | **777** (`sumrjfr_777`) | REDCap choice 777; 70 data rows use 777 |
| 1974 | `rp_childpot` *Yes* | `rp_childpot_yes` | **1** (`rp_childpot_1`), `FIELD_TYPE` yesno | REDCap yesno codes 1/0 |

### Changed — Map_to_OMOP

- Answer 0 *No* of `susmkstoage`, `sualcage` and `suvptoyr` (lines 1994–1996): `Map_to_OMOP` Yes → No. 0 is not a REDCap choice for these questions and does not occur in the data. The rows are kept; the counts report them with "Answer to an excluded question".

### Added

- `cmdosu` (medication dose unit) choices with no row: 19 → 8723 *milligram per gram* (`mg/g`, line 2129) and 20 → 8861 *milligram per milliliter* (`mg/mL`, line 2130), in the format of line 1708.
- Yes (45877994) and No (45878245) answer rows for yes/no questions that had none: `dvamwenyn`, `dcvgmenyn`, `dvenvenyn` (device return) and `eos_ds` (lines 2131–2138), in the format of lines 871–872; `Map_to_OMOP`, transferred, protected and form copied from each question row.

### Added — ECG performed → PROCEDURE_OCCURRENCE

- The ECG form has no yes/no question: the EKG is performed when `rtekgcmpdattim` *Date & time Cardiology - EKG - Pagewriter TC30 Cardiograp performed* is filled in. Until v1.7 that field wrote only an OBSERVATION (line 286, 4160030 *Performed*), so a standard query for an ECG found no AI-READI participants.
- A second Question row for `rtekgcmpdattim` (line 2139, new) maps to **4145308** *12 lead ECG* (SNOMED 268400002, Procedure, standard), exactMatch 1: the PageWriter TC30 is a 12-lead electrocardiograph. Line 286 is unchanged. No qualifier (there is no laterality). Not used: 4163951 *Electrocardiographic procedure* (SNOMED 29303009, more general) and the CPT4 billing codes 93005 / 93000 (2313815 / 2313814); 4065277 *Standard ECG* (164847006) is not standard.
- ETL rule (as v1.7 rules 1–4): when `rtekgcmpdattim` has a value, write one PROCEDURE_OCCURRENCE with `procedure_concept_id` 4145308, `procedure_datetime` (and `procedure_date`) = the value of `rtekgcmpdattim`, `procedure_source_value` `rtekgcmpdattim`, `procedure_source_concept_id` 2005200602 (the custom device concept on line 286). This is the first question with two rows on one key (A5 rises from 78 to 79).
- ECG and EKG are the same test; REDCap names the form `ecg` and the fields `rtekg…`, and the map keeps REDCap's names.

### Added — protected fields missing from the map

Protected rows are mapped like any other row (`Map_to_OMOP` = Yes) and flagged `protected`. The flag decides the release, not the mapping: map2omop (all `Map_to_OMOP` = Yes rows, 2,114) includes them; the open-source public version (1,999) leaves them out. The delivered OMOP survey data is a public build (DRUG_EXPOSURE is empty), so protected rows appear only in a controlled-access build run on map2omop. Four protected fields on the codebook had no row (lines 2140–2143, new; all protected, `Map_to_OMOP` = Yes):

| Line | Field | Target | Note |
|---|---|---|---|
| 2140 | `cmcmpdat2` *Date current medication collected* | 4260905 *Date* (SNOMED), qualifier 2005200594 *Current medication collected* | As `cmcmpdat` (line 681); values from the master row |
| 2141 | `cmrouteot` medication route *If Other, please specify* | 2005200485 *Specify other* (AIREADI), exactMatch 1 | As `odristate` (line 1979); the master had it with `Map_to_OMOP` = No |
| 2142 | `mhoccur_ot` health history *If yes, please specify* | 2005200485 *Specify other* | Same |
| 2143 | `rp_childpot` answer 0 *No* | **42530854** *Not pregnant* (LOINC LA26683-5), exactMatch 1 | Pairs with line 1974 (1 → 45884583 *Currently pregnant*) |

Checked and left at 0 (no concept): `cmdosu` 18 *Other*; `cmroute` question and 888 *Other* (OMOP has no "other" route); `ethnicscore` (REDCap calculation). `dristate` (state codes) and `cmtrt` (RxNorm code from the BioPortal autocomplete) have no answer rows by design.

### Changed — metadata

- Row type (`temp_Question_or_Answer`) blank → **Unit** on the 45 unit rows that had none: the old MoCA unit rows (648–667), the generic unit-text rows `s`, `second`, `score` (668–670) and the generic unit-text rows `pg/mL` … `kg` (1997–2018). `TARGET_DOMAIN_ID` was already Unit on all 153 unit rows. No row in the map now has a blank row type. Metadata only: the unit lookup selects on `TARGET_DOMAIN_ID` and is unchanged (115 keys: field 90, string 25).
- `SRC_CD_DESCRIPTION`: line 361 (`mhcat_adot`) *Yes* → *Alzheimer's disease*; line 1957 (`sulqdosfr` 36) *36 or more* → *More than 36* (REDCap labels).
- `FIELD_TYPE` `yes` / `no` → `yesno` (REDCap field type) on 10 rows (lines 1861–1867, 1869, 1870, 1878), and on line 1974 above. The LinkML `FIELD_TYPE` enum loses `yes` and `no`.

### Changed — master REDCap data dictionary

`redcap-data-dictionary/_master_red_cap_data_dictionary_with_extensions.csv` (last updated 2025-09-22) had fallen behind the concept map. It is now in sync: every concept map row has a master row with the same values in the 26 shared columns.

- **Changed (300 rows):** master rows that match a concept map row (on `FIELD_ID` + `SRC_CODE` + row type; for imported labs, on the field name or REDCap field number) take the map's values; `Origin` = Changed. The imported lab and unit rows (form `import_data`, row type Question) take the map's form (`imported`), row type (Question / Unit), LOINC `SRC_CODE` and concepts; four imported fields renamed since the master was written take the map's name (`import_ldl_cholesterol` → `import_ldl_cholesterol_calculation`, `import_ldl_cholesterol_max\` → `import_ldl_cholesterol_max`, `import_globulin_total` → `import_globulin_total_norc`, `import_a_g_ratio` → `import_ag_ratio`, same field numbers 2945, 2947, 2989, 2990). The imaging date fields (`rt*cmpdattim`) take form `ecg`; `cmrouteot` and `mhoccur_ot` take `Map_to_OMOP` = Yes.
- **Added (212 rows):** concept map rows with no master row, appended at the end with `Origin` = Added: MoCA (lines 615–670), the v1.4–v1.8 unit rows, the retinal imaging procedure rows, BUN/creatinine, NRBC and the v1.8 rows above (including the ECG procedure row), and a few older rows (e.g. `pdrx9` answers, `pxdhc_sum`, `import_uarc`).
- **Date_of_Variable_Modification:** the date of the concept map release in which that line last changed (Changed) or first appeared (Added): v1.0-tvst 10/14/2026, v1.1–v1.2.1 10/16/2026, v1.3 10/17/2026, v1.3.1 10/18/2026, v1.4–v1.5 10/19/2026, v1.6 10/22/2026, v1.7 10/24/2026, v1.8 10/25/2026.
- **Unchanged:** the other 2,638 master rows, byte for byte, including rows that are not in the concept map (REDCap history, `Map_to_OMOP` = No fields such as the `procedures` "not done" checkboxes, and Deleted rows). `NOTES` and `Choices_Calculations_OR_Slider_Labels` are kept on changed rows and blank on added rows. The master grows from 2,938 to 3,150 rows.

### Changed — scripts

- `count_concept_map.sql`: expected values updated to v1.8; the v1.7 entry below that reads "exact 1,267" should read "exact 1,247".
- `validate_concept_map_vocab.sql`: V0 row count 2,142; V10 (Procedure rows) also covers the ECG row.

### Regenerated

- map2omop (2,114 rows) and open-source public (1,999) versions, SSSOM (2,067 rows; 75 incomplete) and LinkML (2,142 records) from the v1.8 common file. `unit_concept_lookup.csv` and `medication_route_lookup.csv` unchanged.
- Counts: standard 1,517 (400 concepts); custom 489 (342); mapped 2,006 (69.0%, 742 concepts); designated but unmapped 136; not designated 764. Standard predicates: exact 1,257; close 258 (170 at 1, 88 at 0.75); related 2.

### Not yet included

- Monofilament redesign: deferred.
- Form name of the device imaging date rows (lines 279–285, form `ecg`): the fields are not on the current codebook; metadata only, the ETL does not use the form name.

## [v1.7] - 2026-10-24

Retinal imaging scans are recorded as procedures, the new BUN/creatinine ratio field is mapped, and the CBC results move to the lab's "by Automated count" LOINC codes. 48 rows are appended at the end of the file (lines 2081–2128), 6 rows are edited in place (lines 675–680), and 20 superseded MoCA unit rows are switched off (lines 648–667), so every existing line number is the same as in v1.6. The new rows write PROCEDURE_OCCURRENCE and MEASUREMENT, so the ETL must be re-run, with the ETL rules below. Concept IDs, names and domains were confirmed in the deployed OMOP vocabulary (Databricks `omop_vocab`).

### Added — retinal imaging procedures

- Form `retinal_imaging_v2` asks one yes/no question per scan type and eye (22 scan types × 2 eyes; questions on lines 1679–1741, answers on lines 1743–1846). Until v1.6 a completed scan was recorded only as an OBSERVATION (custom scan concept, value *Yes*), so a standard query for fundus photography or OCT found no AI-READI participants.
- For each of the 44 questions, a second "Yes" answer row (same `FIELD_ID`, `SRC_CODE` 1 and `SRC_CODE_ID` as the existing Yes row) maps to a standard procedure concept, domain Procedure. This follows the health-history pattern, where a "Yes" has a Yes value row and a Condition row (for example `mhoccur_mi`, lines 440 and 328). Right eye on lines 2081–2102 and left eye on lines 2103–2124, both in form order.

| Scans (per eye) | Concept | Predicate |
|---|---|---|
| OptoMed disc and macula CFP; Eidon central, nasal, temporal CFP and mosaic (6) | 4063911 *Ocular fundus photography* (SNOMED 20067007) | exactMatch 1 |
| Eidon IR, Eidon FAF, FLIO (3) | 4063911 | closeMatch 0.75 (no infrared, autofluorescence or FLIO procedure concept exists) |
| Spectralis posterior pole, Cirrus macula cube, Maestro2 3D wide and 3D macula, Triton 3D (5) | 1073298 *Optical coherence tomography of posterior segment of eye* (SNOMED 1303746000) | exactMatch 1 |
| Spectralis ONH, Cirrus disc cube (2) | 1073298 | closeMatch 1 (optic nerve head scans) |
| Spectralis, Cirrus, Maestro2 and Triton macula OCTA (5) | 745759 *Computerized ophthalmic diagnostic imaging … retina, including OCT angiography* (CPT4 92137) | closeMatch 1 (no SNOMED OCT angiography concept) |
| Cirrus disc 6x6 OCTA (1) | 745759 | closeMatch 0.75 (the code says "retina") |

- Laterality as a CPT4 modifier, the class OMOP intends for `PROCEDURE_OCCURRENCE.modifier_concept_id`: right-eye rows `qualifier_concept_id` 45888271 (RT), `qualifier_source_value` "Right eye", `MODIFIER` "right eye|45888271"; left-eye rows 45888270 (LT), "Left eye", "left eye|45888270". The existing imaging question and Yes rows keep the LOINC answers 45876703 *Right eye* / 45883829 *Left eye*.
- Not used: Measurement-domain concepts such as 4189584 *Confocal scanning laser ophthalmoscopy* and 45763633 *Optical coherence tomography of retina* (they would write MEASUREMENT), and Device-domain OCT scanner concepts. No new custom concepts.

### Added — BUN/creatinine ratio, new REDCap field

- `import_bun_creatinine_ratio` "Creatinine/BUN ratio" (line 2125, new) → **3033837** *Creatinine/Urea nitrogen [Mass Ratio] in Serum or Plasma* (LOINC 31045-8, Lab Test), exactMatch 1; `SRC_CODE` 31045-8, as for the other imported labs. This is the field the data team named for the ratio; it maps to what is stored now (creatinine ÷ BUN).
- Fixed-unit row `import_bun_creatinine_ratio_u` (line 2126) → 8523 *ratio* (UCUM `{ratio}`), same format as line 2080; `unit_concept_lookup.csv` (and `01_create_unit_lookup.sql`) gains `import_bun_creatinine_ratio` (with NRBC below: 115 rows, up from 113).
- Line 554 (`import_buncreatinineratio`) is unchanged from v1.6: 3033837, with the `MODIFIER` note that the stored value is creatinine ÷ BUN. Both fields therefore map to creatinine ÷ BUN (all 3,981 current values; median 0.053). 3018311 *Urea nitrogen/Creatinine [Mass Ratio]* (LOINC 3097-3) is not used; if a field is later recalculated as BUN ÷ creatinine (median about 18), remap that field to 3018311.

### Changed — CBC method codes (lines 675–680)

The performing lab's LOINC map (Labcorp test 028142 *CBC, Platelet, No Differential*) reports these results with the "by Automated count" codes; WBC (6690-2), RBC (789-8) and hemoglobin (718-7) already matched. All exactMatch 1; concept names from `omop_vocab`.

| Line | Field | v1.6 | v1.7 |
|---|---|---|---|
| 675 | `lbscat_hct` Hematocrit - % | 3009542 *… by calculation* (20570-8) | **3023314** *Hematocrit [Volume Fraction] of Blood by Automated count* (4544-3) |
| 676 | `lbscat_mcv` MCV - fL | 3024731 (30428-7) | **3023599** *MCV [Entitic mean volume] in Red Blood Cells by Automated count* (787-2) |
| 677 | `lbscat_mch` MCH - pg | 3035941 (28539-5), closeMatch 0.75 | **3012030** *MCH [Entitic mass] by Automated count* (785-6) |
| 678 | `lbscat_mchc` MCHC - g/dL | 3003338 (28540-3) | **3009744** *MCHC [Entitic Mass/volume] in Red Blood Cells by Automated count* (786-4) |
| 679 | `lbscat_rdw` RDW - % | 3002385 (30385-9) | **3019897** *Erythrocyte [DistWidth] in Red Blood Cells by Automated count* (788-0) |
| 680 | `lbscat_plt` Platelets - x10E3/µL | 3007461 (26515-7), closeMatch 0.75 | **3024929** *Platelets [#/volume] in Blood by Automated count* (777-3) |

Units are unchanged (the lab's units match the v1.4 CBC unit rows). The lab's NRBC result (58413-6) has no REDCap field yet; see *Added — NRBC* below.

### Added — NRBC (proposed REDCap field)

- Labcorp test 028142 also reports nucleated red blood cells (NRBC) per 100 white blood cells (LOINC 58413-6, unit %), but the REDCap CBC form has no NRBC field. Rows are added in advance for the proposed field `lbscat_nrbc`, so it maps as soon as it is added to the form: question row (line 2127) → **40761514** *Nucleated erythrocytes/Leukocytes [Ratio] in Blood by Automated count* (LOINC 58413-6), exactMatch 1; fixed-unit row `lbscat_nrbc_u` (line 2128) → 8554 *percent* (`%`), as for RDW and hematocrit. Both rows have `transferred_to_fairhub_REDCap_dataset` = Yes, as the other CBC rows: NRBC belongs in the dataset and was missed on the REDCap form. `MODIFIER` is blank on both rows. Note: `lbscat_nrbc` is a proposed REDCap field, not yet on the CBC form; Labcorp 028142 reports NRBC per 100 WBC (LOINC 58413-6), so it should have been included. `lbscat_nrbc` maps to **40761514** *Nucleated erythrocytes/Leukocytes [Ratio] in Blood by Automated count* (line 2127), with unit 8554 *percent* (`lbscat_nrbc_u`, line 2128); the value maps as soon as the field is added. `unit_concept_lookup.csv`: 115 rows (field 90, string 25).

### Changed — Map_to_OMOP: old MoCA unit rows (lines 648–667)

- The 20 original MoCA unit rows (14 `*_time_unit` → 8555 *second*, 6 `*_score_unit` → 44777566 *score*, e.g. `trails_time_unit`, `lettera_score_unit`) are not named after the MoCA measurement fields, so nothing links to them: in the current OMOP data all 30 MoCA measurement fields have `unit_concept_id` 0. They are superseded by the v1.4 `<field>_u` rows (lines 2048–2077), which cover all 30 fields and are used by `unit_concept_lookup.csv`.
- `Map_to_OMOP` Yes → No on lines 648–667; no other column changes (`MODIFIER` stays blank). The rows are kept, not deleted, so the original content and line numbers are preserved, and there are no duplicate active MoCA unit rows. The replacement row for each is listed in the v1.7 decision record. map2omop and the open-source public file each lose these 20 rows; the unit lookup is unchanged (it never used them).
- The generic unit-text rows `s`, `second` → 8555 and `score` → 44777566 (lines 668–670) stay active; the lookup uses them.

### ETL rules (for the survey ETL)

1. **One procedure per "Yes".** Answers are matched on `FIELD_ID` (REDCap field) + `SRC_CODE` (answer code). A "Yes" (1) now matches two rows: the Yes row (Meas Value → `value_as_concept_id` on the OBSERVATION) and the procedure row (Procedure → one PROCEDURE_OCCURRENCE row). A "No" matches only the No row, so no procedure is written. Procedure rows are not merged: up to 22 per eye per visit.
2. **Date.** `procedure_date` = the form's Assessment Date (`rt_dat`, line 1742), the same date for every scan on the form.
3. **Laterality.** For Procedure rows whose `qualifier_concept_id` is a CPT4 Modifier (45888271, 45888270), write `qualifier_concept_id` to `modifier_concept_id` and `qualifier_source_value` to `modifier_source_value`. The monofilament Procedure rows (742–765) are unchanged and not covered by this rule.
4. **Source concept.** `procedure_source_concept_id` = the AI-READI custom concept of the imaging question (the `TARGET_CONCEPT_ID` of the question row whose `SRC_CODE` equals the procedure row's `FIELD_ID`; for example `rtso_odo` → 2005200297 *Spec-ONH-RC-HR-OCT*). `procedure_source_value` = the REDCap field, as for other tables.
5. **Units.** Fill `unit_concept_id` with `unit_concept_lookup.csv` (scripts `03_` / `04_`), matching on the trimmed field name and the trimmed unit text: the current data has `unit_source_value` " " (a single space) on the MoCA rows and a leading space on lab units (" mg/dL"). Write `unit_source_value` trimmed.

### Changed — scripts

- `count_concept_map.sql`: expected values updated to v1.7 (standard predicates: exact 1,267; close 257); the laterality query includes the CPT4 modifiers.
- `validate_concept_map_vocab.sql`: new check V10 (Procedure rows: the target is in the Procedure domain and a laterality qualifier is a CPT4 Modifier; expect only the two monofilament "Tested" rows); V0 row counts.
- Unit lookup scripts (`value-set-mapping-common/scripts/`): `03_left_join_unit_lookup_template.sql`, `04_example_omop_survey_measurement.sql`, `USAGE.md` and `README.md` write `unit_source_value` trimmed, with blank text as NULL (`NULLIF(TRIM(…), '')`, ETL rule 5); `USAGE.md` explains the MoCA unit rows, the generic `s`/`second`/`score` unit-text keys and blank unit text.
- `audit_concept_map.py`: A5 label lists Procedure among the expected duplicate-key pairs (A5 rises from 34 to 78 with the 44 new pairs).

### Regenerated

- map2omop (2,102 rows) and open-source public (1,993) versions, SSSOM (2,051 rows; 76 incomplete) and LinkML (2,127 records; `CPT4` added to the vocabulary enum) from the v1.7 common file. `unit_concept_lookup.csv` rebuilt (115 rows); `medication_route_lookup.csv` unchanged.
- Counts (`run_counts.py`): standard 1,506 (396 concepts); custom 487 (342); mapped 1,993 (738 concepts); designated but unmapped 134 (+20 "Superseded unit row"). The 44 procedure rows, the unit rows and the proposed NRBC field are not REDCap data elements in the curated dictionary, so, as with the earlier unit rows, "not designated" falls from 827 to 779 against the fixed total of 2,906.

### Not yet included

- Monofilament redesign (one procedure per foot, site results as measurements): deferred.

## [v1.6] - 2026-10-22

Lab and vital-sign measurements moved from SNOMED to standard LOINC concepts, unit rows added for the three ratio fields, and the leftover answers of two removed questions excluded. Target concepts change on 4 rows, `Map_to_OMOP` on 4 rows, and 3 unit rows are appended, so the ETL must be re-run to apply these changes. Edits to existing rows are in place and the new rows are appended at the end (lines 2078–2080), so every existing line number is the same as in v1.5. Concept IDs and names were confirmed in the deployed OMOP vocabulary (Databricks `omop_vocab`).

### Changed — target concept (SNOMED → LOINC)

- `import_ag_ratio` "A/G Ratio (calculated field)" (line 584): 4288601 *Albumin/Globulin ratio* (SNOMED 687005) → 3020509 *Albumin/Globulin [Mass Ratio] in Serum or Plasma* (LOINC 1759-0, Lab Test), exactMatch 1. Every other imported lab already maps to a LOINC lab test. Current OMOP data: 3,984 values, median 1.72.
- `import_buncreatinineratio` "BUN/Creatinine ratio" (line 554): 4112223 *BUN/Creatinine ratio* (SNOMED 18207002) → **3033837 *Creatinine/Urea nitrogen [Mass Ratio] in Serum or Plasma*** (LOINC 31045-8, Lab Test), exactMatch 1. The REDCap calculated field stores **creatinine ÷ BUN**, the inverse of its label: compared with each person's own BUN and creatinine on the same date, all 3,981 values in the current OMOP data match creatinine ÷ BUN (median 0.053; BUN ÷ creatinine would be 18.75). The row is mapped to what is stored, with `MODIFIER` "Stored value is creatinine/BUN (REDCap calculation inverted; field label says BUN/Creatinine); remap to 3018311 (LOINC 3097-3) when the REDCap formula and values are corrected". `SRC_CD_DESCRIPTION` keeps the REDCap label. The data team has been asked to correct the formula.
- `bmi_vsorres` "BMI" (line 858): 4245997 *Body mass index* (SNOMED 60621009) → 3038553 *Body mass index (BMI) [Ratio]* (LOINC 39156-5), exactMatch 1, the standard BMI concept used in OHDSI phenotypes.
- `waist_vsorres` "Waist Circumference (cm)" (line 859): 4172830 *Waist circumference* (SNOMED 276361009) → 3016258 *Waist Circumference at umbilicus by Tape measure* (LOINC 8280-0), closeMatch 1. Measurement at the umbilicus with a tape measure is accepted for AI-READI; closeMatch because the site is not stated on the form.
- Kept on SNOMED: hip circumference (line 860; LOINC has only a protocol term, 62409-8) and waist/hip ratio (line 861; no LOINC term).

### Added — units

- Fixed-unit rows for the three ratio fields, same format as the v1.4 fixed-unit rows (`MODIFIER` "fixed unit; no REDCap unit field"): `import_ag_ratio_u` (line 2078), `whr_vsorres_u` (line 2079) and `import_buncreatinineratio_u` (line 2080) → 8523 *ratio* (UCUM `{ratio}`). A ratio of two values in the same unit is dimensionless; the unit is the same whichever way the BUN/creatinine ratio is calculated. v1.4 had left these fields without a unit.
- `unit_concept_lookup.csv` (and `01_create_unit_lookup.sql`): 113 rows (field 88, string 25), up from 110; row counts updated in the scripts' README, USAGE and SQL comments.

### Changed — Map_to_OMOP

- `dri3` "Driver's License photocopied" answers (lines 277–278) and `cmotyn` "Are there any other medications that you are currently taking that are not included here?" answers (lines 730–731): `Map_to_OMOP` Yes → No. In the master REDCap dictionary the `dri3` question was deleted (6/27/2023) and the `cmotyn` question was excluded from mapping (4/25/2024), but their Yes/No answer rows had been left as Yes. Neither field appears in the current OMOP survey data. map2omop and the open-source public file each lose these 4 rows.

### Changed — scripts

- `count_concept_map.sql`: answer rows of an excluded question (`Map_to_OMOP` = No) are reported as designated-but-unmapped with the reason "Answer to an excluded question"; expected values updated to v1.6.
- `audit_concept_map.py` (check A8) and `validate_concept_map_vocab.sql` (check V9): answer rows already excluded (`Map_to_OMOP` = No) are no longer flagged. A8 now lists 3 rows (administrative BCVA "not done" and satisfaction-survey rows).

### Regenerated

- map2omop (2,074 rows) and open-source public (1,965) versions, SSSOM (2,003 rows; 76 incomplete) and LinkML (2,079 records) from the v1.6 common file. `medication_route_lookup.csv` checked against the map: unchanged.
- Counts (`run_counts.py`): standard 1,478 (392 concepts); custom 487 (342); mapped 1,965 (734 concepts); designated but unmapped 114. The 3 added unit rows lower "not designated" from 830 to 827 against the fixed total of 2,906.

### Reviewed and not changed

- LDL cholesterol (lines 537–538): the unit row `import_ldl_cholesterol_u` does not follow the `<field>_u` pattern because the REDCap names differ: the data uses `import_ldl_cholesterol_calculation` (3,984 rows in the current OMOP data) and the REDCap unit field is `import_ldl_cholesterol_u`. The extra key in `unit_concept_lookup.csv` (and the UNION in `01_create_unit_lookup.sql`) is the documented exception.

### Not yet included

- CBC method codes: hematocrit (line 675) stays *by calculation* (20570-8, 3009542) unless the lab confirms it is measured directly (then 4544-3, 3023314); MCV, MCH, MCHC, RDW and platelets (676–680) may move to their "by Automated count" codes (3023599, 3012030, 3009744, 3019897, 3024929) once the lab confirms an automated analyzer. Waiting on the performing labs.

## [v1.5] - 2026-10-19 - 10.5281/zenodo.23488128

Corrections from a full review of all 2,076 rows of v1.4 (the first review of the whole file; earlier releases reviewed only the rows in each batch of changes). Target concepts change on 10 rows, qualifier concepts on 2 rows and field names on 5 answer rows, so the ETL must be re-run to apply these changes. All edits are in place: no rows are added or removed, so every line number is the same as in v1.4. Concept IDs and names for the new standard concepts were confirmed in the deployed OMOP vocabulary (Databricks `omop_vocab`).

### Changed — target concept

- Health history, "Has a doctor or other healthcare professional ever told you that you have/had…": two "Yes" answers moved from AI-READI custom concepts to standard SNOMED conditions, so standard OHDSI cohorts find these participants. As in v1.3, the matching question row's `MODIFIER`, `qualifier_concept_id` and `qualifier_source_value` change with the answer, so OBSERVATION and CONDITION_OCCURRENCE carry the same concept.
  - `mhoccur_strk` "Stroke" (answer line 340, question line 293): custom 2005200628 → 381316 Cerebrovascular accident (SNOMED 230690007), exactMatch 1.
  - `mhoccur_rnl` "Kidney problems" (answer line 392, question line 310): custom 2005200017 → 198124 Kidney disease (SNOMED 90708001), closeMatch 0.75. "Kidney problems" is a lay umbrella term, so the match is to the broad parent, as for `mhoccur_ua` in v1.3.
  - Custom concepts 2005200628 and 2005200017 are no longer referenced but are kept in `concept_manual.csv` (IDs are not reused).
- `susmkdosfr` "31-40 (up to 2 packs)" (line 1923), answer to "On average how many cigarettes do/did you usually smoke in a day?": 45884478 *31 or more (3 points)* (LOINC LA15915-4, closeMatch 1) → new AI-READI custom concept **2005200636** *31-40 (up to 2 packs)*, exactMatch 1. The LOINC answer means 31 or more, but the map used it only for 31–40 while 41–50 and >50 use custom concepts 2005200194 and 2005200195, so a query on 45884478 missed the heaviest smokers. In the current OMOP survey data this affects 41 participants (31–40); 18 more are in the 41–50 and >50 ranges.
- `cm_asp`, `cm_act`, `cm_ibp`, `cm_ant`, `cm_dcg`, `cm_slp` answer "A few days (<1 day/week)" (lines 690, 697, 704, 711, 718, 725), answers to "Have you taken [aspirin, acetaminophen, ibuprofen, antihistamines, decongestants, sleeping pills] in the past 2 weeks?": 45884557 *Less than a day* (LOINC LA14482-6, a duration answer, closeMatch 0.75) → 36210209 *Less than once a week* (LOINC LA27722-0, a frequency answer), exactMatch 1.
- `cmroute` question "How is it taken? (ex. oral, cream, injection, etc.)" (line 331, protected field): 44786711 *Dose form – RxNorm RXCUI of Medication* (LOINC 74054-8, closeMatch 0.75) → 0, with `MODIFIER` "No matching concept; answers populate DRUG_EXPOSURE.route_concept_id". The question asks for a route, not a dose form; since v1.4 the answers map to SNOMED Route concepts.

### Fixed — answer field names

Two answer sets used a `FIELD_ID` that does not exist in REDCap, so the ETL could not link those answers to their question and wrote `value_as_concept_id` = 0. Confirmed in the current OMOP survey data.
- `pdrx9` "On a scale of 1-6, how stressful was this for you?" (racial/ethnic discrimination survey; question line 1052): answers on lines 1149–1151 (1 "Not at all stressful", 6 "Extremely stressful", 777 "Prefer not to say") had `FIELD_ID` `pxrd9` → `pdrx9` (`SRC_CODE_ID` `pxrd9_1` → `pdrx9_1`, etc.). The REDCap field name is `pdrx9`. All 1,896 `pdrx9` rows currently have concept 0.
- `pxne9` (neighborhood environment survey): answers on lines 994–995 (555 "Don't know/Not sure", 777 "Prefer not to say") had `FIELD_ID` `pxne9_` → `pxne9` (`SRC_CODE_ID` `pxne9__555` → `pxne9_555`, etc.). 71 `pxne9` rows currently have concept 0.

### Added

- AI-READI custom concept 2005200636 "31-40 (up to 2 packs)" (Meas Value, Answer) in `OHDSI-vocabulary-request/concept_manual.csv` and `AI-READI-Vocabulary/concept_manual_AIREADI.csv` (now 334 concepts; 418 in total), with a broadMatch to 45884478 *31 or more (3 points)* in `concept_relationship_manual.csv`.
- Release audit scripts in `redCapDataDictionaryWithExtension/scripts/`, to run before every release:
  - `audit_concept_map.py`: structural checks (custom targets present in `concept_manual.csv` with matching name and domain; one name, domain, vocabulary and code per concept ID; standard flags; predicate and confidence rules; duplicate keys; hidden spaces; custom Condition targets; answer rows whose `FIELD_ID` matches no question row) and review lists (answers whose text differs from the target name; questions mapped to standard concepts; "Other" rows). Writes a Markdown report. Runs on the CSV (with line numbers) or, in Databricks, on the loaded tables with `run_audit_table()`. Standard library only.
  - `validate_concept_map_vocab.sql` (Databricks): checks every target, value and qualifier concept against `omop_vocab` (exists, standard, valid; name, domain, vocabulary and code match; unit and route domains), the same structural checks on the loaded table, and lookups.

### Changed — metadata

- `PREDICATE_ID`/`CONFIDENCE` for the "Other (please specify)" questions `scrsexot` (line 20) and `ethnicot` (line 22), exactMatch 1, and `raceot` (line 25), closeMatch 1 → closeMatch 0.75, matching `cl_maristatot` (line 45, changed in v1.3.1). A free-text "other" field is not the question itself.

### Fixed

- `TARGET_CONCEPT_CODE` 118575009 removed from 32 survey timestamp rows mapped to custom concepts 2005200558 (Survey Started Timestamp) and 2005200559 (Survey Completed Timestamp); custom concepts have no code, and 2 rows (931, 932) were already blank.
- Hidden characters: leading space removed from `MODIFIER` on lines 868 and 869 (`paate_6hr`, " 6 hours | 4048382" → "6 hours | 4048382"). The v1.3.1 clean-up removed non-breaking spaces but did not check `MODIFIER` for ordinary leading spaces.
- `AI-READI-Vocabulary/README.md`: lists the retirement of 2005200222 "Puff" (v1.4, not recorded there in v1.4) and the addition of 2005200636.
- `codemeta.json`: `dateModified` updated (was 2026-10-16).

### Regenerated

- map2omop (2,075 rows) and open-source public (1,966) versions, SSSOM (2,000 rows; 76 incomplete, +1 for `cmroute` → 0) and LinkML from the v1.5 common file. `unit_concept_lookup.csv` (110 rows) and `medication_route_lookup.csv` (26 rows) checked against the map: unchanged.
- Counts (`run_counts.py`): standard 1,479 (391 concepts); custom 487 (342); mapped 1,966 (733); designated but unmapped 110. Expected values in `count_concept_map.sql` updated to v1.5.

### Reviewed and not changed

- `dmlpor` question (line 147, *Able to control portion size*, closeMatch 0.75): describes ability rather than approach, but no better standard concept exists and the answers are exact custom concepts.
- `moca_total_score` (line 647, *Montreal Cognitive Assessment version 8.1*): the study used MoCA 8.1.
- Custom "Other heart issues" (337), "Circulation problems" (343) and "Elevated A1C levels" (1869): no single standard concept covers these grouped questions; elevated A1C to be reviewed again.
- `susmkdosfr` question (line 1888, 40769208 *How many of these do you smoke per day [#] [PhenX]*, LOINC 66548-9): 63640-7 *How many cigarettes per day do, or did, you smoke* (40766364) matches the wording and owns the 21–30 answer list, but it is a nominal (range) question, while most AI-READI answers are counts from 1 to 20, which suit the quantitative 66548-9. Kept.
- `pxrd52`/`pxrd53` "How different would your life be now…" (lines 1390–1402): the 6-point answers map to three LOINC answers (*About the same*, *Slight change*, *Major change*), closeMatch 0.75. Kept: the current OMOP data keeps the exact answer code (1–6) in `value_as_number`, so no detail is lost.

### Not yet included

- CBC method-specific LOINC codes (hematocrit 20570-8 *by calculation* vs 4544-3 *by Automated count*): waiting on the performing labs.

## [v1.4] - 2026-10-19

Adds unit mappings and corrects medication route and dose-unit answers. Target concepts change on 18 rows, source codes on 4 rows, and 72 rows are added, so the ETL must be re-run to apply these changes. All new rows are appended at the end of the file (lines 2006–2077), so every existing row keeps its v1.3.1 line number. Unit rows are matched by `FIELD_ID` (e.g. `import_potassium_u`) or by the unit text in `SRC_CODE`, not by position.

### Added — units

- Generic unit-string lookup (lines 2006–2018, same format as lines 1997–2005; blank FORM_NAME and FIELD_ID, unit text in `SRC_CODE`): x10E3/µL → 8848 thousand per microliter; x10E6/µL → 8815 million per microliter; fL → 8583 femtoliter; pg → 8564 picogram; cm → 8582 centimeter; kilograms → 9529 kilogram; kg/m2 → 9531 kilogram per square meter; mmHg → 8876 millimeter mercury column; bpm → 8541 per minute; mg/g → 8723 milligram per gram; diopter → 9291 diopter; degree → 9484 degree; kg → 9529 kilogram (alias of "kilograms").
- Fixed-unit rows for measurements that have no REDCap unit field (the unit is fixed and appears only in the field label). Each is named after its field plus `_u`, with `FIELD_ID_NUM` blank and `MODIFIER` "fixed unit; no REDCap unit field":
  - Imported labs (lines 2019–2020): `import_globulin_total_norc_u` → 8713 gram per deciliter; `import_bilirubin_total_u` → 8840 milligram per deciliter. Units confirmed from the data (medians 2.6 g/dL and 0.5 mg/dL).
  - Physical assessment (lines 2021–2031): height, waist, hip → cm 8582; weight → kilograms 9529; BMI → kg/m2 9531; systolic and diastolic BP (×2) → mmHg 8876; heart rate (×2) → bpm 8541.
  - CBC (lines 2032–2040): WBC, platelets → x10E3/µL 8848; RBC → x10E6/µL 8815; hemoglobin, MCHC → g/dL 8713; hematocrit, RDW → % 8554; MCV → fL 8583; MCH → pg 8564.
  - Autorefractor (lines 2041–2046): sphere and cylinder (both eyes) → diopter 9291; axis (both eyes) → degree 9484.
  - Urine albumin/creatinine ratio (line 2047): `import_uarc_u` → mg/g 8723.
  - MoCA (lines 2048–2077): each MoCA measurement field gets its own unit row: the 16 score fields (14 item scores, combined MIS score, total score) → score 44777566; the 14 time fields → second 8555 (UCUM `s`). The existing MoCA unit rows (lines 648–667, e.g. `trails_time_unit`) are unchanged; they are not named after the measurement fields, so they were not being applied.

### Added — unit lookup scripts

- `redCapDataDictionaryWithExtension/value-set-mapping-common/scripts/` (Databricks SQL), so the ETL can fill `unit_concept_id` with one lookup table and one LEFT JOIN:
  - `USAGE.md`: step-by-step usage; `README.md`: overview and the full lookup content.
  - `00_load_concept_map.sql`: loads the mapping file as `concept_map` if needed.
  - `unit_concept_lookup.csv`: the ready-made lookup table (110 rows; `key_type`, `lookup_key`, `unit_concept_id`, `unit_source_value`), and `01a_load_unit_concept_lookup_csv.sql` to load it as the table `unit_lookup`.
  - `01_create_unit_lookup.sql`: alternatively, one query that builds the same table `unit_lookup` from the concept map (110 rows, one per key): 85 keyed by measurement field name (the `<field>_u` Unit rows, plus the LDL field whose unit field has a different name) and 25 keyed by unit text (generic Unit rows plus `s`, `second`, `score`).
  - `02_view_unit_lookup.sql`: review queries and a duplicate-key check.
  - `03_left_join_unit_lookup_template.sql`: the LEFT JOIN to add to the ETL (field name first, then unit text, otherwise 0).
  - `04_example_omop_survey_measurement.sql`: the same join, ready to run on `omop_survey.measurement`.
  - `05_check_no_fanout.sql`: checks that the join adds no rows.
  - `06_check_units_after_etl.sql`: checks MEASUREMENT units after the ETL re-run.
  - Medication route: `medication_route_lookup.csv` (26 rows: `cmroute` answer code or label → SNOMED Route `route_concept_id`), `07a_load_medication_route_lookup_csv.sql` to load it, `07_create_medication_route_lookup.sql` to build it from the concept map, and `08_left_join_medication_route_template.sql`, the LEFT JOIN for `DRUG_EXPOSURE.route_concept_id`.

### Fixed — MoCA source codes

- `SRC_CODE` for four MoCA rows set back to the REDCap field names used in the data, matching `FIELD_ID`: line 635 `verbal_fluency_language` → `fluency_language`; line 636 `verbal_fluency_language_time` → `fluency_language_time`; line 639 `delayed_recall_with_no_cue` → `delayed_recall_with_no_clue`; line 640 `delayed_recall_with_no_cue_time` → `delayed_recall_with_no_clue_time`. Confirmed in `omop_survey.measurement` (`measurement_source_value` uses the `FIELD_ID` names). This restores the August 2026 correction in `_v5.csv` (commit `01f5c7f`), which was lost when v5 was replaced by v4 (commit `807c116`). Target concepts are unchanged. The custom vocabulary keeps the MoCA dictionary names as concept source codes.

### Changed — target concept (protected fields)

- `cmroute` "How is it taken?" answers (lines 1662–1688) → standard SNOMED Route concepts (domain Route) for `DRUG_EXPOSURE.route_concept_id`, replacing LOINC answer concepts: Intramuscular 4302612, Intraocular 4157760, Intraperitoneal 4243022, Nasal 4262914, Oral 4132161, Rectal 4290759, Inhalation 40486069 Respiratory tract (closeMatch 1), Subcutaneous 4142048, Topical 4263689, Transdermal 4262099, Vaginal 4057765. Intralesional (4157758) unchanged. Other (888) → 0, no matching concept.
- `cmdosu` dose-unit answers → UCUM units (domain Unit): Inhalation (line 1696), Puff (line 1714) and Spray (line 1751) → 45744809 Actuation `{actuat}` (closeMatch 1); Tablet (line 1752) → 9431 tablet `{tbl}`. Capsule (line 1692) and Other (line 1755) → 0; no UCUM concept exists for capsule.
- Puff previously mapped to AI-READI custom concept 2005200222 (domain Device). That concept is retired: removed from `concept_manual.csv`, from `concept_relationship_manual.csv` (its broadMatch to 45758813 Metered dose inhaler) and from the split file `AI-READI-Vocabulary/concept_manual_AIREADI.csv` (now 333 concepts; 417 in total). It remains in the frozen October 2025 submission.

### Regenerated

- map2omop and open-source public versions, SSSOM and LinkML from the v1.4 common file; split custom vocabulary files from `concept_manual.csv`.
- Counts: standard 1,479 (391 concepts); custom 488 (343); mapped 1,967 (734); designated but unmapped 109. The 72 added unit rows are counted as mapped elements although they are not REDCap data elements, so "mapped" rises and "not designated" falls from 902 to 830 against the fixed total of 2,906; `count_concept_map.sql` comments updated.

### Not yet included

- CBC method-specific LOINC codes (hematocrit and others): waiting on the labs.

## [v1.3.1] - 2026-10-18

Metadata-only release. No `TARGET_CONCEPT_ID`, `value_as_concept_id`, `qualifier_concept_id` or `Map_to_OMOP` values changed; counts are unchanged from v1.3, and no ETL re-run is required.

### Changed — metadata

- `TARGET_CONCEPT_CLASS_ID`: removed the trailing space from "Assessment Item " on 29 MoCA rows (lines 615–642, 644), matching `concept_manual.csv`.
- `Extension_Needed` set to match the target concept: "Yes" for the 34 rows that map to AI-READI custom concepts but were marked "No" (lines 11–12, 17–18, 615–642, 644, 646); "No" for line 1893 (`subrdosfr`, standard concept 40766674), consistent with the other questions that have a standard target and custom answers.
- Predicate and confidence:
  - `cl_maristatot` "Other (please specify)" (line 45): exactMatch 1 → closeMatch 0.75. A free-text "other" field is not the marital status question itself.
  - `pxep1` "Is English your first language?" (line 1409): exactMatch 0.75 → closeMatch 0.75. "First language" vs "primary language"; exactMatch with confidence below 1 was contradictory.
  - `cmdosu_1` "Percent Volume per Volume" (line 1690): exactMatch 0.75 → exactMatch 1. Same unit as 45891010 ({vol}%{vol}).
- `TARGET_CONCEPT_NAME` for custom concept 2005200296 (line 1727): "Eidon-Create Mosaic Image-CFP" → "Eidon- Create Mosaic Image-CFP", matching `concept_manual.csv` and line 1693.

### Fixed — hidden characters

- Removed non-breaking spaces (hidden characters) and stray leading or trailing spaces:
  - `SRC_CD_DESCRIPTION`: lines 41–44, 675, 770, 1049, 1431, 1434, 1449–1451, 1855, 1884, 1895, 1905, 1907.
  - `TARGET_CONCEPT_NAME`: lines 1431, 1434, 1855, 1895, 1907.
  - `MODIFIER`: lines 1449–1451.
- The same clean-up was applied to the names of the five affected AI-READI custom concepts (2005200027, 2005200037, 2005200093, 2005200096, 2005200550) in `redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/concept_manual.csv`, so the names are identical in the map and the custom vocabulary files.

### Added

- `redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/AI-READI-Vocabulary/`: `concept_manual_AIREADI.csv` (334 concepts), `concept_manual_AIREADI-Vision.csv` (54) and `concept_manual_AIREADI-MOCA.csv` (30), generated from the v1.3.1 `concept_manual.csv` by `vocabulary_id`. Together they contain exactly the 418 custom concepts in `concept_manual.csv` (same columns and values). These are the current version of the split. The October 2025 OHDSI submission (Vocabulary-v5.0 issue #1176) in `AIREADi_OMOP_Vocabulary_Request/split_concept_manual/` is kept frozen, unchanged, and differs from the current custom vocabulary: it includes four concepts later retired from the map (2005200193, 2005200236, 2005200239, 2005200560), lacks five added since (2005200455, 2005200632–2005200635), and has blank `valid_start_date` (15 MoCA concepts) or `v6_domain_id` (2005200451, 2005200459, 2005200629) where `concept_manual.csv` has values, and still has non-breaking spaces in five names. `AI-READI-Vocabulary/README.md` now lists the three files and these differences.

### Regenerated

- map2omop and open-source public versions, SSSOM and LinkML from the v1.3.1 common file. Counts unchanged: standard 1,409 (379); custom 489 (344); mapped 1,898 (723); designated but unmapped 106.

## [v1.3] - 2026-10-17

### Changed — target concept

- `cmtrt_lfst_1` "Yes" (line 1873), answer to `cmtrt_lfst` "Do you use lifestyle changes to control your A1C and blood glucose levels?": 607008 (Able to modify behavior and lifestyle to support health improvement, SNOMED Clinical Finding) → 45877994 (Yes, LOINC LA33-6, Meas Value), exactMatch 1. The previous concept described ability rather than practice and did not pair with the "No" answer (`cmtrt_lfst_0`, 45878245 No, LA32-8). In the current OMOP survey data this affects 1,245 participants' "Yes" responses (`value_as_concept_id`); `value_as_string` is unaffected.

- Health history "Has a doctor or other healthcare professional ever told you that you have/had..." (`2005200014`): four condition concepts corrected. Each change updates the "Yes" answer row (CONDITION_OCCURRENCE target) and the matching question row (`MODIFIER`, `qualifier_concept_id`, `qualifier_source_value` on the OBSERVATION record), so both tables carry the same concept.
  - `mhoccur_cns` "Other neurological conditions" (lines 303, 371): 46271045 Neurocognitive disorder → 376337 Disorder of nervous system (SNOMED 118940003), closeMatch 0.75. Neurocognitive disorder covers only cognitive conditions, which have their own questions (dementia, mild cognitive impairment).
  - `mhoccur_ua` "Urinary problems (Examples: urinary tract infections, incontinence, prostate problems)" (lines 309, 389): 81902 Urinary tract infectious disease → 75865 Disorder of urinary system (SNOMED 128606002), closeMatch 0.75. The previous concept covered infections only.
  - `mhoccur_clsh` "High blood cholesterol" (lines 295, 346): 4159131 Dyslipidemia → 4029305 Hypercholesterolemia (SNOMED 13644009), exactMatch 1. The previous concept was broader than the question.
  - `mhoccur_ca` "Cancer (any type)" (lines 306, 380): 4194405 Cancer confirmed (Context-dependent) → 443392 Malignant neoplastic disease (SNOMED 363346000, Disorder), exactMatch 1, the standard concept used for "any cancer" cohort definitions.
- Health history question rows left unchanged in v1.1 (lines 301, 311, 319): v1.1 corrected the "Yes" → Condition targets for `mhoccur_cogn_1` (line 365), `mhoccur_ear_1` (line 395) and `mhoccur_crt_1` (line 421), but the matching question rows kept the old concepts in `MODIFIER`, `qualifier_concept_id` and `qualifier_source_value`. They now match the Condition targets, so OBSERVATION and CONDITION_OCCURRENCE agree:
  - `mhoccur_cogn` (line 301): 439795 Minimal cognitive impairment → 4297400 Mild neurocognitive disorder.
  - `mhoccur_ear` (line 311): 439378 Ear anomalies with hearing impairment → 377889 Hearing loss.
  - `mhoccur_crt` (line 319): 4317977 Bilateral cataracts → 375545 Cataract.

### Fixed

- `dcvgmenyn` "Dexcom G6 transmitter returned?" (line 127): `qualifier_concept_id` 1615066 → 2615313 (Transmitter; external, for use with non-durable medical equipment interstitial continuous glucose monitoring system; HCPCS, Device, standard). Concept 1615066 (GLUCOSE TRANSMITTER DEXCOM G6) is not present in the deployed OMOP vocabulary (Databricks `omop_vocab`), and no Dexcom G6 device concept exists there. 2615313 was chosen over 45764014 (Invasive interstitial-fluid glucose monitoring system, SNOMED) because the question and `qualifier_source_value` refer specifically to the transmitter. `qualifier_source_value` is unchanged. Target concept 2005200589 is unchanged.

- `TARGET_CONCEPT_NAME` aligned with the deployed OMOP vocabulary for two rows (metadata only; concept IDs unchanged):
  - `dvamwendhand_3` (line 140, 763013): "Not Provided" → "Not provided". The map now uses one spelling for this concept.
  - `cmdosfrq` (line 334, 3042548): "Current Medication, Frequency" → "Current medication, Frequency".

### Regenerated

- map2omop and open-source public versions, SSSOM and LinkML from the v1.3 common file. Counts (`run_counts.py`): standard 1,409 elements (379 distinct concepts, down from 380 because 607008 is no longer used; the four condition replacements are one-for-one); custom 489 (344); mapped 1,898 (723); designated but unmapped 106.

### Downstream

- Survey ETL must be re-run to apply all v1.3 changes.
- Note for the ETL team: in the current OMOP survey data, "Yes" answers to the `2005200014` health history questions are written as `value_as_concept_id` 4188539 (SNOMED Yes), while the map specifies 45877994 (LOINC Yes, LA33-6).

## [v1.2.1] - 2026-10-16

### Fixed

- Reverted the v1.2 `TARGET_CONCEPT_NAME` edits for four CBC rows so the names again match the deployed OMOP vocabulary (Databricks `omop_vocab`). The v1.2 names had been taken from an older external vocabulary release (ATLAS demo, Feb 2025). Concept IDs and codes are unchanged; no ETL impact.
  - `lbscat_hct` (line 675, 3009542): Hematocrit [Volume Fraction] of Blood by calculation
  - `lbscat_mcv` (line 676, 3024731): MCV [Entitic mean volume] in Red Blood Cells
  - `lbscat_mchc` (line 678, 3003338): MCHC [Entitic Mass/volume] in Red Blood Cells
  - `lbscat_rdw` (line 679, 3002385): Erythrocyte [DistWidth] in Red Blood Cells

### Regenerated

- map2omop and open-source public versions, SSSOM and LinkML from the v1.2.1 common file.

## [v1.2] - 2026-10-16

### Concept map v1.2 (`_ai_readi_redcap_value_set_mapping_common.csv`)

10 rows changed from `v1.1`: 6 target-concept corrections and 4 concept-name fixes. Line numbers refer to the CSV file (header = line 1).

#### Changed — target concept

- `dmlgrain` (line 146): 46272478 (Assessment of eating and drinking behavior, a SNOMED procedure used with a domain override) → custom 2005200633 (Observation, Survey), exactMatch 1. No standard concept matches the question; LOINC 90725-3 differs in time frame, foods and answer type.
- `eos_dsdecod_1` "Did not meet Inclusion/Exclusion criteria" (line 250): custom 2005200280 → 40480675 (Does not meet eligibility criteria for clinical trial, SNOMED 444734003), exactMatch 1.
- `eos_dsdecod_5` "Investigator deemed not appropriate for study" (line 254): 40480675 (closeMatch 0.75; investigator judgment is not ineligibility) → custom 2005200634 (Meas Value, Answer), exactMatch 1.
- `lbscat_wbc` (line 672): custom 2005200182 → 3000905 (Leukocytes [#/volume] in Blood by Automated count, LOINC 6690-2).
- `lbscat_rbc` (line 673): custom 2005200183 → 3020416 (Erythrocytes [#/volume] in Blood by Automated count, LOINC 789-8).
- `paid_scrd` (line 813): 36716888 (Fear of metabolic disease, a SNOMED Condition-domain clinical finding used with a domain override) → custom 2005200635 (Observation, Survey), exactMatch 1, consistent with the other PAID-5 items.

#### Changed — concept name only (target concept unchanged)

- `lbscat_hct` (675): Hematocrit [Volume Fraction] of Blood (removed "by calculation").
- `lbscat_mcv` (676): MCV [Entitic volume].
- `lbscat_mchc` (678): MCHC [Mass/volume].
- `lbscat_rdw` (679): Erythrocyte distribution width [Ratio].

#### Added

- AI-READI custom concepts 2005200633 (`dmlgrain`), 2005200634 (`eos_dsdecod_5`) and 2005200635 (`paid_scrd`) in `OHDSI-vocabulary-request/concept_manual.csv`. Custom concepts 2005200182, 2005200183 and 2005200280 are no longer referenced but are kept (IDs are not reused).

#### Regenerated

- map2omop and open-source public versions from the v1.2 common file.
- SSSOM and LinkML with `generate_linkml_sssom.py`.
- Counts (`redCapDataDictionaryWithExtension/scripts/run_counts.py`): standard 1,409 (380 concepts); custom 489 (344); mapped 1,898 (724); designated but unmapped 106.

#### Downstream

- Survey ETL must be re-run to apply v1.2.


## [v1.1] - 2026-10-16

### Concept map v1.1 (`_ai_readi_redcap_value_set_mapping_common.csv`)

17 rows changed from `v1.0-tvst`: 11 target-concept corrections and 6 metadata-only fixes. Line numbers refer to the CSV file (header = line 1). Release `v1.0-tvst` and the frozen copy in `manuscript-tvst2026/` are unchanged.

#### Changed — target concept

- Race, Middle Eastern / North African answers (`race_C77820`, `race_C77813`, `race2_C77820`, `race2_C77813`; lines 463, 465, 472, 474): 45877987 (White) → 1546809 (Middle Eastern, OMOP5558948) and 1546912 (North African, OMOP5559052), standard Ethnicity-vocabulary concepts added in July 2025. Answers were previously collapsed into White.
- Hearing loss (`mhoccur_ear_1`, line 395): 439378 (Ear anomalies with hearing impairment, a congenital anomaly) → 377889 (Hearing loss, SNOMED 15188001).
- Cataract (`mhoccur_crt_1`, line 421): 4317977 (Bilateral cataracts) → 375545 (Cataract, SNOMED 193570009); the question does not specify laterality.
- Mild cognitive impairment (`mhoccur_cogn_1`, line 365): 439795 (Minimal cognitive impairment, SNOMED 110352000) → 4297400 (Mild neurocognitive disorder, SNOMED 386805003).
- Last study visit (`eos_dsvst`, line 249): 3655035 (Date of last examination, relatedMatch 0.5) → custom 2005200632, exactMatch 1. The field records which visit/stage was completed, not a date.
- Age (`cage`, line 110): 4265453 (SNOMED Age, Meas Value) → 3022304 (LOINC 30525-0 Age, Observation).
- Hispanic score (`ethnicscore`, line 23) and birth year (`brthyy`, line 109): set to 0 (No matching concept). `ethnicscore` is an internal screening-logic calculation, not Hispanic ethnicity; birth year is carried in `PERSON.year_of_birth`, not as an observation.

#### Changed — metadata only (target concept unchanged)

- `dmlgrain` (line 146): domain Procedure → Observation; predicate exactMatch → closeMatch.
- `dmlfeet_10` "Daily or weekly" (line 186): confidence 1 → 0.75 (target LA18934-2 is "Daily or almost daily", so weekly is not covered exactly).
- `paid_scrd` (line 813): domain Condition → Observation (PAID-5 item response, not a diagnosis); concept 36716888 kept.
- `sualcage` (line 1890): exactMatch 1 → closeMatch 0.75.
- `lbscat_a1c` (line 674): added missing TARGET_CONCEPT_CODE 718-7 for 3000963 (Hemoglobin [Mass/volume] in Blood). Despite the variable name, this field holds total hemoglobin in g/dL, not HbA1c; confirmed against OMOP data (median 13.8; r = 0.004 with `import_hba1c` across 2,212 participants). HbA1c is mapped separately via `import_hba1c`.
- `lbscat_hct` (line 675): removed trailing space from TARGET_CONCEPT_NAME.

#### Added

- AI-READI custom concept 2005200632 "Last study visit/stage completed" (Observation, Survey) in `OHDSI-vocabulary-request/concept_manual.csv`, for `eos_dsvst`.
- `redCapDataDictionaryWithExtension/scripts/count_concept_map.sql` and `run_counts.py`: working count scripts for the maintained mapping file; TARGET_CONCEPT_ID = 0 is counted as designated but unmapped. The frozen manuscript scripts in `manuscript-tvst2026/` are unchanged. Results on v1.1:
  - Standard 1,409 (380 concepts); custom 489 (344); mapped 1,898 (724); designated but unmapped 106, including 2 "No matching concept".
  - Vocabularies: LOINC 1,199/284, SNOMED 131/65, Ethnicity 4/2 (the MENA concepts).
  - Integrity checks: all 4 return 0 rows.
- `redCapDataDictionaryWithExtension/scripts/survey-concept-map-validation.ipynb`: Databricks queries used to validate v1.1 target concepts and to confirm `lbscat_a1c` is total hemoglobin (outputs cleared).

#### Regenerated

- `_ai_readi_redcap_value_set_mapping_common_map2omop.csv` (Map_to_OMOP = Yes; 2,003 rows) and `_ai_readi_redcap_value_set_mapping_map2omop_open_source_public_version.csv` (open-source rows; 1,895 rows) from the v1.1 common file.
- SSSOM and LinkML (`redCapDataDictionaryWithExtension/sssom/`, `linkml/`) with `generate_linkml_sssom.py`: SSSOM 1,932 rows, 72 incomplete (`ethnicscore` and `brthyy` now listed as incomplete); `Ethnicity` added to the LinkML domain and vocabulary enums.


### Manuscript package (changes since v1.0-tvst)

#### Added

- Word (.docx) versions of Supplementary Tables S1 and S2 in `manuscript-tvst2026/supplementary/`.

#### Changed

- Removed the outdated `manuscript-tvst2026/source/Supplementary_Table_S2_Mapping_Quality.docx`; the current .docx is now in `manuscript-tvst2026/supplementary/` alongside the .md and .pdf.

#### Fixed

- Supplementary Table S2 footnote linked the pre-rename `count_mapping_concepts.sql`; it now links `count_concept_map.sql` at tag v1.0-tvst and cites doi:10.5281/zenodo.23375723 (.md and .pdf).


## [v1.0-tvst] - 2026-10-14

First archived release, accompanying the manuscript *"A Generalizable Framework for Mapping Survey, Vision Care, and Cognitive Assessment Data to the OMOP Common Data Model in AI-READI"* (Translational Vision Science & Technology, 2026). Archived on Zenodo: https://doi.org/10.5281/zenodo.23375723

### Added

- `manuscript-tvst2026/`: frozen mapping file, frozen SSSOM and LinkML copies, DuckDB and Databricks count scripts (`count_concept_map*.sql`, `run_counts.py`), OMOP vocabulary validation script, Figures 1–3 and Supplementary Tables S1–S2.
- AI-READI custom concepts:
  - 2005200631 "Location of environmental sensor within home" for `dvenvlocn`, with qualifier 45762337 (Environmental sensor). It was previously mapped to SNOMED 284349006 (4109238), which does not describe sensor location.
  - 2005200630 "Discrimination in Medical Settings (DMS) total score [PhenX]" for `pxdhc_sum`, with qualifier 2005200575 (PhenX SDOH Survey). It was previously unmapped.
- SSSOM mapping set and LinkML schema in `redCapDataDictionaryWithExtension/`.
- `deprecated/` folder with a README describing superseded files.

### Changed

- Non-standard targets replaced with standard concepts after validation against the OMOP Standardized Vocabularies (v5.0, 27-Aug-2025):
  - Heart rate (`pulse_vsorres`): 4239408 (SNOMED 364075005) → 3027018 (LOINC 8867-4, Heart rate).
  - MoCA total score: 37174522 (SNOMED 1255891005) → 606671 (SNOMED 1148423001, Montreal Cognitive Assessment version 8.1).
- Closer standard equivalents:
  - Substance use (`subrdosfr`): 1010004 (LOINC 68518-0) → 40766674 (LOINC 63954-2), closeMatch, confidence 0.75.
  - Current medications, frequency: 4126015 (SNOMED 260864003) → 3042548 (LOINC 52810-9, Current Medication, Frequency).
  - Disposition reason: 4260904 (SNOMED 410666004) → 44810920 (SNOMED 871401000000109), relatedMatch, confidence 0.5; no exact standard concept, flagged for review.
- Insulin mapped to LOINC 3695-4 (Mass/volume) with ng/mL units.
- Count scripts renamed `count_mapping_concepts*.sql` → `count_concept_map*.sql`; `run_counts.py` now prints UTF-8 output on Windows.
- Supplementary Table S1 now links the MoCA to https://mocacognition.com/paper; the MoCA 8.1 test form PDF was removed (copyright).
- `_v4` and `_v5` copies of the common mapping file moved to `deprecated/`; map2omop and open-source public versions regenerated from the common file.
- Top-level README, `CITATION.cff` and `codemeta.json` rewritten for this repository (previously template content).
- Superseded mapping files and folders moved to `deprecated/`.

### Fixed

- REDCap survey start/completion timestamp concepts swapped back for the PhenX racial and ethnic discrimination survey (`pxrdstartts` → 2005200558 Survey Started Timestamp; `pxrdcmpts` → 2005200559 Survey Completed Timestamp).
- Lab result unit rows (25) that had a blank UCUM `TARGET_CONCEPT_ID` after the lab mappings were merged into the common file are now filled in.
- Excel-corrupted values restored: long concept codes converted to scientific notation (e.g., 434941000124101, 859981000000107, 449921000124105, 873751000000103, 368441000000106) and answer ranges converted to dates (e.g., "4-Mar" → "3-4", "2-Jan" → "1-2").
- Concept IDs that had been entered in the concept code field corrected.
- Concept names that did not match the OMOP vocabulary concept name corrected.
- Missing laterality qualifiers added: Snellen visual acuity rows (Right eye / Left eye) and monofilament foot sensation rows (Structure of right foot / Structure of left foot).
