# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Where to find the mapping files

- **Working version (use for ETL):** `redCapDataDictionaryWithExtension/value-set-mapping-common/_ai_readi_redcap_value_set_mapping_common.csv`. This file is actively maintained and may change after each release.
- **Frozen release version:** `manuscript-tvst2026/ai_readi_redcap_value_set_mapping_common.csv` (with frozen SSSOM and LinkML copies), matching release `v1.0-tvst` and the TVST 2026 manuscript.

## [Unreleased]

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
