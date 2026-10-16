# Supplementary Table S2. Mapping Relationships, Confidence Scores, Reasons for Non-Mapping, and Laterality Qualifiers in the AI-READI Survey-to-OMOP Mapping

## A. Mapped data elements by SKOS mapping relationship and confidence score

| Target concept type | SKOS mapping relationship | Confidence 1.0 | Confidence 0.75 | Confidence 0.5 | Total |
|---|---|--:|--:|--:|--:|
| **Standard OMOP concepts** | | **1,327** | **83** | **2** | **1,412** |
| | Exact match | 1,171 | 3 | 0 | 1,174 |
| | Close match | 156 | 79 | 0 | 235 |
| | Related match | 0 | 1 | 2 | 3 |
| **AI-READI custom concepts** | | **488** | **0** | **0** | **488** |
| | Exact match | 488 | 0 | 0 | 488 |
| **Total mapped elements** | | **1,815** | **83** | **2** | **1,900** |

Counts are mapped data elements (n = 1,900). Mappings with an exact or close match and a confidence score of at least 0.75 were accepted; all others were flagged for working group review. Two related-match mappings at confidence 0.5 were retained as standard concepts after review. All AI-READI custom concept mappings are exact matches at confidence 1.0.

## B. Data elements designated for mapping but not mapped to concepts, by reason

| Reason | n | % of 104 | Description |
|---|--:|--:|---|
| Laboratory reference ranges | 46 | 44.2 | Minimum and maximum reference values accompanying laboratory results; handled as measurement attributes (e.g., range_low/range_high) during ETL |
| REDCap survey timestamps | 34 | 32.7 | Survey start and completion timestamps; REDCap system metadata rather than survey content |
| Specimen handling fields | 12 | 11.5 | Specimen collection and processing dates and handling notes |
| BCVA data-entry modifiers | 10 | 9.6 | Best-corrected visual acuity "not done" indicators and sphere sign (+/−) modifiers applied during ETL |
| REDCap administrative field | 1 | 1.0 | Survey-scheduling workflow flag |
| MoCA paper-administration flag | 1 | 1.0 | Indicator that the MoCA was administered on paper |
| **Total** | **104** | **100.0** | |

These 104 elements were designated for mapping but intentionally not assigned OMOP concepts; they were handled as attributes or metadata during ETL. Survey timestamps were assigned AI-READI custom concepts in the mapping file but are counted here because they are system metadata rather than survey content.

## C. Data elements with laterality recorded as a qualifier

| Assessment | Right (n) | Left (n) | Total | Qualifier concept |
|---|--:|--:|--:|---|
| Retinal imaging acquisitions | 66 | 66 | 132 | Eye |
| Best-corrected visual acuity | 6 | 6 | 12 | Eye |
| Contrast sensitivity (photopic and mesopic) | 6 | 6 | 12 | Eye |
| Monofilament foot sensation (felt/tested totals) | 2 | 2 | 4 | Foot |
| **Total** | **80** | **80** | **160** | |

Laterality was recorded with standard concepts: Right eye (45876703) and Left eye (45883829); Structure of right foot (4298982) and Structure of left foot (4320144). Site-level monofilament results additionally use AI-READI custom site qualifiers (concept IDs 2005200605–2005200624).

All counts were generated from the final mapping file using [`count_concept_map.sql`](https://github.com/AI-READI/DataElementMaps/blob/v1.0-tvst/manuscript-tvst2026/count_concept_map.sql) (manuscript-tvst2026/count_concept_map.sql in release v1.0-tvst; doi:[10.5281/zenodo.23375723](https://doi.org/10.5281/zenodo.23375723)). BCVA, best-corrected visual acuity; ETL, extract, transform, load; MoCA, Montreal Cognitive Assessment; SKOS, Simple Knowledge Organization System.
