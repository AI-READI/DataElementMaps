-- =============================================================================
-- 05_check_no_fanout.sql
-- AI-READI concept map: check that the unit LEFT JOIN adds no rows
--
-- Requires unit_lookup (01_create_unit_lookup.sql). Dialect: Databricks / Spark SQL.
-- For an ETL staging table, replace omop_survey.measurement and the field-name expression.
-- =============================================================================

-- A. The two counts must be equal.
SELECT (SELECT COUNT(*) FROM omop_survey.measurement) AS rows_before,
       (SELECT COUNT(*)
        FROM omop_survey.measurement m
        LEFT JOIN unit_lookup f
               ON f.key_type = 'field'  AND f.lookup_key = TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))
        LEFT JOIN unit_lookup u
               ON u.key_type = 'string' AND u.lookup_key = TRIM(m.unit_source_value)) AS rows_after;

-- B. Must return 0 rows (no measurement appears more than once).
SELECT m.measurement_id, COUNT(*) AS n
FROM omop_survey.measurement m
LEFT JOIN unit_lookup f
       ON f.key_type = 'field'  AND f.lookup_key = TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))
LEFT JOIN unit_lookup u
       ON u.key_type = 'string' AND u.lookup_key = TRIM(m.unit_source_value)
GROUP BY m.measurement_id
HAVING COUNT(*) > 1;
