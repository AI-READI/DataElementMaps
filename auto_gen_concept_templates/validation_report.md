# Validation Report

Generated on: 2025-08-25 18:50:23

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
| concept | 413 | 413 | 413 | 0 | 0 |
| concept_relationship | 413 | 413 | 413 | 0 | 40 |

## Concept Validation

- **Manual rows:** 413
- **Generated rows:** 413
- **Matched rows:** 413
- **Unmatched manual rows:** 0
- **Unmatched generated rows:** 0


## Concept_Relationship Validation

- **Manual rows:** 413
- **Generated rows:** 413
- **Matched rows:** 413
- **Unmatched manual rows:** 0
- **Unmatched generated rows:** 0

### Discrepancies (40 rows with other differences)

#### Column Match Rates

| Column | Matching | Total | Match Rate |
|--------|----------|-------|------------|
| temp standard | 389 | 413 | 94.2% |
| temp name | 399 | 413 | 96.6% |
| concept_code_2 | 406 | 413 | 98.3% |
| vocabulary_id_2 | 410 | 413 | 99.3% |
| temp class | 410 | 413 | 99.3% |
| temp domain | 411 | 413 | 99.5% |
| mapping_tool | 413 | 413 | 100.0% |
| predicate_id | 413 | 413 | 100.0% |
| relationship_valid_start_date | 413 | 413 | 100.0% |
| invalid_reason | 413 | 413 | 100.0% |
| vocabulary_id_1 | 413 | 413 | 100.0% |
| mapping_source | 413 | 413 | 100.0% |
| relationship_id | 413 | 413 | 100.0% |
| confidence | 413 | 413 | 100.0% |
| concept_id_1 | 413 | 413 | 100.0% |
| concept_name | 413 | 413 | 100.0% |
| mapping_justification | 413 | 413 | 100.0% |
| concept_id_2 | 413 | 413 | 100.0% |
| relationship_valid_end_date | 413 | 413 | 100.0% |

#### All Discrepancies

**temp standard**: 0 manual blanks, 12 generated blanks (out of 24 total differences)


- **1 - 10 times** (2005200262)
  - temp name: 🔴 [1 - 10 ](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G168) vs 🔵 [1-10](output/concept_relationship.csv#L166) (Content difference requiring review)
- **1 - 3 times** (2005200239)
  - concept_code_2: 🔴 [LA23695-2](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K145) vs 🔵 [LA15695-2](output/concept_relationship.csv#L143) (Content difference requiring review)
- **29 to 35** (2005200197)
  - concept_code_2: 🔴 [LA14679-7](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K121) vs 🔵 [LA15787-7](output/concept_relationship.csv#L119) (Content difference requiring review)
- **Activity monitor returned?** (2005200555)
  - concept_code_2: 🔴 [42528781](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K344) vs 🔵 [82611-5](output/concept_relationship.csv#L342) (Content difference requiring review)
- **Covered** (2005200252)
  - temp name: 🔴 [Covered](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G158) vs 🔵 [Insurance](output/concept_relationship.csv#L156) (Content difference requiring review)
- **Does not apply to my neighborhood** (2005200268)
  - concept_code_2: 🔴 [LA14452-9](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K174) vs 🔵 [LA16616-7](output/concept_relationship.csv#L172) (Content difference requiring review)
  - temp name: 🔴 [Does not apply](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G174) vs 🔵 [PEFR 1](output/concept_relationship.csv#L172) (Content difference requiring review)
- **Doing daily or almost daily** (2005200317)
  - temp name: 🔴 [Doing daily or almost daily](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G219) vs 🔵 [Daily or almost daily](output/concept_relationship.csv#L217) (Content difference requiring review)
- **I HAVE some kind of health insurance** (2005200254)
  - temp name: 🔴 [I HAVE some kind of health insurance](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G160) vs 🔵 [Insurance](output/concept_relationship.csv#L158) (Content difference requiring review)
- **I do NOT have health insurance** (2005200253)
  - temp name: 🔴 [I do NOT have health insurance](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G159) vs 🔵 [Not Covered by Insurance](output/concept_relationship.csv#L157) (Content difference requiring review)
- **More than 20 years** (2005200211)
  - temp name: 🔴 [More than 20 years](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G134) vs 🔵 [Electronic cigarette smoker](output/concept_relationship.csv#L132) (Content difference requiring review)
- **Other heart issues (Examples: pacemaker, heart valve disease, open heart surgery)** (2005200627)
  - temp name: 🔴 [History of Problems with your heart or circulation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G414) vs 🔵 [History of Problems with your heart or circulation [PhenX]](output/concept_relationship.csv#L412) (Content difference requiring review)
- **Protocol Deviation** (2005200284)
  - temp name: 🔴 [Protocol Deviation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G188) vs 🔵 [Research administrative status](output/concept_relationship.csv#L186) (Content difference requiring review)
- **Red Blood Cells (RBC) - x10E6/µL** (2005200183)
  - temp name: 🔴 [RBC - Red blood cell count](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G116) vs 🔵 [Red blood cell count](output/concept_relationship.csv#L114) (Content difference requiring review)
- **Stroke** (2005200628)
  - temp name: 🔴 [History of Problems with your heart or circulation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G415) vs 🔵 [History of Problems with your heart or circulation [PhenX]](output/concept_relationship.csv#L413) (Content difference requiring review)
- **There is MORE THAN ONE place** (2005200257)
  - concept_code_2: 🔴 [394777002](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K163) vs 🔵 [65123005](output/concept_relationship.csv#L161) (Content difference requiring review)
  - temp class: 🔴 [Answer](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=J163) vs 🔵 [Substance](output/concept_relationship.csv#L161) (Content difference requiring review)
  - temp domain: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=H163) vs 🔵 [Drug](output/concept_relationship.csv#L161) (Content difference requiring review)
  - temp name: 🔴 [There is MORE THAN ONE place](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G163) vs 🔵 [Choline](output/concept_relationship.csv#L161) (Content difference requiring review)
  - vocabulary_id_2: 🔴 [SNOMED ](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=I163) vs 🔵 [Nebraska Lexicon](output/concept_relationship.csv#L161) (Content difference requiring review)
- **There is NO place** (2005200256)
  - temp class: 🔴 [Answer](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=J162) vs 🔵 [Location](output/concept_relationship.csv#L160) (Content difference requiring review)
  - temp domain: 🔴 [Observation](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=H162) vs 🔵 [Place of Service](output/concept_relationship.csv#L160) (Content difference requiring review)
  - temp name: 🔴 [There is NO place](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G162) vs 🔵 [Health encounter sites](output/concept_relationship.csv#L160) (Content difference requiring review)
  - vocabulary_id_2: 🔴 [SNOMED ](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=I162) vs 🔵 [Nebraska Lexicon](output/concept_relationship.csv#L160) (Content difference requiring review)
- **When you used marijuana, approximately how many days in a typical week would you use it?** (2005200039)
  - concept_code_2: 🔴 [1333013](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K28) vs 🔵 [733460004](output/concept_relationship.csv#L26) (Content difference requiring review)
  - temp class: 🔴 [Question](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=J28) vs 🔵 [Clinical Finding](output/concept_relationship.csv#L26) (Content difference requiring review)
  - temp name: 🔴 [How often did you use cannabis?](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=G28) vs 🔵 [Marijuana user](output/concept_relationship.csv#L26) (Content difference requiring review)
  - vocabulary_id_2: 🔴 [PPI](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=I28) vs 🔵 [SNOMED](output/concept_relationship.csv#L26) (Content difference requiring review)
- **White Blood Cells (WBC) - x10E3/µL** (2005200182)
  - concept_code_2: 🔴 [767002](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125&range=K115) vs 🔵 [104128002](output/concept_relationship.csv#L113) (Content difference requiring review)
