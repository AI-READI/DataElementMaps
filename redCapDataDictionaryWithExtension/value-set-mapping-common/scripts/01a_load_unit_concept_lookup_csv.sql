-- =============================================================================
-- 01a_load_unit_concept_lookup_csv.sql
-- AI-READI concept map: create the unit_lookup table from unit_concept_lookup.csv
--
-- Option A (simplest): load the ready-made file. Same result as
-- 01_create_unit_lookup.sql (option B), without loading the concept map.
--
-- unit_concept_lookup.csv columns: key_type, lookup_key, unit_concept_id, unit_source_value
-- v1.8.1: 114 rows (field 89, string 25), one row per (key_type, lookup_key).
-- The file is UTF-8 (x10E3/µL and x10E6/µL use the micro sign U+00B5).
--
-- Set the path to your copy of unit_concept_lookup.csv, then run.
-- Dialect: Databricks / Spark SQL.
-- =============================================================================

CREATE OR REPLACE TEMPORARY VIEW unit_concept_lookup_csv
USING csv
OPTIONS (
  path     '/Volumes/<catalog>/<schema>/<volume>/unit_concept_lookup.csv',  -- <-- set this
  header   'true',
  encoding 'UTF-8'
);

CREATE OR REPLACE TABLE unit_lookup AS
SELECT TRIM(key_type)                AS key_type,
       TRIM(lookup_key)              AS lookup_key,
       CAST(unit_concept_id AS INT)  AS unit_concept_id,
       TRIM(unit_source_value)       AS unit_source_value
FROM unit_concept_lookup_csv;

-- Check: 114 rows; field 89, string 25.
SELECT key_type, COUNT(*) AS n FROM unit_lookup GROUP BY key_type ORDER BY key_type;
