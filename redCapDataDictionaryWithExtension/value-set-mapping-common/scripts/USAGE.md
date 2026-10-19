# Unit lookup: usage

How to fill `MEASUREMENT.unit_concept_id` from the AI-READI concept map: create one lookup table, add one LEFT JOIN, check. All scripts are Databricks / Spark SQL and can be copied as they are.

## Step 1. Create the unit_lookup table (choose one)

**Option A: load the ready-made file (simplest).** `unit_concept_lookup.csv` (in this folder) is the complete lookup table, 110 rows:

| Column | Meaning |
|---|---|
| `key_type` | `field` (lookup by measurement field name) or `string` (lookup by unit text) |
| `lookup_key` | the field name (e.g. `lbscat_rbc`) or the unit text (e.g. `mEq/L`) |
| `unit_concept_id` | the OMOP unit concept (e.g. 8815) |
| `unit_source_value` | the unit text (e.g. `x10E6/µL`) |

Upload it, set the path in `01a_load_unit_concept_lookup_csv.sql`, and run it. This creates the table `unit_lookup`. Or load the CSV with any tool you prefer into a table named `unit_lookup` with these four columns (`unit_concept_id` as an integer, file encoding UTF-8).

**Option B: build it from the concept map.** Run `00_load_concept_map.sql` (set the path to `_ai_readi_redcap_value_set_mapping_common.csv`), then `01_create_unit_lookup.sql`, one query. The result is identical to the CSV.

| key_type | lookup_key | Rows | Example |
|---|---|---|---|
| `field` | measurement field name | 85 | `lbscat_rbc` → 8815 (`x10E6/µL`) |
| `string` | unit text | 25 | `mEq/L` → 9557 |

Each key appears once.

## Step 2. Review (optional)

Run `02_view_unit_lookup.sql`: counts, both lists, and a duplicate check that must return 0 rows.

## Step 3. Add the LEFT JOIN to the measurement ETL

Copy the query in `03_left_join_unit_lookup_template.sql` and replace the placeholders:

```sql
SELECT m.*,
       COALESCE(f.unit_concept_id, u.unit_concept_id, 0)   AS unit_concept_id,
       COALESCE(f.unit_source_value, m.<unit_text_column>) AS unit_source_value
FROM <your_measurement_table> m
LEFT JOIN unit_lookup f
       ON f.key_type = 'field'  AND f.lookup_key = TRIM(m.<field_name_column>)
LEFT JOIN unit_lookup u
       ON u.key_type = 'string' AND u.lookup_key = TRIM(m.<unit_text_column>);
```

| Placeholder | Meaning | Example |
|---|---|---|
| `<your_measurement_table>` | your measurement or staging table | `staging.measurement` |
| `<field_name_column>` | the REDCap field name | `lbscat_rbc` |
| `<unit_text_column>` | the unit text on the record, if any (can be NULL) | `mEq/L` |

How it decides: the unit for the field first; if the field is not in `unit_lookup`, the unit text on the record; otherwise 0 (OMOP: no matching concept). `unit_source_value` is the unit text that goes with the concept chosen.

`04_example_omop_survey_measurement.sql` is the same join, ready to run on `omop_survey.measurement`, where the field name is the text before the first comma of `measurement_source_value`:
```sql
f.lookup_key = TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))
```

## Step 4. Check

| Script | Check | Expected |
|---|---|---|
| `05_check_no_fanout.sql` | Row count before and after the join; measurements that appear twice | Equal counts; 0 rows |
| `06_check_units_after_etl.sql` | After the ETL re-run: units on CBC, globulin, bilirubin, physical assessment, potassium; all measurements still without a unit | No `unit_concept_id` = 0 in the first list; only unitless vision scores and ratios in the second |

## Example result

| Field | Unit text on record | unit_concept_id | unit_source_value |
|---|---|---|---|
| lbscat_rbc | (none) | 8815 | x10E6/µL |
| import_globulin_total_norc | N/A | 8713 | g/dL |
| import_potassium | mEq/L | 9557 | mEq/L |
| import_potassium | (none) | 9557 | mEq/L |
| import_ldl_cholesterol_calculation | mg/dL | 8840 | mg/dL |
| height_vsorres | (none) | 8582 | cm |
| another field | x10E3/µL | 8848 | x10E3/µL |
| naming (MoCA score) | (none) | 44777566 | score |
| naming_time (MoCA time) | (none) | 8555 | s |

9 rows in, 9 rows out.

## Good to know

- **Why a lookup table and not a join to the concept map:** the same unit text sits in several Unit rows of the concept map (for example `g/dL` in 6 rows). Joining measurements to all of them on `SRC_CODE` multiplies the measurement rows. `unit_lookup` has one row per key.
- **Exact text:** `x10E3/µL` and `x10E6/µL` use the micro sign µ (U+00B5). If your data uses the Greek letter μ (U+03BC), use `REPLACE(TRIM(m.<unit_text_column>), 'μ', 'µ')` in the second join.
- **Missing values:** text such as "NA", "N/A" or "nan" in the unit column does not match anything, so those records get the field's unit (or 0). It is still best to load missing values as NULL.
- **LDL:** the field `import_ldl_cholesterol_calculation` has its unit in the REDCap field `import_ldl_cholesterol_u`; `unit_lookup` includes this pair.
- **MoCA:** score fields get 44777566 (score) and time fields 8555 (second).
- **After a new concept map release:** reload the new `unit_concept_lookup.csv` (option A) or rerun `01_create_unit_lookup.sql` (option B). The CSV is regenerated with every release.

## Medication route (DRUG_EXPOSURE.route_concept_id)

Same pattern, for the protected medication route question `cmroute`:

1. Create the table `medication_route_lookup`: load `medication_route_lookup.csv` with `07a_load_medication_route_lookup_csv.sql` (option A), or build it from the concept map with `07_create_medication_route_lookup.sql` (option B). 26 rows: 13 by answer code, 13 by answer label.
2. Add the LEFT JOIN from `08_left_join_medication_route_template.sql` to the drug exposure step, with your answer-code column and/or answer-label column.

| Answer | route_concept_id |
|---|---|
| 1 Intralesional | 4157758 |
| 2 Intramuscular | 4302612 |
| 3 Intraocular | 4157760 |
| 4 Intraperitoneal | 4243022 |
| 5 Nasal | 4262914 |
| 6 Oral | 4132161 |
| 7 Rectal | 4290759 |
| 8 Inhalation | 40486069 (Respiratory tract) |
| 9 Subcutaneous | 4142048 |
| 10 Topical | 4263689 |
| 11 Transdermal | 4262099 |
| 12 Vaginal | 4057765 |
| 888 Other | 0 |
