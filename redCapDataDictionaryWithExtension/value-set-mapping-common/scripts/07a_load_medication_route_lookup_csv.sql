-- =============================================================================
-- 07a_load_medication_route_lookup_csv.sql
-- AI-READI concept map: create the medication_route_lookup table from medication_route_lookup.csv
--
-- Option A (simplest): load the ready-made file. Same result as
-- 07_create_medication_route_lookup.sql (option B), without loading the concept map.
--
-- medication_route_lookup.csv columns:
--   key_type, lookup_key, route_concept_id, route_concept_name, route_source_value
-- v1.4: 26 rows (code 13, string 13), one row per (key_type, lookup_key).
--
-- Set the path to your copy of medication_route_lookup.csv, then run.
-- Dialect: Databricks / Spark SQL.
-- =============================================================================

CREATE OR REPLACE TEMPORARY VIEW medication_route_lookup_csv
USING csv
OPTIONS (
  path     '/Volumes/<catalog>/<schema>/<volume>/medication_route_lookup.csv',  -- <-- set this
  header   'true',
  encoding 'UTF-8'
);

CREATE OR REPLACE TABLE medication_route_lookup AS
SELECT TRIM(key_type)                AS key_type,
       TRIM(lookup_key)              AS lookup_key,
       CAST(route_concept_id AS INT) AS route_concept_id,
       COALESCE(route_concept_name, '') AS route_concept_name,
       TRIM(route_source_value)      AS route_source_value
FROM medication_route_lookup_csv;

-- Check: 26 rows; code 13, string 13.
SELECT key_type, COUNT(*) AS n FROM medication_route_lookup GROUP BY key_type ORDER BY key_type;
