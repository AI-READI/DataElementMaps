-- =============================================================================
-- 07_create_medication_route_lookup.sql
-- AI-READI concept map: create the medication_route_lookup table (one query)
--
-- For the medication route question cmroute ("How is it taken?"), a protected field.
-- Maps each answer to a standard SNOMED Route concept for DRUG_EXPOSURE.route_concept_id.
--
-- medication_route_lookup has one row per (key_type, lookup_key):
--   key_type = 'code'   : lookup_key = REDCap answer code (e.g. '6')   -> 13 rows
--   key_type = 'string' : lookup_key = answer label       (e.g. 'Oral') -> 13 rows
-- v1.4: 26 rows. Same content as medication_route_lookup.csv
-- (option A: 07a_load_medication_route_lookup_csv.sql). "Other" maps to 0.
--
-- Requires the concept map as a table or view named concept_map (see 00_load_concept_map.sql).
-- Dialect: Databricks / Spark SQL.
-- =============================================================================

CREATE OR REPLACE TABLE medication_route_lookup AS
SELECT DISTINCT
       'code'                                     AS key_type,
       TRIM(SRC_CODE)                             AS lookup_key,
       CAST(TARGET_CONCEPT_ID AS INT)             AS route_concept_id,
       COALESCE(TARGET_CONCEPT_NAME, '')          AS route_concept_name,
       TRIM(SRC_CD_DESCRIPTION)                   AS route_source_value
FROM concept_map
WHERE TRIM(FIELD_ID) = 'cmroute'
  AND temp_Question_or_Answer = 'Answer'
UNION ALL
SELECT DISTINCT
       'string', TRIM(SRC_CD_DESCRIPTION),
       CAST(TARGET_CONCEPT_ID AS INT), COALESCE(TARGET_CONCEPT_NAME, ''), TRIM(SRC_CD_DESCRIPTION)
FROM concept_map
WHERE TRIM(FIELD_ID) = 'cmroute'
  AND temp_Question_or_Answer = 'Answer';
