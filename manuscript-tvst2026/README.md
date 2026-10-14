Manuscript Artifacts — TVST 2026

This folder contains the exact files used for the manuscript:

Hong S, et al. A Generalizable Framework for Mapping Survey, Vision Care, and Cognitive Assessment Data to the OMOP Common Data Model in AI-READI. Translational Vision Science & Technology. 2026 (under review).

The files here are a frozen snapshot that reproduces every number reported in the paper. The working (actively maintained) mapping lives in redCapDataDictionaryWithExtension/value-set-mapping-common/ and may change after publication. 
For the archived version cited in the paper, use release v1.0-tvst (Zenodo DOI: 10.5281/zenodo.23375723).

---

## Contents

| File | Description |
|---|---|
| `ai_readi_redcap_value_set_mapping_common.csv` | Final REDCap-to-OMOP value-set mapping used in the manuscript (2,004 rows; 26 columns). Field definitions: [value-set-mapping-common/README.md](../redCapDataDictionaryWithExtension/value-set-mapping-common/README.md). |
| `count_concept_map.sql` | Reproduces all counts in Table 2, the Results and the Abstract. DuckDB; runs locally on the CSV. |
| `count_concept_map_output.txt` | Output of `count_concept_map.sql` on the final mapping file. |
| `count_concept_map_databricks.sql` | Same counts for Databricks / Spark SQL; reads the CSV loaded as table `ai_readi_redcap_value_set_mapping_common`. |
| `validate_mapping_against__omop_vocabulary.sql` | Validates every standard target and qualifier concept against the OMOP Standardized Vocabularies (existence, standard status, validity, domain, vocabulary, concept code). Databricks / Spark SQL; requires vocabulary tables in schema `omop_vocab`. |
| `validation-count-mapping-concepts_databricks.ipynb` | Databricks notebook that runs the count and validation queries, with saved outputs. |
| `run_counts.py` | Runs `count_concept_map.sql` with the DuckDB Python package (no CLI needed). |
| `scripts/` | Supporting queries: OMOP vocabulary validation of AI-READI concepts, mapping-strategy counts, and the type 2 diabetes + BCVA example use-case query. |


Supplementary tables and figures:

| Folder | Contents |
|---|---|
| [`supplementary/`](supplementary/) | Supplementary Tables S1 (survey instruments and documentation) and S2 (mapping relationships, confidence, reasons for non-mapping, laterality), as PDF and Markdown |
| [`figures/`](figures/) | Figures 1–3 (PDF, PNG, TIFF) and the Figure 3 plotting script |
| [`source/`](source/) | Editable sources: Figure 2 Graphviz `.dot` file and the Supplementary Table S2 `.docx` |


Related artifacts elsewhere in this repository:

| Artifact | Location |
|---|---|
| SSSOM mapping set | [`redCapDataDictionaryWithExtension/sssom/`](../redCapDataDictionaryWithExtension/sssom/) |
| LinkML schema and data | [`redCapDataDictionaryWithExtension/linkml/`](../redCapDataDictionaryWithExtension/linkml/) |
| AI-READI custom vocabulary (OHDSI submission) | [`redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/`](../redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/) |
| REDCap survey forms (PDF) | [`redCapDataDictionaryWithExtension/survey_pdfs/`](../redCapDataDictionaryWithExtension/survey_pdfs/) |

---

## Versions

| Component | Version |
|---|---|
| OMOP CDM | v5.3.1 |
| OMOP Standardized Vocabularies (validation) | v5.0 27-AUG-25 |
| Repository release | `v1.0-tvst` |


|vocabulary_id|vocabulary_version|
|---|---|
|LOINC|LOINC 2.80|
|None|v5.0 27-AUG-25|
|OMOP Extension|OMOP Extension 20240716|
|PPI|Codebook Version 0.4.43 + COVID + MHWB + SDOH + PFH + BHP + EHH|
|SNOMED|2025-02-01 SNOMED CT International Edition; 2025-03-01 SNOMED CT US Edition; 2025-04-09 SNOMED CT UK Edition|
|UCUM|Version 1.8.2|
---

## Reproducing the counts

**Option A — DuckDB (local, no database needed)**

Install the DuckDB command-line tool ([duckdb.org/docs/installation](https://duckdb.org/docs/installation/)):

| OS | Install |
|---|---|
| Windows | `winget install DuckDB.cli` (then reopen your terminal) |
| macOS | `brew install duckdb` |
| Linux | `curl https://install.duckdb.org \| sh` |

Then, from this folder (Terminal, PowerShell or Git Bash):

```bash
duckdb < count_concept_map.sql
```

The script reads `ai_readi_redcap_value_set_mapping_common.csv` from the same folder.

*Python alternative (no CLI needed):*

```bash
pip install duckdb
python run_counts.py
```
**Option B — Databricks**

1. Load the CSV as table `ai_readi_redcap_value_set_mapping_common` (catalog/schema-qualify the name in the script if needed).
2. Run `count_concept_map_databricks.sql`.
3. With the OMOP vocabulary tables in schema `omop_vocab`, run `validate_mapping_against__omop_vocabulary.sql`.

### Counting rules

- **Designated for mapping:** `Map_to_OMOP = 'Yes'`
- **Mapped:** designated and `TARGET_CONCEPT_ID` populated
- **Custom (AI-READI) concept:** `TARGET_CONCEPT_ID` ≥ 2,000,000,000; **standard concept:** < 2,000,000,000
- **Excluded from mapped counts:** REDCap survey start/completion timestamps (custom concepts 2005200558 and 2005200559; n = 34). These are system metadata rather than survey content and are counted as designated but not mapped. Including them would yield 522 custom-mapped elements and 345 distinct custom concepts.
- **Not designated:** the 2,906 curated REDCap data elements minus the 2,004 rows in the mapping file.

### Expected results (Table 2)

| Category | Data elements, n (%) | Distinct concepts |
|---|---|---|
| Mapped to standard concepts | 1,412 (48.6) | 380 |
| — LOINC | 1,203 (41.4) | 283 |
| — SNOMED CT | 134 (4.6) | 68 |
| — UCUM | 69 (2.4) | 23 |
| — PPI | 5 (0.2) | 5 |
| — OMOP Extension | 1 (<0.1) | 1 |
| Mapped to AI-READI custom concepts | 488 (16.8) | 343 |
| — AIREADI | 389 (13.4) | 266 |
| — AIREADI-Vision | 69 (2.4) | 47 |
| — AIREADI-MOCA | 30 (1.0) | 30 |
| **Mapped total** | **1,900 (65.4)** | **723** |
| Designated but not mapped | 104 (3.6) | — |
| Not designated for OMOP mapping | 902 (31.0) | — |
| **Total curated elements** | **2,906 (100)** | |

Designated-but-not-mapped breakdown: laboratory reference ranges 46; survey timestamps 34; specimen-handling fields 12; BCVA not-done/sign modifiers 10; REDCap administrative 1; MoCA paper-administration flag 1.

Mapping relationships (standard concepts): exact match 1,174; close match 235; related match 3. Confidence: 1.0 = 1,327; 0.75 = 83; 0.5 = 2. All 488 custom mappings are exact match at confidence 1.0.

Laterality qualifiers: Right eye (45876703) 78; Left eye (45883829) 78; Structure of right foot (4298982) 2; Structure of left foot (4320144) 2.

All integrity checks in section 6 of the count scripts (6a–6d) return zero rows.

---

## How to cite

If you use these artifacts, please cite the manuscript above and the archived release:

```
AI-READI Survey Data Element Commons, release v1.0-tvst. Zenodo. https://doi.org/10.5281/zenodo.23375723
```

## License

MIT — see [LICENSE](../LICENSE).