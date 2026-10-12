# Deprecated mapping files

These files are earlier versions of the AI-READI REDCap-to-OMOP value-set mapping.
They are kept for provenance only and should not be used.
These files and folders are **superseded** and retained only for provenance (version history of the AI-READI survey-to-OMOP mappings). They are no longer maintained and should not be used for new work.

| File | Notes |
|---|---|
| aireadi2omop_redcap_valueset_mapping_23Apr2024.csv | Snapshot of 23 Apr 2024 |
| aireadi2omop_redcap_valueset_mapping_2558.csv | Earlier version (2,558 rows) |
| aireadi2omop_redcap_valueset_mapping.csv | Earlier working version |



# Use instead:

| Need | Current location |
|---|---|
| Working value-set mapping | [`redCapDataDictionaryWithExtension/value-set-mapping-common/`](../redCapDataDictionaryWithExtension/value-set-mapping-common/) |
| Mapping used in the TVST 2026 manuscript (frozen) | [`manuscript-tvst2026/`](../manuscript-tvst2026/) |
| AI-READI custom vocabulary (OHDSI submission) | [`redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/`](../redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/) |


**Current working mapping version in the** redCapDataDictionaryWithExtension/value-set-mapping-common/

**Version used in the TVST 2026 manuscript:** manuscript/tvst-2026/


**Old Contents, no longer used**

| Folder | Formerly at | Description |
|---|---|---|
| `top-level-csvs/` | repository root | Early combined REDCap value-set mapping exports (2024) |
| `valuset-mappings/` | `valuset-mappings/` | Value-set mapping and extension-mapping snapshots (April–May 2024) |
| `mappings-csv/` | `mappings-csv/` | Dated working versions of the REDCap, Labs, Vision, MoCA and timestamp mappings (2023–2025) |
| `Custom_Concepts_Review/` | `Custom_Concepts_Review/` | Custom concept review lists (2025), superseded by the OHDSI vocabulary request files |
| `auto_gen_concept_templates/` | `auto_gen_concept_templates/` | Earlier script for generating custom concept templates |

Full history of each file is preserved in git (`git log --follow <file>`).

## Questions

These files are retained for provenance only and are no longer maintained.
For questions, please [open an issue](https://github.com/AI-READI/DataElementMaps/issues)
and reference the file name.

