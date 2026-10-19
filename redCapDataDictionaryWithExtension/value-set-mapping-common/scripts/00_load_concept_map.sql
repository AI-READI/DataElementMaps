-- =============================================================================
-- 00_load_concept_map.sql
-- AI-READI concept map: load the mapping file as a view named `concept_map`
--
-- Dialect: Databricks / Spark SQL.
-- Every column is read as text (STRING); empty cells are read as NULL.
--
-- Set the path to your copy of the mapping file, then run this script once per
-- session before the other scripts.
-- =============================================================================

CREATE OR REPLACE TEMPORARY VIEW concept_map
USING csv
OPTIONS (
  path      '/Volumes/<catalog>/<schema>/<volume>/_ai_readi_redcap_value_set_mapping_common.csv',  -- <-- set this
  header    'true',
  encoding  'UTF-8',
  multiLine 'true'
);

-- Check: v1.4 has 2,076 data rows.
SELECT COUNT(*) AS n_rows FROM concept_map;

-- Alternative: if the concept map is already loaded as a table, point the view at it instead.
-- CREATE OR REPLACE TEMPORARY VIEW concept_map AS SELECT * FROM <catalog>.<schema>.<concept_map_table>;
