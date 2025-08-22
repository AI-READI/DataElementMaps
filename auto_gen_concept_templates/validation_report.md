# Validation Report

Generated on: 2025-08-22 14:19:26

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
| concept | 416 | 638 | 413 | 0 | 413 |
| concept_relationship | 413 | 638 | 413 | 0 | 412 |

## Concept Validation

- **Manual rows:** 416
- **Generated rows:** 638
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
| concept_class_id | 0 | 413 | 0.0% |
| vocabulary_id | 0 | 413 | 0.0% |
| domain_id | 0 | 413 | 0.0% |
| concept_name | 412 | 413 | 99.8% |
| valid_end_date | 413 | 413 | 100.0% |
| valid_start_date | 413 | 413 | 100.0% |
| invalid_reason | 413 | 413 | 100.0% |
| standard_concept | 413 | 413 | 100.0% |
| concept_id | 413 | 413 | 100.0% |

#### All Discrepancies

**concept_class_id**: 0 manual blanks, 413 generated blanks (out of 413 total differences)

**vocabulary_id**: 0 manual blanks, 413 generated blanks (out of 413 total differences)

**domain_id**: 0 manual blanks, 413 generated blanks (out of 413 total differences)


- **Have you been diagnosed with any conditions not listed above? (any condition, not just eyes)** (2005200470)
  - concept_name: 🔴 [Have you been diagnosed with any conditions not listed above? (any condition, not just eyes)](https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917&range=A280) vs 🔵 [Have you been diagnosed with any conditions not listed above?](output/concept.csv#L331) (Content difference requiring review)

## Concept_Relationship Validation

- **Manual rows:** 413
- **Generated rows:** 638
- **Matched rows:** 413
- **Unmatched manual rows:** 0
- **Unmatched generated rows:** 0

### Discrepancies (412 rows with other differences)

#### Column Match Rates

| Column | Matching | Total | Match Rate |
|--------|----------|-------|------------|
| mapping_source | 1 | 413 | 0.2% |
| mapping_justification | 1 | 413 | 0.2% |
| predicate_id | 92 | 413 | 22.3% |
| confidence | 92 | 413 | 22.3% |
| temp name | 328 | 413 | 79.4% |
| temp standard | 331 | 413 | 80.1% |
| concept_code_2 | 332 | 413 | 80.4% |
| temp class | 336 | 413 | 81.4% |
| vocabulary_id_2 | 336 | 413 | 81.4% |
| temp domain | 337 | 413 | 81.6% |
| concept_id_1 | 413 | 413 | 100.0% |
| mapping_tool | 413 | 413 | 100.0% |
| relationship_valid_end_date | 413 | 413 | 100.0% |
| relationship_valid_start_date | 413 | 413 | 100.0% |
| relationship_id | 413 | 413 | 100.0% |
| concept_name | 413 | 413 | 100.0% |
| vocabulary_id_1 | 413 | 413 | 100.0% |
| concept_id_2 | 413 | 413 | 100.0% |
| invalid_reason | 413 | 413 | 100.0% |

#### All Discrepancies

**predicate_id**: 0 manual blanks, 321 generated blanks (out of 321 total differences)

**mapping_source**: 0 manual blanks, 412 generated blanks (out of 412 total differences)

**confidence**: 0 manual blanks, 321 generated blanks (out of 321 total differences)

**mapping_justification**: 0 manual blanks, 412 generated blanks (out of 412 total differences)

**temp name**: 0 manual blanks, 74 generated blanks (out of 85 total differences)

**concept_code_2**: 0 manual blanks, 74 generated blanks (out of 81 total differences)

**temp domain**: 0 manual blanks, 74 generated blanks (out of 76 total differences)

**temp class**: 0 manual blanks, 74 generated blanks (out of 77 total differences)

**temp standard**: 0 manual blanks, 82 generated blanks (out of 82 total differences)

**vocabulary_id_2**: 0 manual blanks, 74 generated blanks (out of 77 total differences)


