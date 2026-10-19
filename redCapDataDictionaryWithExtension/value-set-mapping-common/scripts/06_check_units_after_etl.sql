-- =============================================================================
-- 06_check_units_after_etl.sql
-- AI-READI concept map: check MEASUREMENT units after the ETL is re-run with v1.4
--
-- Dialect: Databricks / Spark SQL.
-- =============================================================================

-- A. Fields that should now have a unit: expect no unit_concept_id = 0.
--    (CBC, globulin, bilirubin, physical assessment, autorefractor, imported labs)
SELECT TRIM(SPLIT_PART(measurement_source_value, ',', 1)) AS field_name,
       unit_concept_id,
       unit_source_value,
       COUNT(*) AS n
FROM omop_survey.measurement
WHERE TRIM(SPLIT_PART(measurement_source_value, ',', 1)) IN (
        'lbscat_wbc', 'lbscat_rbc', 'lbscat_a1c', 'lbscat_hct', 'lbscat_mcv',
        'lbscat_mch', 'lbscat_mchc', 'lbscat_rdw', 'lbscat_plt',
        'import_globulin_total_norc', 'import_bilirubin_total', 'import_potassium',
        'height_vsorres', 'weight_vsorres', 'bmi_vsorres', 'waist_vsorres', 'hip_vsorres',
        'bp1_sysbp_vsorres', 'bp1_diabp_vsorres', 'bp2_sysbp_vsorres', 'bp2_diabp_vsorres',
        'pulse_vsorres', 'pulse_vsorres_2')
GROUP BY ALL
ORDER BY field_name;

-- B. All measurements still without a unit, by field.
--    Expected: unitless vision scores and ratios only.
SELECT TRIM(SPLIT_PART(measurement_source_value, ',', 1)) AS field_name,
       COUNT(*) AS n
FROM omop_survey.measurement
WHERE COALESCE(unit_concept_id, 0) = 0
GROUP BY ALL
ORDER BY n DESC;
