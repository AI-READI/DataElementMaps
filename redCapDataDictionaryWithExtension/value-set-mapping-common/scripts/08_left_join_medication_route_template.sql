-- =============================================================================
-- 08_left_join_medication_route_template.sql
-- AI-READI concept map: LEFT JOIN template to assign DRUG_EXPOSURE.route_concept_id
--
-- Replace the placeholders, then add this to the drug exposure ETL step:
--   <your_drug_exposure_table> : your drug exposure / staging table
--   <cmroute_code_column>      : the REDCap answer code for cmroute, e.g. '6' (may be NULL)
--   <cmroute_label_column>     : the answer label, e.g. 'Oral', if the code is not available (may be NULL)
--
-- Rule: route by answer code first, then by label, otherwise 0 (no matching concept).
-- medication_route_lookup has one row per key, so the LEFT JOINs never add rows.
-- Requires medication_route_lookup (07_ or 07a_). Dialect: Databricks / Spark SQL.
-- This file contains placeholders and does not run until they are replaced.
-- =============================================================================

SELECT d.*,
       COALESCE(c.route_concept_id, s.route_concept_id, 0)         AS route_concept_id,
       COALESCE(c.route_source_value, s.route_source_value,
                d.<cmroute_label_column>)                          AS route_source_value
FROM <your_drug_exposure_table> d
LEFT JOIN medication_route_lookup c
       ON c.key_type = 'code'   AND c.lookup_key = TRIM(CAST(d.<cmroute_code_column> AS STRING))
LEFT JOIN medication_route_lookup s
       ON s.key_type = 'string' AND LOWER(s.lookup_key) = LOWER(TRIM(d.<cmroute_label_column>));

-- Check: the row count before and after the join must be equal.
-- SELECT (SELECT COUNT(*) FROM <your_drug_exposure_table>) AS rows_before,
--        (SELECT COUNT(*) FROM <your_drug_exposure_table> d
--           LEFT JOIN medication_route_lookup c ON c.key_type = 'code'   AND c.lookup_key = TRIM(CAST(d.<cmroute_code_column> AS STRING))
--           LEFT JOIN medication_route_lookup s ON s.key_type = 'string' AND LOWER(s.lookup_key) = LOWER(TRIM(d.<cmroute_label_column>))) AS rows_after;
