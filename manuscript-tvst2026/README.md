Manuscript Artifacts — TVST 2026

This folder contains the exact files used for the manuscript:

Hong S, et al. A Generalizable Framework for Mapping Survey, Vision Care, and Cognitive Assessment Data to the OMOP Common Data Model in AI-READI. Translational Vision Science & Technology. 2026 (under review).

The files here are a frozen snapshot that reproduces every number reported in the paper. The working (actively maintained) mapping lives in redCapDataDictionaryWithExtension/value-set-mapping-common/ and may change after publication. 
For the archived version cited in the paper, use release v1.0-tvst (Zenodo DOI: 10.5281/zenodo.XXXXXXX).

Contents

---

## Contents

| File | Description |
|---|---|
| `ai_readi_redcap_value_set_mapping_common.csv` | Final REDCap-to-OMOP value-set mapping used in the manuscript (2,004 rows; 26 columns). Field definitions: [value-set-mapping-common/README.md](../../redCapDataDictionaryWithExtension/value-set-mapping-common/README.md). |
| `count_mapping_concepts.sql` | Reproduces all counts in Table 2, the Results and the Abstract. DuckDB; runs locally on the CSV. |
| `count_mapping_concepts_databricks.sql` | Same counts for Databricks / Spark SQL; reads the CSV loaded as table `ai_readi_redcap_value_set_mapping_common`. |
| `validate_mapping_against_omop_vocabulary.sql` | Validates every standard target and qualifier concept against the OMOP Standardized Vocabularies (existence, standard status, validity, domain, vocabulary, concept code). Databricks / Spark SQL; requires vocabulary tables in schema `omop_vocab`. |

Related artifacts elsewhere in this repository:

| Artifact | Location |
|---|---|
| SSSOM mapping set | [`redCapDataDictionaryWithExtension/sssom/`](../../redCapDataDictionaryWithExtension/sssom/) |
| LinkML schema and data | [`redCapDataDictionaryWithExtension/linkml/`](../../redCapDataDictionaryWithExtension/linkml/) |
| AI-READI custom vocabulary (OHDSI submission) | [`redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/`](../../redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/) |
| REDCap survey forms (PDF) | [`redCapDataDictionaryWithExtension/survey_pdfs/`](../../redCapDataDictionaryWithExtension/survey_pdfs/) |

---

## Versions

| Component | Version |
|---|---|
| OMOP CDM | v5.3.1 |
| OMOP Standardized Vocabularies (validation) | v5.0 27-AUG-25 |
| Repository release | `v1.0-tvst` |

## Reproducing the counts

**Option A — DuckDB (local, no database needed)**

```bash
pip install duckdb
duckdb -c ".read count_mapping_concepts.sql"
--or
winget install DuckDB.cli
```

Run from this folder; the script reads `ai_readi_redcap_value_set_mapping_common.csv` directly.
```
   cd /c/path/to/DataElementMaps/manuscript/tvst-2026
   duckdb < count_mapping_concepts.sql
```

**Option B — Databricks**

1. Load the CSV as table `ai_readi_redcap_value_set_mapping_common` (catalog/schema-qualify the name in the script if needed).
2. Run `count_mapping_concepts_databricks.sql`.
3. With the OMOP vocabulary tables in schema `omop_vocab`, run `validate_mapping_against_vocabulary.sql`.

### Counting rules

- **Designated for mapping:** `Map_to_OMOP = 'Yes'`
- **Mapped:** designated and `TARGET_CONCEPT_ID` populated
- **Custom (AI-READI) concept:** `TARGET_CONCEPT_ID` ≥ 2,000,000,000; **standard concept:** < 2,000,000,000
- **Excluded from mapped counts:** REDCap survey start/completion timestamps (custom concepts 2005200558 and 2005200559; n = 34). These are system metadata rather than survey content and are counted as designated but not mapped. Including them would yield 521 custom-mapped elements and 344 distinct custom concepts.
- **Not designated:** the 2,906 curated REDCap data elements minus the 2,004 rows in the mapping file.


### Expected results (Table 2)

| Category | Data elements, n (%) | Distinct concepts |
|---|---|---|
| Mapped to standard concepts | 1,413 (48.6) | 381 |
| — LOINC | 1,200 (41.3) | 281 |
| — SNOMED CT | 138 (4.7) | 71 |
| — UCUM | 69 (2.4) | 23 |
| — PPI | 5 (0.2) | 5 |
| — OMOP Extension | 1 (<0.1) | 1 |
| Mapped to AI-READI custom concepts | 487 (16.8) | 342 |
| — AIREADI | 388 (13.4) | 265 |
| — AIREADI-Vision | 69 (2.4) | 47 |
| — AIREADI-MOCA | 30 (1.0) | 30 |
| **Mapped total** | **1,900 (65.4)** | **723** |
| Designated but not mapped | 104 (3.6) | — |
| Not designated for OMOP mapping | 902 (31.0) | — |
| **Total curated elements** | **2,906 (100)** | |

Designated-but-not-mapped breakdown: laboratory reference ranges 46; survey timestamps 34; specimen-handling fields 12; BCVA not-done/sign modifiers 10; REDCap administrative 1; MoCA paper-administration flag 1.

Mapping relationships (standard concepts): exact match 1,173; close match 237; related match 3. Confidence: 1.0 = 1,327; 0.75 = 84; 0.5 = 2. All 487 custom mappings are exact match at confidence 1.0.

Laterality qualifiers: Right eye (45876703) 78; Left eye (45883829) 78; Structure of right foot (4298982) 2; Structure of left foot (4320144) 2.

All integrity checks in section 6 of the count scripts return zero rows.

---

## How to cite

If you use these artifacts, please cite the manuscript above and the archived release:

```
AI-READI Survey Data Element Commons, release v1.0-tvst. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
```

## License

MIT — see [LICENSE](../../LICENSE).
