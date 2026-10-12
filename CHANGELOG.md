# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]
- prior versions are used for development and testing

## [v1.0-tvst] - 2026-10-11

First archived release, accompanying the manuscript *"A Generalizable Framework for Mapping Survey, Vision Care, and Cognitive Assessment Data to the OMOP Common Data Model in AI-READI"* (Translational Vision Science & Technology, 2026).

### Added

- `manuscript-tvst2026/`: frozen mapping file, DuckDB and Databricks count scripts, OMOP vocabulary validation script, Figures 1–3 and Supplementary Tables S1–S2.
- AI-READI custom concepts 2005200630 (PhenX DMS total score) and 2005200631 (dvenvlocn).
- SSSOM mapping set and LinkML schema in `redCapDataDictionaryWithExtension/`.
- `deprecated/` folder with a README describing superseded files.

### Changed

- Laterality qualifiers added to Snellen visual acuity rows and corrected on monofilament foot rows (Structure of right foot 4298982; Structure of left foot 4320144).
- Standard concepts replaced after validation against the OMOP Standardized Vocabularies (e.g., heart rate 3027018, LOINC 63954-2, LOINC 52810-9, SNOMED 1148423001).
- Insulin mapped to LOINC 3695-4 (Mass/volume) with ng/mL units; 24 missing lab unit concepts added.
- Top-level README, `CITATION.cff` and `codemeta.json` rewritten for this repository (previously template content).
- Superseded mapping files and folders moved to `deprecated/`.

### Fixed

- Swapped REDCap survey start and completion timestamp concepts.
- Excel-corrupted values: concept codes converted to scientific notation and answer ranges converted to dates.
- Malformed `_v5` mapping file restored from `_v4`.
- release version is ai_readi_redcap_value_set_mapping_common.csv
- current release mapping file is located in the manuscript-tvst2026/
- working version is located in the redCapDataDictionaryWithExtension/value-set-mapping-common/
- working directory contains the ai_readi_redcap_value_set_mapping_common.csv, which should be used for ETL. 
