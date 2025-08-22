# Validation Report

Generated on: 2025-08-21 20:34:21

## Data Sources

This report compares generated CSV files against manual Google Sheets:

- **Manual Sheets**: [template_4_adding_vocabulary-2](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY)
  - concept_manual worksheet
  - concept_relationship_manual worksheet
- **Generated Files**: 
  - `output/concept.csv` (from autogen.py)
  - `output/concept_relationship.csv` (from autogen.py)

### Link Legend
- 🔴 Manual values link to specific cells in Google Sheets
- 🔵 Generated values link to line numbers in CSV files
- Explanations in parentheses describe the type of difference

## Summary

| Target | Manual Rows | Generated Rows | Matched Rows | Errors | Discrepancies |
|--------|-------------|----------------|--------------|--------|---------------|
| concept | 416 | 413 | 413 | 0 | 413 |
| concept_relationship | 416 | 413 | 413 | 0 | 42 |

## Concept Validation

- **Manual rows:** 416
- **Generated rows:** 413
- **Matched rows:** 413
- **Unmatched manual rows:** 3
- **Unmatched generated rows:** 0

### Unmatched Manual Concepts (3)

| Concept ID | Concept Name |
|------------|--------------|
| [2005200236](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=A145) | Date device received back from participant |
| [2005200560](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=A350) | Survey Date |
| [2005200193](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=A118) | What was the study discontinuation or completion date? |

### Discrepancies (413 rows with other differences)

#### Column Match Rates

| Column | Matching | Total | Match Rate |
|--------|----------|-------|------------|
| standard_concept | 0 | 413 | 0.0% |
| concept_class_id | 384 | 413 | 93.0% |
| domain_id | 393 | 413 | 95.2% |
| concept_name | 413 | 413 | 100.0% |
| invalid_reason | 413 | 413 | 100.0% |
| valid_end_date | 413 | 413 | 100.0% |
| valid_start_date | 413 | 413 | 100.0% |
| vocabulary_id | 413 | 413 | 100.0% |
| concept_id | 413 | 413 | 100.0% |

#### All Discrepancies

**standard_concept**: 413 manual blanks, 0 generated blanks (out of 413 total differences)


- **Animal name recall task score** (2005200350)
  - concept_class_id: 🔴 [Assessment Item](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G251) vs 🔵 [Observable Entity](output/concept.csv#L8) (Content difference requiring review)
- **Left foot - site 1** (2005200615)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G405) vs 🔵 [Procedure](output/concept.csv#L359) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E405) vs 🔵 [Procedure](output/concept.csv#L359) (Content difference requiring review)
- **Left foot - site 10** (2005200624)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G414) vs 🔵 [Procedure](output/concept.csv#L368) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E414) vs 🔵 [Procedure](output/concept.csv#L368) (Content difference requiring review)
- **Left foot - site 2** (2005200616)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G406) vs 🔵 [Procedure](output/concept.csv#L360) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E406) vs 🔵 [Procedure](output/concept.csv#L360) (Content difference requiring review)
- **Left foot - site 3** (2005200617)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G407) vs 🔵 [Procedure](output/concept.csv#L361) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E407) vs 🔵 [Procedure](output/concept.csv#L361) (Content difference requiring review)
- **Left foot - site 4** (2005200618)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G408) vs 🔵 [Procedure](output/concept.csv#L362) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E408) vs 🔵 [Procedure](output/concept.csv#L362) (Content difference requiring review)
- **Left foot - site 5** (2005200619)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G409) vs 🔵 [Procedure](output/concept.csv#L363) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E409) vs 🔵 [Procedure](output/concept.csv#L363) (Content difference requiring review)
- **Left foot - site 6** (2005200620)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G410) vs 🔵 [Procedure](output/concept.csv#L364) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E410) vs 🔵 [Procedure](output/concept.csv#L364) (Content difference requiring review)
- **Left foot - site 7** (2005200621)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G411) vs 🔵 [Procedure](output/concept.csv#L365) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E411) vs 🔵 [Procedure](output/concept.csv#L365) (Content difference requiring review)
- **Left foot - site 8** (2005200622)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G412) vs 🔵 [Procedure](output/concept.csv#L366) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E412) vs 🔵 [Procedure](output/concept.csv#L366) (Content difference requiring review)
- **Left foot - site 9** (2005200623)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G413) vs 🔵 [Procedure](output/concept.csv#L367) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E413) vs 🔵 [Procedure](output/concept.csv#L367) (Content difference requiring review)
- **PhenX Education Attainment Survey** (2005200577)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G367) vs 🔵 [Survey](output/concept.csv#L403) (Content difference requiring review)
- **PhenX English Proficiency Survey** (2005200576)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G366) vs 🔵 [Survey](output/concept.csv#L402) (Content difference requiring review)
- **PhenX Health Care Access Survey** (2005200582)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G372) vs 🔵 [Survey](output/concept.csv#L408) (Content difference requiring review)
- **PhenX Health Insurance Survey** (2005200581)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G371) vs 🔵 [Survey](output/concept.csv#L407) (Content difference requiring review)
- **PhenX Healthcare Discrimination Survey** (2005200583)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G373) vs 🔵 [Survey](output/concept.csv#L409) (Content difference requiring review)
- **PhenX Housing Insecurity Survey** (2005200579)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G369) vs 🔵 [Survey](output/concept.csv#L405) (Content difference requiring review)
- **PhenX Job Security Survey** (2005200578)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G368) vs 🔵 [Survey](output/concept.csv#L404) (Content difference requiring review)
- **PhenX Prescriptions Affordability Survey** (2005200580)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G370) vs 🔵 [Survey](output/concept.csv#L406) (Content difference requiring review)
- **Right foot - site 1** (2005200605)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G395) vs 🔵 [Procedure](output/concept.csv#L349) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E395) vs 🔵 [Procedure](output/concept.csv#L349) (Content difference requiring review)
- **Right foot - site 10** (2005200614)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G404) vs 🔵 [Procedure](output/concept.csv#L358) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E404) vs 🔵 [Procedure](output/concept.csv#L358) (Content difference requiring review)
- **Right foot - site 2** (2005200606)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G396) vs 🔵 [Procedure](output/concept.csv#L350) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E396) vs 🔵 [Procedure](output/concept.csv#L350) (Content difference requiring review)
- **Right foot - site 3** (2005200607)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G397) vs 🔵 [Procedure](output/concept.csv#L351) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E397) vs 🔵 [Procedure](output/concept.csv#L351) (Content difference requiring review)
- **Right foot - site 4** (2005200608)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G398) vs 🔵 [Procedure](output/concept.csv#L352) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E398) vs 🔵 [Procedure](output/concept.csv#L352) (Content difference requiring review)
- **Right foot - site 5** (2005200609)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G399) vs 🔵 [Procedure](output/concept.csv#L353) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E399) vs 🔵 [Procedure](output/concept.csv#L353) (Content difference requiring review)
- **Right foot - site 6** (2005200610)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G400) vs 🔵 [Procedure](output/concept.csv#L354) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E400) vs 🔵 [Procedure](output/concept.csv#L354) (Content difference requiring review)
- **Right foot - site 7** (2005200611)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G401) vs 🔵 [Procedure](output/concept.csv#L355) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E401) vs 🔵 [Procedure](output/concept.csv#L355) (Content difference requiring review)
- **Right foot - site 8** (2005200612)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G402) vs 🔵 [Procedure](output/concept.csv#L356) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E402) vs 🔵 [Procedure](output/concept.csv#L356) (Content difference requiring review)
- **Right foot - site 9** (2005200613)
  - concept_class_id: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=G403) vs 🔵 [Procedure](output/concept.csv#L357) (Content difference requiring review)
  - domain_id: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=E403) vs 🔵 [Procedure](output/concept.csv#L357) (Content difference requiring review)

## Concept_Relationship Validation

- **Manual rows:** 416
- **Generated rows:** 413
- **Matched rows:** 413
- **Unmatched manual rows:** 3
- **Unmatched generated rows:** 0

### Unmatched Manual Concepts (3)

| Concept ID | Concept Name |
|------------|--------------|
| [2005200236](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=A145) | Date device received back from participant |
| [2005200560](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=A350) | Survey Date |
| [2005200193](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=A118) | What was the study discontinuation or completion date? |

### Discrepancies (42 rows with other differences)

#### Column Match Rates

| Column | Matching | Total | Match Rate |
|--------|----------|-------|------------|
| temp standard | 387 | 413 | 93.7% |
| temp name | 398 | 413 | 96.4% |
| concept_code_2 | 404 | 413 | 97.8% |
| temp class | 408 | 413 | 98.8% |
| vocabulary_id_2 | 408 | 413 | 98.8% |
| temp domain | 409 | 413 | 99.0% |
| concept_name | 412 | 413 | 99.8% |
| mapping_justification | 413 | 413 | 100.0% |
| predicate_id | 413 | 413 | 100.0% |
| relationship_valid_start_date | 413 | 413 | 100.0% |
| relationship_id | 413 | 413 | 100.0% |
| relationship_valid_end_date | 413 | 413 | 100.0% |
| mapping_source | 413 | 413 | 100.0% |
| mapping_tool | 413 | 413 | 100.0% |
| vocabulary_id_1 | 413 | 413 | 100.0% |
| invalid_reason | 413 | 413 | 100.0% |
| confidence | 413 | 413 | 100.0% |
| concept_id_1 | 413 | 413 | 100.0% |
| concept_id_2 | 413 | 413 | 100.0% |

#### All Discrepancies

**temp standard**: 0 manual blanks, 14 generated blanks (out of 26 total differences)


- **1 - 10 times** (2005200262)
  - temp name: 🔴 [1 - 10 ](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G170) vs 🔵 [1-10](output/concept_relationship.csv#L334) (Content difference requiring review)
- **1 - 3 times** (2005200239)
  - concept_code_2: 🔴 [LA23695-2](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K147) vs 🔵 [LA15695-2](output/concept_relationship.csv#L271) (Content difference requiring review)
- **29 to 35** (2005200197)
  - concept_code_2: 🔴 [LA14679-7](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K122) vs 🔵 [LA15787-7](output/concept_relationship.csv#L343) (Content difference requiring review)
- **Activity monitor returned?** (2005200555)
  - concept_code_2: 🔴 [42528781](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K346) vs 🔵 [82611-5](output/concept_relationship.csv#L95) (Content difference requiring review)
- **Covered** (2005200252)
  - temp name: 🔴 [Covered](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G160) vs 🔵 [Insurance](output/concept_relationship.csv#L327) (Content difference requiring review)
- **Does not apply to my neighborhood** (2005200268)
  - concept_code_2: 🔴 [LA14452-9](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K176) vs 🔵 [LA16616-7](output/concept_relationship.csv#L316) (Content difference requiring review)
  - temp name: 🔴 [Does not apply](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G176) vs 🔵 [PEFR 1](output/concept_relationship.csv#L316) (Content difference requiring review)
- **Doing daily or almost daily** (2005200317)
  - temp name: 🔴 [Doing daily or almost daily](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G221) vs 🔵 [Daily or almost daily](output/concept_relationship.csv#L252) (Content difference requiring review)
- **Have you been diagnosed with any conditions not listed above?** (2005200470)
  - concept_name: 🔴 [Have you been diagnosed with any conditions not listed above?](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=A280) vs 🔵 [Have you been diagnosed with any conditions not listed above? (any condition, not just eyes)](output/concept_relationship.csv#L231) (Content difference requiring review)
- **I HAVE some kind of health insurance** (2005200254)
  - temp name: 🔴 [I HAVE some kind of health insurance](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G162) vs 🔵 [Insurance](output/concept_relationship.csv#L329) (Content difference requiring review)
- **I do NOT have health insurance** (2005200253)
  - temp name: 🔴 [I do NOT have health insurance](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G161) vs 🔵 [Not Covered by Insurance](output/concept_relationship.csv#L328) (Content difference requiring review)
- **Less than 30 minutes daily less than 3 days a week** (2005200313)
  - concept_code_2: 🔴 [27789000](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K217) vs 🔵 [blank](output/concept_relationship.csv#L96) (Value missing in generated file)
  - temp class: 🔴 [Qualifier Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=J217) vs 🔵 [blank](output/concept_relationship.csv#L96) (Value missing in generated file)
  - temp domain: 🔴 [Meas Value](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=H217) vs 🔵 [blank](output/concept_relationship.csv#L96) (Value missing in generated file)
  - temp name: 🔴 [Infrequent](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G217) vs 🔵 [blank](output/concept_relationship.csv#L96) (Value missing in generated file)
  - vocabulary_id_2: 🔴 [SNOMED ](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=I217) vs 🔵 [blank](output/concept_relationship.csv#L96) (Value missing in generated file)
- **More than 20 years** (2005200211)
  - temp name: 🔴 [More than 20 years](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G135) vs 🔵 [Electronic cigarette smoker](output/concept_relationship.csv#L115) (Content difference requiring review)
- **Other heart issues (Examples: pacemaker, heart valve disease, open heart surgery)** (2005200627)
  - temp name: 🔴 [History of Problems with your heart or circulation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G417) vs 🔵 [History of Problems with your heart or circulation [PhenX]](output/concept_relationship.csv#L83) (Content difference requiring review)
- **Protocol Deviation** (2005200284)
  - concept_code_2: 🔴 [309032007](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K190) vs 🔵 [blank](output/concept_relationship.csv#L280) (Value missing in generated file)
  - temp class: 🔴 [Clinical Finding](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=J190) vs 🔵 [blank](output/concept_relationship.csv#L280) (Value missing in generated file)
  - temp domain: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=H190) vs 🔵 [blank](output/concept_relationship.csv#L280) (Value missing in generated file)
  - temp name: 🔴 [Protocol Deviation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G190) vs 🔵 [blank](output/concept_relationship.csv#L280) (Value missing in generated file)
  - vocabulary_id_2: 🔴 [SNOMED ](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=I190) vs 🔵 [blank](output/concept_relationship.csv#L280) (Value missing in generated file)
- **Red Blood Cells (RBC) - x10E6/µL** (2005200183)
  - temp name: 🔴 [RBC - Red blood cell count](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G116) vs 🔵 [Red blood cell count](output/concept_relationship.csv#L289) (Content difference requiring review)
- **Stroke** (2005200628)
  - temp name: 🔴 [History of Problems with your heart or circulation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G418) vs 🔵 [History of Problems with your heart or circulation [PhenX]](output/concept_relationship.csv#L84) (Content difference requiring review)
- **There is MORE THAN ONE place** (2005200257)
  - concept_code_2: 🔴 [394777002](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K165) vs 🔵 [65123005](output/concept_relationship.csv#L111) (Content difference requiring review)
  - temp class: 🔴 [Answer](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=J165) vs 🔵 [Substance](output/concept_relationship.csv#L111) (Content difference requiring review)
  - temp domain: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=H165) vs 🔵 [Drug](output/concept_relationship.csv#L111) (Content difference requiring review)
  - temp name: 🔴 [There is MORE THAN ONE place](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G165) vs 🔵 [Choline](output/concept_relationship.csv#L111) (Content difference requiring review)
  - vocabulary_id_2: 🔴 [SNOMED ](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=I165) vs 🔵 [Nebraska Lexicon](output/concept_relationship.csv#L111) (Content difference requiring review)
- **There is NO place** (2005200256)
  - temp class: 🔴 [Answer](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=J164) vs 🔵 [Location](output/concept_relationship.csv#L110) (Content difference requiring review)
  - temp domain: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=H164) vs 🔵 [Place of Service](output/concept_relationship.csv#L110) (Content difference requiring review)
  - temp name: 🔴 [There is NO place](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G164) vs 🔵 [Health encounter sites](output/concept_relationship.csv#L110) (Content difference requiring review)
  - vocabulary_id_2: 🔴 [SNOMED ](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=I164) vs 🔵 [Nebraska Lexicon](output/concept_relationship.csv#L110) (Content difference requiring review)
- **When you used marijuana, approximately how many days in a typical week would you use it?** (2005200039)
  - concept_code_2: 🔴 [1333013](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K28) vs 🔵 [733460004](output/concept_relationship.csv#L226) (Content difference requiring review)
  - temp class: 🔴 [Question](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=J28) vs 🔵 [Clinical Finding](output/concept_relationship.csv#L226) (Content difference requiring review)
  - temp name: 🔴 [How often did you use cannabis?](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G28) vs 🔵 [Marijuana user](output/concept_relationship.csv#L226) (Content difference requiring review)
  - vocabulary_id_2: 🔴 [PPI](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=I28) vs 🔵 [SNOMED](output/concept_relationship.csv#L226) (Content difference requiring review)
- **White Blood Cells (WBC) - x10E3/µL** (2005200182)
  - concept_code_2: 🔴 [767002](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K115) vs 🔵 [104128002](output/concept_relationship.csv#L288) (Content difference requiring review)
