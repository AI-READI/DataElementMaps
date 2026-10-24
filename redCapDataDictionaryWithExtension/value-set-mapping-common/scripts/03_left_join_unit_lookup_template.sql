-- =============================================================================
-- 03_left_join_unit_lookup_template.sql
-- AI-READI concept map: LEFT JOIN template to assign unit_concept_id
--
-- Replace the placeholders, then add this to the measurement ETL step:
--   <your_measurement_table> : your measurement / staging table
--   <field_name_column>      : the REDCap field name, e.g. lbscat_rbc
--   <unit_text_column>       : the unit text on the record, if any, e.g. 'mEq/L' (may be NULL)
--
-- Rule: unit by field name first, then by unit text, otherwise 0 (no matching concept).
-- Unit text is trimmed, and blank text (e.g. ' ') is written as NULL (v1.7 ETL rule 5).
-- unit_lookup has one row per key, so the LEFT JOINs never add rows.
-- Requires unit_lookup (01_create_unit_lookup.sql). Dialect: Databricks / Spark SQL.
-- This file contains placeholders and does not run until they are replaced.
-- =============================================================================

SELECT m.*,
       COALESCE(f.unit_concept_id, u.unit_concept_id, 0)   AS unit_concept_id,
       COALESCE(f.unit_source_value, NULLIF(TRIM(m.<unit_text_column>), '')) AS unit_source_value
FROM <your_measurement_table> m
LEFT JOIN unit_lookup f
       ON f.key_type = 'field'  AND f.lookup_key = TRIM(m.<field_name_column>)
LEFT JOIN unit_lookup u
       ON u.key_type = 'string' AND u.lookup_key = TRIM(m.<unit_text_column>);
