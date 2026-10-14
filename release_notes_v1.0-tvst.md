Archived on Zenodo: https://doi.org/10.5281/zenodo.23375723

First archived release, accompanying the manuscript *"A Generalizable Framework for Mapping Survey, Vision Care, and Cognitive Assessment Data to the OMOP Common Data Model in AI-READI"* (Translational Vision Science & Technology, 2026).

**What's in this release**
- `manuscript-tvst2026/`: the frozen REDCap-to-OMOP mapping file (2,004 rows) used in the manuscript, frozen SSSOM and LinkML copies, count scripts that reproduce every number in the paper (`count_concept_map.sql`, `run_counts.py`), the OMOP vocabulary validation script, Figures 1–3 and Supplementary Tables S1–S2.
- AI-READI custom vocabularies (AIREADI, AIREADI-Vision, AIREADI-MOCA) submitted to the OHDSI Vocabulary Working Group.

**Key numbers (Table 2):** 2,906 curated elements; 1,900 mapped (65.4%): 1,412 to 380 standard concepts and 488 to 343 AI-READI custom concepts.

**Reproduce:** `cd manuscript-tvst2026 && pip install duckdb && python run_counts.py`

The working mapping in `redCapDataDictionaryWithExtension/value-set-mapping-common/` may change after this release. Use this tag for the version cited in the paper.

See `CHANGELOG.md` for the full list of changes.
