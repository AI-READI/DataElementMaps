# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Where to find the mapping files

- **Working version (use for ETL):** `redCapDataDictionaryWithExtension/value-set-mapping-common/_ai_readi_redcap_value_set_mapping_common.csv`. This file is actively maintained and may change after each release.
- **Frozen release version:** `manuscript-tvst2026/ai_readi_redcap_value_set_mapping_common.csv` (with frozen SSSOM and LinkML copies), matching release `v1.0-tvst` and the TVST 2026 manuscript.

## [Unreleased]
### Added

- Word (.docx) versions of Supplementary Tables S1 and S2 in `manuscript-tvst2026/supplementary/`.
### Changed

- Removed the outdated `manuscript-tvst2026/source/Supplementary_Table_S2_Mapping_Quality.docx`; the current .docx is now in `manuscript-tvst2026/supplementary/` alongside the .md and .pdf.


### Fixed

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
