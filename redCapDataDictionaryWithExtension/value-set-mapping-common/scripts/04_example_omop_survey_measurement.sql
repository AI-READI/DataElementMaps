-- =============================================================================
-- 04_example_omop_survey_measurement.sql
-- AI-READI concept map: example of the LEFT JOIN on omop_survey.measurement
--
-- In omop_survey.measurement the field name is the text before the first comma of
-- measurement_source_value, e.g. 'lbscat_rbc, Red Blood Cells (RBC) - x10E6/µL'.
-- Requires unit_lookup (01_create_unit_lookup.sql). Dialect: Databricks / Spark SQL.
-- =============================================================================

-- A. One row per measurement with the unit assigned.
SELECT m.measurement_id,
       m.measurement_source_value,
       m.value_as_number,
       m.unit_concept_id                                   AS unit_concept_id_current,
       COALESCE(f.unit_concept_id, u.unit_concept_id, 0)   AS unit_concept_id,
       COALESCE(f.unit_source_value, NULLIF(TRIM(m.unit_source_value), '')) AS unit_source_value
FROM omop_survey.measurement m
LEFT JOIN unit_lookup f
       ON f.key_type = 'field'  AND f.lookup_key = TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))
LEFT JOIN unit_lookup u
       ON u.key_type = 'string' AND u.lookup_key = TRIM(m.unit_source_value);

-- B. Summary by field: current unit vs unit from unit_lookup.
SELECT TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))  AS field_name,
       m.unit_concept_id                                     AS unit_concept_id_current,
       COALESCE(f.unit_concept_id, u.unit_concept_id, 0)     AS unit_concept_id,
       COALESCE(f.unit_source_value, NULLIF(TRIM(m.unit_source_value), '')) AS unit_source_value,
       COUNT(*)                                              AS n
FROM omop_survey.measurement m
LEFT JOIN unit_lookup f
       ON f.key_type = 'field'  AND f.lookup_key = TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))
LEFT JOIN unit_lookup u
       ON u.key_type = 'string' AND u.lookup_key = TRIM(m.unit_source_value)
GROUP BY ALL
ORDER BY field_name;
