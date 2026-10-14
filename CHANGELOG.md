# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]
- prior versions are used for development and testing

## [v1.0-tvst] - 2026-10-14

First archived release, accompanying the manuscript *"A Generalizable Framework for Mapping Survey, Vision Care, and Cognitive Assessment Data to the OMOP Common Data Model in AI-READI"* (Translational Vision Science & Technology, 2026).

### Added

- `manuscript-tvst2026/`: frozen mapping file, DuckDB and Databricks count scripts, OMOP vocabulary validation script, Figures 1–3 and Supplementary Tables S1–S2.
- AI-READI custom concepts 2005200630 (PhenX DMS total score) and 2005200631 (dvenvlocn).
- SSSOM mapping set and LinkML schema in `redCapDataDictionaryWithExtension/`.
- `deprecated/` folder with a README describing superseded files.

### Changed

- Standard concepts replaced after validation against the OMOP Standardized Vocabularies from non-standard (e.g., heart rate 3027018, LOINC 63954-2, LOINC 52810-9, SNOMED 1148423001).
- Insulin mapped to LOINC 3695-4 (Mass/volume) with ng/mL units; 24 missing lab unit concepts added.
- Top-level README, `CITATION.cff` and `codemeta.json` rewritten for this repository (previously template content).
- Superseded mapping files and folders moved to `deprecated/`.
- New custom concept created to support the following concept
Line 436, dvenvlocn (“Location of the environmental sensor in the home”): **dvenvlocn** → 2005200631 (436) and PhenX DMS → 2005200630 (1408)
It was mapped to SNOMED 4109238 (284349006), which doesn’t describe sensor location.
No suitable standard concept exists, so it now uses the new custom concept 2005200631, “Location of environmental sensor within home”, with qualifier 45762337 (Environmental sensor).
- Line 1408, pxdhc_sum (PhenX Discrimination in Medical Settings summary score):
It was previously unmapped.
It now uses the new custom concept 2005200630, “Discrimination in Medical Settings (DMS) total score [PhenX]”, with qualifier 2005200575 (PhenX SDOH Survey).
- concept map changed for MoCA total score/ 37174522 (SNOMED 1255891005) -> 606671 (SNOMED 1148423001), class Staging / Scale


### Fixed

- Swapped REDCap survey start and completion timestamp concepts.
- Excel-corrupted values: concept codes converted to scientific notation and answer ranges converted to dates.
- the swapped timestamp concepts (1098/1099) Survey timestamp concepts swapped back (lines 1098–1099)
In the PhenX racial and ethnic discrimination survey, the start and completion timestamps were mapped the wrong way round:
pxrdcmpts (completion) pointed to 2005200558 Survey Started Timestamp;
pxrdstartts (start) pointed to 2005200559 Survey Completed Timestamp.
- heart rate (864/867), MoCA total (647), line 1893, line 334, line 246
- 25 lab unit rows that had no UCUM concept
- the Excel-corrupted codes found in the mapping csv, fixed
- line 647 - failed standard validation test (non-standard vs standard)  - use the standard concept
- line 864,867 - non-standard vs. standard - use standard concept
Heart rate (pulse_vsorres)
4239408 (SNOMED 364075005)
3027018 (LOINC 8867-4, Heart rate)
Standard Measurement-domain concept for a recorded vital sign
- Line 1893 - found a better term
Substance use item (subrdosfr)
1010004 (LOINC 68518-0) -> 40766674 (LOINC 63954-2)closeMatch, confidence 0.75 Closer standard equivalent
- Line 334 - found a better term
Current medications, frequency/ 4126015 (SNOMED 260864003)-> 3042548 (LOINC 52810-9, “Current Medication, Frequency”)
Question-level LOINC concept matches the item
- Line 246 - found a better term
Disposition reason
4260904 (SNOMED 410666004) -> 
44810920 (SNOMED 871401000000109), relatedMatch, confidence 0.5
No exact standard concept; nearest related concept kept and was flagged for review

- We used to have the lab results in the separate mapping file, but they are all merged. In the merged list the UCUM unit concept id was blank in the target_concept_id column. They are now all filled in. 25 rows of imported lab result unit (line range: 506-613)
- Values corrupted by excel- found few values that were turned into a scientific notation when the code value was long ( i.e. 434941000124101, 859981000000107, 449921000124105, 873751000000103, 368441000000106)
For example, case of 4-Mar when it should be 3-4 and case of 2-Jan when it should be 1-2

-line 862,865,863,866 - concept id was entered into the code field - corrected.

- Concept names did not match the concept name in the OMOP vocabulary table - corrected

- Laterality qualifiers added for eye and foot measurements - missing qualifier values added
Snellen visual acuity rows were missing the qualifier concept id for right eye or left eye 
Monofilament foot sensation rows were missing the laterality qualifier - right or left


## release version is ai_readi_redcap_value_set_mapping_common.csv
- current release concept map csv file is located in the manuscript-tvst2026/
- working version is located in the redCapDataDictionaryWithExtension/value-set-mapping-common/
note, the working directory contains the ai_readi_redcap_value_set_mapping_common.csv, which should be used for ETL. This file is working file so it can change after each release. The fronzen release version is in the manuscript-tvst2026 folder