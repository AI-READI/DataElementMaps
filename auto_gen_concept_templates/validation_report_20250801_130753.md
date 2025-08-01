# Validation Report

Generated on: 2025-08-01 13:07:53

## Summary

| Target | Manual Rows | Generated Rows | Matched Rows | Match Rate |
|--------|-------------|----------------|--------------|------------|
| concept | 416 | 528 | 346 | 65.5% |
| concept_relationship | 434 | 528 | 346 | 65.5% |

## Concept Validation

- **Manual rows:** 416
- **Generated rows:** 528
- **Matched rows:** 346
- **Unmatched manual rows:** 70
- **Unmatched generated rows:** 3

### Column Match Rates

| Column | Matching | Total | Match Rate |
|--------|----------|-------|------------|
| domain_id | 346 | 346 | 100.0% |
| vocabulary_id | 345 | 346 | 99.7% |
| invalid_reason | 346 | 346 | 100.0% |
| v6_domain_id | 164 | 346 | 47.4% |
| concept_name | 346 | 346 | 100.0% |
| concept_id | 346 | 346 | 100.0% |
| concept_class_id | 345 | 346 | 99.7% |
| valid_start_date | 346 | 346 | 100.0% |
| valid_end_date | 346 | 346 | 100.0% |
| standard_concept | 0 | 346 | 0.0% |

### Unmatched Manual Rows (70)

- 2005200608
- 2005200586
- 2005200610
- 2005200623
- 2005200596
- 2005200595
- 2005200626
- 2005200562
- 2005200597
- 2005200584
- ... and 60 more

### Unmatched Generated Rows (3)

- 2005200152
- 2005200455
- 2005200153

### Row-by-Row Differences (346 rows with differences)

#### Row ID: 2005200061

| Column | Manual | Generated |
|--------|--------|----------|
| standard_concept |  | S |

#### Row ID: 2005200138

| Column | Manual | Generated |
|--------|--------|----------|
| standard_concept |  | S |

#### Row ID: 2005200221

| Column | Manual | Generated |
|--------|--------|----------|
| standard_concept |  | S |

#### Row ID: 2005200489

| Column | Manual | Generated |
|--------|--------|----------|
| v6_domain_id |  | survey_conduct |
| standard_concept |  | S |

#### Row ID: 2005200530

| Column | Manual | Generated |
|--------|--------|----------|
| standard_concept |  | S |

*... and 341 more rows with differences*


## Concept_Relationship Validation

- **Manual rows:** 434
- **Generated rows:** 528
- **Matched rows:** 346
- **Unmatched manual rows:** 71
- **Unmatched generated rows:** 3

### Column Match Rates

| Column | Matching | Total | Match Rate |
|--------|----------|-------|------------|
| vocabulary_id_2 | 341 | 346 | 98.6% |
| confidence | 280 | 346 | 80.9% |
| invalid_reason | 346 | 346 | 100.0% |
| predicate_id | 346 | 346 | 100.0% |
| Notes | 345 | 346 | 99.7% |
| relationship_valid_end_date | 346 | 346 | 100.0% |
| concept_id_2 | 92 | 346 | 26.6% |
| temp name | 331 | 346 | 95.7% |
| concept_code_2 | 337 | 346 | 97.4% |
| temp class | 341 | 346 | 98.6% |
| SRC_CODE | 220 | 346 | 63.6% |
| temp standard | 336 | 346 | 97.1% |
| concept_name | 345 | 346 | 99.7% |
| temp domain | 342 | 346 | 98.8% |
| mapping_justification | 346 | 346 | 100.0% |
| vocabulary_id_1 | 345 | 346 | 99.7% |
| relationship_valid_start_date | 346 | 346 | 100.0% |
| mapping_tool | 346 | 346 | 100.0% |
| relationship_id | 346 | 346 | 100.0% |
| mapping_source | 346 | 346 | 100.0% |
| concept_id_1 | 346 | 346 | 100.0% |

### Unmatched Manual Rows (71)

- 
- 2005200608
- 2005200586
- 2005200610
- 2005200623
- 2005200596
- 2005200595
- 2005200626
- 2005200562
- 2005200597
- ... and 61 more

### Unmatched Generated Rows (3)

- 2005200152
- 2005200455
- 2005200153

### Row-by-Row Differences (257 rows with differences)

#### Row ID: 2005200061

| Column | Manual | Generated |
|--------|--------|----------|
| concept_id_2 | 4025584 | 4025584.0 |

#### Row ID: 2005200138

| Column | Manual | Generated |
|--------|--------|----------|
| confidence | 1 | 1.0 |
| concept_id_2 | 4161694 | 4161694.0 |
| temp standard | N |  |

#### Row ID: 2005200221

| Column | Manual | Generated |
|--------|--------|----------|
| concept_id_2 | 45890999 | 45890999.0 |

#### Row ID: 2005200489

| Column | Manual | Generated |
|--------|--------|----------|
| concept_id_2 | 4256483 | 4256483.0 |

#### Row ID: 2005200350

| Column | Manual | Generated |
|--------|--------|----------|
| confidence | 1 | 1.0 |
| concept_id_2 | 606671 | 606671.0 |

*... and 252 more rows with differences*

