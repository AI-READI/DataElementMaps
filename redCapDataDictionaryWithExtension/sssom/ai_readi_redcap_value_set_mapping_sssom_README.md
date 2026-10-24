# AI-READI REDCap Value Set Mapping — SSSOM Representation

Generated from `_ai_readi_redcap_value_set_mapping_common.csv` with `generate_linkml_sssom.py`.

## Files

- `ai_readi_redcap_value_set_mapping.sssom.tsv` — SSSOM-style mapping table.
- `ai_readi_redcap_value_set_mapping.sssom.yaml` — SSSOM metadata file with CURIE prefixes.
- `ai_readi_redcap_value_set_mapping_sssom_incomplete_rows.csv` — rows not included in the SSSOM TSV because they were missing `TARGET_CONCEPT_ID` or `PREDICATE_ID`.

## Row counts

- Source rows: 2,127
- Rows included in SSSOM TSV: 2,051
- Rows excluded as incomplete for SSSOM: 76

## Identifier conventions

- `subject_id`: generated as `AIREADI_REDCAP:<FORM_NAME>.<SRC_CODE>[.<SRC_CODE_ID>]` when source codes were available. When source codes were missing, the generator used `FIELD_ID`, `FIELD_ID_NUM`, or the source row number.
- `object_id`: generated as `OMOP:<TARGET_CONCEPT_ID>`.
- `predicate_id`: taken directly from the source mapping file, such as `skos:exactMatch` or `skos:closeMatch`.
- `mapping_justification`: set to `semapv:ManualMappingCuration` for all included rows.

## Notes

The TSV includes both standard SSSOM columns and AI-READI/OMOP-specific extension columns such as `target_domain_id`, `target_vocabulary_id`, `value_as_concept_id`, and `qualifier_concept_id`. These extension columns preserve information needed for OMOP ETL and downstream review.

Row counts here are rows in the mapping file. Manuscript counts (e.g., 1,900 mapped elements) additionally exclude REDCap survey timestamps; see `manuscript-tvst2026/README.md`.
