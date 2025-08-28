# Validation Report

Generated on: 2025-08-28 10:24:03

## Data Sources

This report compares generated Google Sheets against manual Google Sheets:

- **Manual Sheets**: [template_4_adding_vocabulary-2](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit)
  - concept_manual worksheet
  - concept_relationship_manual worksheet
- **Generated Sheets**: [template_4_adding_vocabulary-2](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit)
  - concept_generated worksheet (from autogen.py)
  - concept_relationship_generated worksheet (from autogen.py)

## Summary

| Target | Manual Rows | Generated Rows | Matched Rows | Errors | Discrepancies |
|--------|-------------|----------------|--------------|--------|---------------|
| concept | 412 | 412 | 412 | 0 | 0 |
| concept_relationship | 412 | 412 | 412 | 0 | 22 |

## Concept Validation

- **Manual rows:** 412
- **Generated rows:** 412
- **Matched rows:** 412
- **Unmatched manual rows:** 0
- **Unmatched generated rows:** 0


## Concept_Relationship Validation

- **Manual rows:** 412
- **Generated rows:** 412
- **Matched rows:** 412
- **Unmatched manual rows:** 0
- **Unmatched generated rows:** 0

### Discrepancies (22 rows with other differences)

#### Column Match Rates

| Column | Matching | Total | Match Rate |
|--------|----------|-------|------------|
| temp standard | 400 | 412 | 97.1% |
| temp name | 403 | 412 | 97.8% |
| concept_code_2 | 411 | 412 | 99.8% |
| confidence | 412 | 412 | 100.0% |
| temp domain | 412 | 412 | 100.0% |
| concept_name | 412 | 412 | 100.0% |
| invalid_reason | 412 | 412 | 100.0% |
| relationship_id | 412 | 412 | 100.0% |
| relationship_valid_end_date | 412 | 412 | 100.0% |
| temp class | 412 | 412 | 100.0% |
| concept_id_2 | 412 | 412 | 100.0% |
| vocabulary_id_1 | 412 | 412 | 100.0% |
| concept_id_1 | 412 | 412 | 100.0% |
| mapping_source | 412 | 412 | 100.0% |
| predicate_id | 412 | 412 | 100.0% |
| mapping_tool | 412 | 412 | 100.0% |
| vocabulary_id_2 | 412 | 412 | 100.0% |
| relationship_valid_start_date | 412 | 412 | 100.0% |
| mapping_justification | 412 | 412 | 100.0% |

#### Discrepancy Summary

- 🔴 Manual values link to specific cells in manual Google Sheets
- 🔵 Generated values link to specific cells in generated Google Sheets
- Explanations in parentheses describe the type of difference

**temp standard**: 0 manual blanks, 12 generated blanks (out of 12 total differences)

**Whitespace/Case differences**: 1 instances across 1 columns
- 1 - 10 times (2005200262) - temp name: "1 - 10 " vs "1-10" (Only whitespace differences (spaces, tabs, or line breaks))


#### Substantive Content Differences (9 instances)

- **Doing daily or almost daily** (2005200317)
  - temp name: 🔴 [Doing daily or almost daily](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G217) vs 🔵 [Daily or almost daily](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=G217) (Content difference requiring review)
- **I HAVE some kind of health insurance** (2005200254)
  - temp name: 🔴 [I HAVE some kind of health insurance](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G158) vs 🔵 [Insurance](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=G158) (Content difference requiring review)
- **I do NOT have health insurance** (2005200253)
  - temp name: 🔴 [I do NOT have health insurance](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G157) vs 🔵 [Not Covered by Insurance](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=G157) (Content difference requiring review)
- **More than 20 years** (2005200211)
  - temp name: 🔴 [More than 20 years](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G133) vs 🔵 [Electronic cigarette smoker](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=G133) (Content difference requiring review)
- **Other heart issues (Examples: pacemaker, heart valve disease, open heart surgery)** (2005200627)
  - temp name: 🔴 [History of Problems with your heart or circulation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G412) vs 🔵 [History of Problems with your heart or circulation [PhenX]](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=G412) (Content difference requiring review)
- **Protocol Deviation** (2005200284)
  - temp name: 🔴 [Protocol Deviation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G186) vs 🔵 [Research administrative status](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=G186) (Content difference requiring review)
- **Red Blood Cells (RBC) - x10E6/µL** (2005200183)
  - temp name: 🔴 [RBC - Red blood cell count](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G115) vs 🔵 [Red blood cell count](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=G115) (Content difference requiring review)
- **Stroke** (2005200628)
  - temp name: 🔴 [History of Problems with your heart or circulation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G413) vs 🔵 [History of Problems with your heart or circulation [PhenX]](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=G413) (Content difference requiring review)
- **White Blood Cells (WBC) - x10E3/µL** (2005200182)
  - concept_code_2: 🔴 [767002](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K114) vs 🔵 [104128002](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=963371514#gid=963371514&range=K114) (Content difference requiring review)
