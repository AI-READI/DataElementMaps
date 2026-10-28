# Concept map v1.8.4: metrics

Counts for concept map **v1.8.4** (tag `v1.8.4`, 2026-10-28), from `redCapDataDictionaryWithExtension/scripts/count_concept_map.sql` run on the tagged mapping file (2,143 rows; MD5 `3041c810d90c87c7f686aa976b523e44`). Counting rules are in the header of that script.

## Headline numbers

| Measure | Value |
|---|---|
| Curated REDCap data elements | 2,906 |
| Mapped to OMOP | 2,005 (69.0%), 742 distinct concepts |
| Mapped to standard OMOP concepts | 1,519 (52.3%), 403 distinct concepts |
| Mapped to AI-READI custom concepts | 486 (16.7%), 339 distinct concepts |
| Designated for mapping but unmapped | 138 (4.7%) |
| Not designated for mapping | 763 (26.3%) |
| Standard mappings that are exact matches | 1,258 of 1,519 (82.8%) |
| Unit lookup | 114 keys (89 field, 25 unit text) |

## Release audit (audit_concept_map_report.md)

| Check | Result |
|---|---|
| A1 Custom targets match concept_manual.csv | 0 issues |
| A2 Same concept ID, conflicting name/domain/vocabulary/code | 0 issues |
| A3 Non-custom target not standard | 0 issues |
| A4 Predicate / confidence rules | 0 issues |
| A5 Duplicate keys (expected Yes -> condition/observation/procedure + value pairs) | 79 (expected) |
| A6 Stray spaces in key columns | 0 issues |
| A7 Custom concepts used as Condition targets | 2 (known: `mhoccur_circ`, `mhoccur_cvdot`) |
| A8 Answers with no question row | 3 (administrative fields, expected) |
| B1 / B2 review lists | 342 / 209 rows reviewed |
| C1 / C2 | 17 'Other' rows; 6 predicate/confidence combinations |

## Element summary

| category | n | pct_of_2906 | distinct_concepts |
|---|---|---|---|
| Standard | 1519 | 52.3 | 403 |
| Custom | 486 | 16.7 | 339 |
| Mapped total | 2005 | 69.0 | 742 |
| Designated but unmapped | 138 | 4.7 |  |
| Not designated | 763 | 26.3 |  |
| Total curated elements | 2906 | 100.0 |  |

## Mapped elements by vocabulary

| mapping_category | vocabulary | elements | distinct_concepts |
|---|---|---|---|
| Standard | LOINC | 1190 | 277 |
| Standard | SNOMED | 172 | 75 |
| Standard | UCUM | 132 | 40 |
| Standard | CPT4 | 12 | 1 |
| Standard | PPI | 8 | 7 |
| Standard | Ethnicity | 4 | 2 |
| Standard | OMOP Extension | 1 | 1 |
| Custom | AIREADI | 387 | 262 |
| Custom | AIREADI-Vision | 69 | 47 |
| Custom | AIREADI-MOCA | 30 | 30 |

## Designated but unmapped, by reason

| unmapped_reason | n |
|---|---|
| Laboratory reference range | 46 |
| REDCap survey timestamp | 34 |
| Superseded unit row | 20 |
| Specimen handling | 12 |
| BCVA not-done / sign modifier | 10 |
| Answer to an excluded question | 7 |
| No matching concept | 5 |
| Not collected (NRBC) | 2 |
| REDCap administrative | 1 |
| MoCA paper-administration flag | 1 |

## Predicate and confidence

| mapping_category | PREDICATE_ID | CONFIDENCE | n |
|---|---|---|---|
| Standard | skos:closeMatch | 1 | 170 |
| Standard | skos:closeMatch | 0.75 | 89 |
| Standard | skos:exactMatch | 1 | 1258 |
| Standard | skos:relatedMatch | 0.75 | 1 |
| Standard | skos:relatedMatch | 0.5 | 1 |
| Custom | skos:exactMatch | 1 | 486 |

## Qualifier (laterality / body site) concepts

| qualifier_concept_id | qualifier_source_value | n |
|---|---|---|
| 4298982 | Structure of right foot | 2 |
| 4320144 | Structure of left foot | 2 |
| 45876703 | Right eye | 78 |
| 45883829 | Left eye | 78 |
| 45888270 | Left eye | 22 |
| 45888271 | Right eye | 22 |
