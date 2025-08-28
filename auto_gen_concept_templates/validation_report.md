# Validation Report

Generated on: 2025-08-28 11:12:31

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
| concept_relationship | 412 | 412 | 412 | 0 | 13 |

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

### Discrepancies (13 rows with other differences)

#### Column Match Rates

| Column | Matching | Total | Match Rate |
|--------|----------|-------|------------|
| temp standard | 400 | 412 | 97.1% |
| temp name | 411 | 412 | 99.8% |
| mapping_source | 412 | 412 | 100.0% |
| concept_id_1 | 412 | 412 | 100.0% |
| temp domain | 412 | 412 | 100.0% |
| mapping_tool | 412 | 412 | 100.0% |
| vocabulary_id_2 | 412 | 412 | 100.0% |
| predicate_id | 412 | 412 | 100.0% |
| concept_id_2 | 412 | 412 | 100.0% |
| relationship_valid_end_date | 412 | 412 | 100.0% |
| invalid_reason | 412 | 412 | 100.0% |
| concept_name | 412 | 412 | 100.0% |
| concept_code_2 | 412 | 412 | 100.0% |
| relationship_id | 412 | 412 | 100.0% |
| vocabulary_id_1 | 412 | 412 | 100.0% |
| relationship_valid_start_date | 412 | 412 | 100.0% |
| temp class | 412 | 412 | 100.0% |
| confidence | 412 | 412 | 100.0% |
| mapping_justification | 412 | 412 | 100.0% |

#### Discrepancy Summary

- 🔴 Manual values link to specific cells in manual Google Sheets
- 🔵 Generated values link to specific cells in generated Google Sheets
- Explanations in parentheses describe the type of difference

**temp standard**: 0 manual blanks, 12 generated blanks (out of 12 total differences)

**Whitespace/Case differences**: 1 instances across 1 columns
- 1 - 10 times (2005200262) - temp name: "1 - 10 " vs "1-10" (Only whitespace differences (spaces, tabs, or line breaks))


