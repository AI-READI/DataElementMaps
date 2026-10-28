# Concept map v1.8.4: release snapshot

Frozen reports for concept map **v1.8.4** (tag `v1.8.4`, commit `1beb536`, 2026-10-28), kept for citation (e.g. posters and papers). They are generated from the tagged files and are not updated afterwards; later releases get their own `releases/<version>/` folder.

| File | Contents | How it was made |
|---|---|---|
| `concept_map_metrics.md` | Element and concept counts: standard / custom / unmapped, by vocabulary, unmapped reasons, predicates and confidence, laterality qualifiers | `python redCapDataDictionaryWithExtension/scripts/run_counts.py` on tag `v1.8.4` |
| `audit_concept_map_report.md` | Release audit: structural checks A1-A8, review lists B1-B2, predicate conventions C1-C2 (line numbers refer to the v1.8.4 mapping CSV) | `python redCapDataDictionaryWithExtension/scripts/audit_concept_map.py --out ...` on tag `v1.8.4` |

## Files these reports describe

| File (v1.8.4) | Data rows | MD5 | Git blob |
|---|---|---|---|
| `value-set-mapping-common/_ai_readi_redcap_value_set_mapping_common.csv` | 2,143 | `3041c810d90c87c7f686aa976b523e44` | `d49e63030d12` |
| `value-set-mapping-common/_ai_readi_redcap_value_set_mapping_common_map2omop.csv` | 2,113 | `8d2ea4a1fcd22c06e0458caa1e18264b` | `8e933901db75` |
| `value-set-mapping-common/_ai_readi_redcap_value_set_mapping_map2omop_open_source_public_version.csv` | 1,998 | `39bc6cd0e9ee3c1807c58bb3ee5e32d3` | `92140ef492ff` |
| `sssom/ai_readi_redcap_value_set_mapping.sssom.tsv` | 2,068 | `a177a7c00bc1072f67721da15a1b91eb` | `3a194893ad0b` |
| `redcap-data-dictionary/_master_red_cap_data_dictionary_with_extensions.csv` | 3,150 | `12515f44aacc1acdb86ccbc1abc4d88b` | `f93508d5eea4` |
| `value-set-mapping-common/scripts/unit_concept_lookup.csv` | 114 | `38fa0b4598ee1551d12d5f8196f89ac6` | `eacb4dafcfbe` |
| `value-set-mapping-common/scripts/unit_concept_lookup_extended.csv` | 89 | `8a2979addf3233cc98411617f2839d89` | `88fc5f74abb7` |

Paths are under `redCapDataDictionaryWithExtension/`. MD5 is of the file as checked out; the git blob ID is what `git rev-parse v1.8.4:<path>` returns.

## Map version in the OMOP survey data

| OMOP survey build | Concept map used |
|---|---|
| Build checked 2026-10-28 | `v1.0-tvst` |
| Handoff to the ETL team for the next build | `v1.8.4` (files above) |
