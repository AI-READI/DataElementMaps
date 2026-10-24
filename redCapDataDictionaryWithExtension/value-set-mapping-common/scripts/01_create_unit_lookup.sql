-- =============================================================================
-- 01_create_unit_lookup.sql
-- AI-READI concept map: create the unit_lookup table (one query)
--
-- unit_lookup has one row per (key_type, lookup_key):
--   key_type = 'field'  : lookup_key = measurement field name (e.g. lbscat_rbc)      -> 90 rows
--   key_type = 'string' : lookup_key = unit text            (e.g. 'mEq/L')          -> 25 rows
-- v1.7: 115 rows (v1.6: 113; v1.4 and v1.5: 110). Same content as unit_concept_lookup.csv (option A: 01a_load_unit_concept_lookup_csv.sql).
--
-- Requires the concept map as a table or view named concept_map (see 00_load_concept_map.sql).
-- Dialect: Databricks / Spark SQL.
-- =============================================================================

CREATE OR REPLACE TABLE unit_lookup AS
-- by field name: Unit rows named <field>_u
SELECT DISTINCT
       'field'                                   AS key_type,
       REGEXP_REPLACE(TRIM(FIELD_ID), '_u$', '') AS lookup_key,
       CAST(TARGET_CONCEPT_ID AS INT)            AS unit_concept_id,
       TRIM(SRC_CODE)                            AS unit_source_value
FROM concept_map
WHERE TARGET_DOMAIN_ID = 'Unit'
  AND RIGHT(TRIM(FIELD_ID), 2) = '_u'
UNION ALL
-- LDL: the measurement field and its unit field have different names
SELECT DISTINCT
       'field', 'import_ldl_cholesterol_calculation',
       CAST(TARGET_CONCEPT_ID AS INT), TRIM(SRC_CODE)
FROM concept_map
WHERE TARGET_DOMAIN_ID = 'Unit'
  AND TRIM(FIELD_ID) = 'import_ldl_cholesterol_u'
UNION ALL
-- by unit text: generic Unit rows (blank FIELD_ID) plus 's', 'second', 'score'
SELECT DISTINCT
       'string', TRIM(SRC_CODE),
       CAST(TARGET_CONCEPT_ID AS INT), TRIM(SRC_CODE)
FROM concept_map
WHERE TARGET_DOMAIN_ID = 'Unit'
  AND (COALESCE(TRIM(FIELD_ID), '') = '' OR TRIM(SRC_CODE) IN ('s', 'second', 'score'));
