-- =============================================================================
-- 09_validate_units_and_value_ranges.sql
-- AI-READI OMOP survey data - unit mapping and value-range validation (added in v1.8.5)
-- Databricks / Spark SQL
-- READ-ONLY: only SELECT and TEMPORARY VIEWs. Nothing is written to
-- omop_survey, omop_vocab or redcapsurveydb.
--
-- Inputs:
--   omop_survey.measurement, omop_survey.person      (delivered OMOP survey build)
--   redcapsurveydb.unit_concept_lookup               (v1.8.4, 114 rows: 89 field, 25 string)
--   redcapsurveydb.concept_map_v184                  (v1.8.4 concept map, all STRING)
--   omop_vocab.concept
--
-- Sections
--   U1  Unit coverage (rows / fields that get a unit)
--   U2  No fan-out from the unit join
--   U3  Lookup units are valid standard Unit concepts; map unit rows are Unit domain
--   U4  Fields with no unit (confirm each is meant to be unitless)
--   U5  Source unit text that disagrees with the assigned unit
--   U6  Value distribution per field and unit text
--   U7  Batch comparison: rows with vs without unit text (same units?)
--   U8  Plausible / extreme range check per field (summary + row list)
--   U9  Waist / hip: zeros, values entered in the wrong fields, mismatch with BMI
--   U10 Refraction: large difference between the two eyes
--   U11 Dates and age at measurement; stored ages over 89 (cage, age_years_at_interview)
--   U12 Same person, date and field with different values
--   U13 Zeros by year (fields where 0 is not a real result)
--   U14 Monthly median drift (lab or assay changes)
--
-- Baseline results from the v1.0-tvst build checked on 2026-10-28 are noted
-- under each section. Corrections belong in REDCap and are handed off to the ETL
-- team for the next build; none of these checks needs a concept map change.
--
-- Output lists person_id values: keep results in Databricks or a private channel;
-- do not paste them into GitHub issues, commits or public documents.
--
-- Related: value-set-mapping-common/scripts/05_check_no_fanout.sql and
-- 06_check_units_after_etl.sql (post-ETL checks on the reloaded tables).
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Setup (temporary views only)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW mu AS
SELECT m.measurement_id, m.person_id, m.measurement_date,
       TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))  AS field,
       m.value_as_number                                      AS v,
       NULLIF(TRIM(m.unit_source_value), '')                  AS unit_text,
       m.unit_concept_id                                      AS current_unit_concept_id,
       COALESCE(f.unit_concept_id, s.unit_concept_id, 0)      AS test_unit_concept_id,
       COALESCE(f.unit_source_value, s.unit_source_value)     AS lookup_unit,
       CASE WHEN f.lookup_key IS NOT NULL THEN 'field'
            WHEN s.lookup_key IS NOT NULL THEN 'string' END   AS matched_on
FROM omop_survey.measurement m
LEFT JOIN redcapsurveydb.unit_concept_lookup f
       ON f.key_type = 'field'  AND f.lookup_key = TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))
LEFT JOIN redcapsurveydb.unit_concept_lookup s
       ON s.key_type = 'string' AND s.lookup_key = NULLIF(TRIM(m.unit_source_value), '');

-- -----------------------------------------------------------------------------
-- U1. Unit coverage
-- -----------------------------------------------------------------------------
-- Baseline: unit filled 86 fields / 337,196 rows; no unit 26 fields / 104,454 rows
SELECT CASE WHEN test_unit_concept_id = 0 THEN 'no unit' ELSE 'unit filled' END AS status,
       COUNT(DISTINCT field) AS fields, COUNT(*) AS n
FROM mu WHERE v IS NOT NULL GROUP BY 1;

-- How the unit was matched (field name first, then unit text)
SELECT COALESCE(matched_on, 'none') AS matched_on, COUNT(DISTINCT field) AS fields, COUNT(*) AS n
FROM mu WHERE v IS NOT NULL GROUP BY 1;

-- -----------------------------------------------------------------------------
-- U2. No fan-out
-- -----------------------------------------------------------------------------
-- Expected: view_rows = table_rows (441,661)
SELECT (SELECT COUNT(*) FROM mu) AS view_rows,
       (SELECT COUNT(*) FROM omop_survey.measurement) AS table_rows;

-- -----------------------------------------------------------------------------
-- U3. Lookup and map unit concepts are valid
-- -----------------------------------------------------------------------------
-- Expected: 0 rows (every lookup unit is a standard, valid Unit concept)
SELECT l.key_type, l.lookup_key, l.unit_concept_id, l.unit_source_value,
       c.concept_name, c.domain_id, c.standard_concept, c.invalid_reason
FROM redcapsurveydb.unit_concept_lookup l
LEFT JOIN omop_vocab.concept c ON c.concept_id = CAST(l.unit_concept_id AS BIGINT)
WHERE c.concept_id IS NULL OR c.domain_id <> 'Unit'
   OR c.standard_concept IS DISTINCT FROM 'S' OR c.invalid_reason IS NOT NULL;

-- Expected: 0 rows (every map Unit row points to a Unit-domain concept)
SELECT TRIM(m.FIELD_ID) AS field_id, TRIM(m.SRC_CODE) AS src_code, m.TARGET_CONCEPT_ID, c.concept_name, c.domain_id
FROM redcapsurveydb.concept_map_v184 m
JOIN omop_vocab.concept c ON c.concept_id = CAST(NULLIF(TRIM(m.TARGET_CONCEPT_ID), '') AS BIGINT)
WHERE TRIM(m.Map_to_OMOP) = 'Yes' AND TRIM(m.TARGET_DOMAIN_ID) = 'Unit' AND c.domain_id <> 'Unit';

-- Expected: 0 rows (every field-key in the lookup has a Yes unit row named <field>_u).
-- Known exception, excluded below: import_ldl_cholesterol_calculation, whose unit row is
-- import_ldl_cholesterol_u (map line 538); the lookup also has the key import_ldl_cholesterol.
SELECT l.lookup_key, l.unit_concept_id
FROM redcapsurveydb.unit_concept_lookup l
LEFT JOIN redcapsurveydb.concept_map_v184 m
       ON TRIM(m.FIELD_ID) = CONCAT(l.lookup_key, '_u') AND TRIM(m.Map_to_OMOP) = 'Yes'
      AND TRIM(m.TARGET_DOMAIN_ID) = 'Unit'
WHERE l.key_type = 'field' AND m.FIELD_ID IS NULL
  AND l.lookup_key <> 'import_ldl_cholesterol_calculation';

-- -----------------------------------------------------------------------------
-- U4. Fields with no unit
-- -----------------------------------------------------------------------------
-- Expected: 26 fields, all meant to be unitless (monofilament and other
-- categorical/score fields). Any lab or vital sign here is a gap in the lookup.
SELECT field, COUNT(*) AS n, MIN(v) AS min_v, MAX(v) AS max_v, COLLECT_SET(unit_text) AS unit_texts
FROM mu WHERE v IS NOT NULL AND test_unit_concept_id = 0
GROUP BY 1 ORDER BY 1;

-- -----------------------------------------------------------------------------
-- U5. Source unit text that disagrees with the assigned unit
-- -----------------------------------------------------------------------------
-- Expected (known, harmless because the field key wins):
--   import_calcium 'mEq/L' (values are mg/dL); import_c_peptide and import_insulin 'ng/L'
--   (values are ng/mL); import_urine_albumin / import_urine_creatinine 'g/mL', '_g/mL'
--   (garbled; values are mg/dL); import_ag_ratio, import_bilirubin_total,
--   import_globulin_total_norc 'N/A'. Anything else: review.
SELECT field, unit_text, lookup_unit, matched_on, COUNT(*) AS n
FROM mu
WHERE v IS NOT NULL AND unit_text IS NOT NULL AND lookup_unit IS NOT NULL
  AND LOWER(REPLACE(unit_text, ' ', '')) <> LOWER(REPLACE(lookup_unit, ' ', ''))
GROUP BY 1, 2, 3, 4 ORDER BY 1, 2;

-- -----------------------------------------------------------------------------
-- U6. Value distribution per field and unit text (about 113 rows)
-- -----------------------------------------------------------------------------
-- Review: each median must suit the assigned unit (e.g. creatinine ~0.8 mg/dL,
-- glucose ~95 mg/dL, HbA1c ~5.8 %). A median off by a conversion factor = wrong unit.
SELECT field, lookup_unit, COALESCE(unit_text, 'no text') AS unit_text, COUNT(*) AS n,
       PERCENTILE_APPROX(v, 0.01) AS p01, PERCENTILE_APPROX(v, 0.5) AS median,
       PERCENTILE_APPROX(v, 0.99) AS p99, MIN(v) AS min_v, MAX(v) AS max_v
FROM mu WHERE v IS NOT NULL AND test_unit_concept_id <> 0
GROUP BY 1, 2, 3 ORDER BY 1, 3;

-- -----------------------------------------------------------------------------
-- U7. Batch comparison: rows without unit text vs rows with unit text
-- -----------------------------------------------------------------------------
-- Expected: 0 rows (the 512-participant import without unit text uses the same
-- units; medians agree within 25%)
WITH b AS (
  SELECT field,
         PERCENTILE_APPROX(CASE WHEN unit_text IS NULL     THEN v END, 0.5) AS med_no_text,
         PERCENTILE_APPROX(CASE WHEN unit_text IS NOT NULL THEN v END, 0.5) AS med_text,
         SUM(CASE WHEN unit_text IS NULL THEN 1 ELSE 0 END) AS n_no_text,
         SUM(CASE WHEN unit_text IS NOT NULL THEN 1 ELSE 0 END) AS n_text
  FROM mu WHERE v IS NOT NULL GROUP BY 1)
SELECT field, n_text, med_text, n_no_text, med_no_text, ROUND(med_no_text / med_text, 2) AS ratio
FROM b
WHERE n_text > 0 AND n_no_text > 0 AND med_text <> 0
  AND (med_no_text / med_text < 0.8 OR med_no_text / med_text > 1.25)
ORDER BY 1;

-- -----------------------------------------------------------------------------
-- U8. Plausible and extreme range check
-- -----------------------------------------------------------------------------
-- imp_lo / imp_hi: outside = implausible (almost certainly an entry error)
-- ext_lo / ext_hi: outside = clinically extreme (possible; check same-date values)
-- Ranges are in the unit the lookup assigns.
CREATE OR REPLACE TEMPORARY VIEW ranges AS
SELECT * FROM VALUES
  ('bmi_vsorres',                         12,    100,    16,    60),
  ('bp1_sysbp_vsorres',                   60,    260,    80,   200),
  ('bp2_sysbp_vsorres',                   60,    260,    80,   200),
  ('bp1_diabp_vsorres',                   30,    160,    40,   120),
  ('bp2_diabp_vsorres',                   30,    160,    40,   120),
  ('pulse_vsorres',                       25,    220,    40,   130),
  ('pulse_vsorres_2',                     25,    220,    40,   130),
  ('height_vsorres',                     120,    220,   140,   200),
  ('weight_vsorres',                      25,    300,    40,   200),
  ('waist_vsorres',                       50,    200,    60,   160),
  ('hip_vsorres',                         60,    220,    75,   160),
  ('whr_vsorres',                        0.5,    1.6,  0.65,   1.2),
  ('import_ag_ratio',                    0.2,      5,   0.8,   2.8),
  ('import_albumin',                       1,      7,     3,   5.5),
  ('import_alkaline_phosphatase',         10,   2000,    30,   300),
  ('import_alt_got',                       1,   5000,     1,   200),
  ('import_ast_got',                       1,   5000,     1,   200),
  ('import_bilirubin_total',               0,     30,     0,     3),
  ('import_bun',                           1,    200,     3,    60),
  ('import_buncreatinineratio',        0.003,      1,  0.02,   0.2),
  ('import_bun_creatinine_ratio',          1,    300,     5,    50),
  ('import_c_peptide',                     0,     50,     0,    15),
  ('import_calcium',                       4,     16,   7.5,  11.5),
  ('import_carbon_dioxide_total',          5,     50,    15,    35),
  ('import_chloride',                     70,    140,    90,   115),
  ('import_creatinine',                  0.2,     20,   0.3,     4),
  ('import_crp_hs',                        0,    500,     0,    50),
  ('import_globulin_total_norc',         0.5,     10,     1,   4.5),
  ('import_glucose',                      20,   2000,    50,   400),
  ('import_hba1c',                         3,     20,     4,    14),
  ('import_hdl_cholesterol',               5,    200,    20,   120),
  ('import_insulin',                       0,     20,     0,    15),
  ('import_ldl_cholesterol_calculation',   0,    500,     0,   250),
  ('import_nt_probnp',                     0, 100000,     0, 10000),
  ('import_potassium',                     2,      8,     3,   6.5),
  ('import_protein_total',                 3,     12,   5.5,     9),
  ('import_sodium',                      110,    170,   128,   150),
  ('import_total_cholesterol',            50,    800,    60,   350),
  ('import_triglycerides',                10,  10000,    20,  1000),
  ('import_troponin_t',                    0,  10000,     0,   100),
  ('import_urine_albumin',                 0,   2000,     0,   300),
  ('import_urine_creatinine',              5,   1000,     5,   500),
  ('lbscat_a1c',                           4,     25,     8,    18),
  ('lbscat_hct',                          10,     75,    25,    55),
  ('lbscat_mch',                          15,     45,    20,    36),
  ('lbscat_mchc',                         20,     45,    28,    37),
  ('lbscat_mcv',                          50,    150,    70,   110),
  ('lbscat_plt',                           5,   2000,   100,   600),
  ('lbscat_rbc',                           1,     10,     3,   6.5),
  ('lbscat_rdw',                           8,     40,     9,    20),
  ('lbscat_wbc',                         0.5,    100,     2,    20),
  ('viaodsph',                           -30,     20,   -20,    10),
  ('viaossph',                           -30,     20,   -20,    10),
  ('viaodcyl',                             0,     10,     0,     6),
  ('viaoscyl',                             0,     10,     0,     6),
  ('viaodaxi',                             0,    180,     0,   180),
  ('viaosaxi',                             0,    180,     0,   180),
  ('moca_total_score',                     0,     30,     0,    30),
  ('moca_combined_mis_score',              0,     15,     0,    15),
  ('moca_orientation',                     0,      6,     0,     6)
AS r(field, imp_lo, imp_hi, ext_lo, ext_hi);

-- U8a. Summary per field (review every row with implausible > 0)
SELECT r.field, COUNT(*) AS n,
       SUM(CASE WHEN mu.v < r.imp_lo OR mu.v > r.imp_hi THEN 1 ELSE 0 END) AS implausible,
       SUM(CASE WHEN (mu.v >= r.imp_lo AND mu.v <= r.imp_hi)
                 AND (mu.v < r.ext_lo OR mu.v > r.ext_hi) THEN 1 ELSE 0 END) AS extreme,
       MIN(mu.v) AS min_v, MAX(mu.v) AS max_v
FROM mu JOIN ranges r ON r.field = mu.field
WHERE mu.v IS NOT NULL
GROUP BY 1
HAVING implausible > 0 OR extreme > 0
ORDER BY implausible DESC, extreme DESC;

-- U8b. Row list with person IDs (implausible first, then extreme)
SELECT CASE WHEN mu.v < r.imp_lo OR mu.v > r.imp_hi THEN 'implausible' ELSE 'extreme' END AS level,
       mu.field, mu.person_id, mu.measurement_date, mu.v AS value, mu.unit_text, mu.lookup_unit,
       CONCAT(r.imp_lo, ' to ', r.imp_hi) AS plausible_range, CONCAT(r.ext_lo, ' to ', r.ext_hi) AS usual_range
FROM mu JOIN ranges r ON r.field = mu.field
WHERE mu.v IS NOT NULL AND (mu.v < r.ext_lo OR mu.v > r.ext_hi)
ORDER BY level DESC, mu.field, mu.v;

-- U8c. Same-date context for people with extreme or implausible lab values
-- (several extreme values on one date usually means a real clinical picture,
--  a single isolated value more often an error, e.g. hemolysed potassium)
WITH flagged AS (
  SELECT DISTINCT mu.person_id, mu.measurement_date
  FROM mu JOIN ranges r ON r.field = mu.field
  WHERE mu.v IS NOT NULL AND (mu.v < r.ext_lo OR mu.v > r.ext_hi) AND mu.field LIKE 'import_%')
SELECT f.person_id, f.measurement_date,
       COUNT(*) AS n_flagged_fields,
       COLLECT_LIST(CONCAT(mu.field, '=', CAST(mu.v AS STRING))) AS flagged_values
FROM flagged f
JOIN mu ON mu.person_id = f.person_id AND mu.measurement_date = f.measurement_date
JOIN ranges r ON r.field = mu.field
WHERE mu.v < r.ext_lo OR mu.v > r.ext_hi
GROUP BY 1, 2 ORDER BY n_flagged_fields DESC, person_id;

-- -----------------------------------------------------------------------------
-- U9. Waist / hip review
-- -----------------------------------------------------------------------------
-- Baseline (v1.0-tvst build, 2026-10-28): 35 flagged person-dates. Entered in the wrong
-- fields: 3 (both values swapped with height/weight, or height < 130 equal to waist/hip).
-- Waist or hip equal to weight: 7, of which 2 have an implausible hip; the other 5 are
-- probably coincidence (waist in cm and weight in kg often have the same number).
-- sex: map gender_concept_id to your build's concepts (check SELECT DISTINCT gender_concept_id).
CREATE OR REPLACE TEMPORARY VIEW body AS
SELECT mu.person_id, mu.measurement_date,
       CASE p.gender_concept_id WHEN 8507 THEN 'M' WHEN 8532 THEN 'F' ELSE 'other' END AS sex,
       YEAR(mu.measurement_date) - p.year_of_birth AS age,
       MAX(CASE WHEN field = 'waist_vsorres'  THEN v END) AS waist_cm,
       MAX(CASE WHEN field = 'hip_vsorres'    THEN v END) AS hip_cm,
       MAX(CASE WHEN field = 'whr_vsorres'    THEN v END) AS whr,
       MAX(CASE WHEN field = 'height_vsorres' THEN v END) AS height_cm,
       MAX(CASE WHEN field = 'weight_vsorres' THEN v END) AS weight_kg,
       MAX(CASE WHEN field = 'bmi_vsorres'    THEN v END) AS bmi
FROM mu JOIN omop_survey.person p ON p.person_id = mu.person_id
WHERE field IN ('waist_vsorres', 'hip_vsorres', 'whr_vsorres', 'height_vsorres', 'weight_vsorres', 'bmi_vsorres')
GROUP BY 1, 2, 3, 4;

SELECT person_id, measurement_date, sex, age, waist_cm, hip_cm, ROUND(whr, 2) AS whr,
       height_cm, weight_kg, ROUND(bmi, 1) AS bmi,
       CONCAT_WS('; ',
         CASE WHEN waist_cm = 0 OR hip_cm = 0 THEN '0 recorded for a missing value' END,
         CASE WHEN (waist_cm = height_cm AND hip_cm = weight_kg)
                OR (waist_cm = weight_kg AND hip_cm = height_cm)
                OR ((waist_cm = height_cm OR hip_cm = height_cm) AND height_cm < 130)
              THEN 'entered in the wrong fields' END,
         CASE WHEN NOT ((waist_cm = height_cm AND hip_cm = weight_kg) OR (waist_cm = weight_kg AND hip_cm = height_cm)
                        OR ((waist_cm = height_cm OR hip_cm = height_cm) AND height_cm < 130))
               AND (waist_cm = weight_kg OR hip_cm = weight_kg)
              THEN 'waist or hip equals weight (often coincidence; an error only if the value is implausible)' END,
         CASE WHEN waist_cm > 0 AND waist_cm < 55  THEN 'waist < 55'  END,
         CASE WHEN waist_cm > 180                  THEN 'waist > 180' END,
         CASE WHEN hip_cm   > 0 AND hip_cm   < 65  THEN 'hip < 65'    END,
         CASE WHEN hip_cm   > 180                  THEN 'hip > 180'   END,
         CASE WHEN waist_cm - hip_cm > 30          THEN 'hip far below waist' END,
         CASE WHEN whr IS NOT NULL AND hip_cm > 0
               AND ABS(whr - waist_cm / hip_cm) > 0.01 THEN 'stored WHR <> waist / hip' END,
         CASE WHEN bmi < 22 AND waist_cm > 110     THEN 'waist large for BMI' END,
         CASE WHEN bmi > 28 AND waist_cm BETWEEN 1 AND 70 THEN 'waist small for BMI' END,
         CASE WHEN bmi > 28 AND hip_cm   BETWEEN 1 AND 85 THEN 'hip small for BMI' END,
         CASE WHEN bmi < 30 AND hip_cm   > 150     THEN 'hip large for BMI' END,
         CASE WHEN ABS(bmi - weight_kg / POWER(height_cm / 100, 2)) > 0.5 THEN 'stored BMI <> weight / height^2' END
       ) AS flag
FROM body
WHERE waist_cm = 0 OR hip_cm = 0
   OR waist_cm = height_cm OR hip_cm = weight_kg OR waist_cm = weight_kg OR hip_cm = height_cm
   OR waist_cm < 55 OR waist_cm > 180 OR hip_cm < 65 OR hip_cm > 180 OR waist_cm - hip_cm > 30
   OR (whr IS NOT NULL AND hip_cm > 0 AND ABS(whr - waist_cm / hip_cm) > 0.01)
   OR (bmi < 22 AND waist_cm > 110) OR (bmi > 28 AND waist_cm BETWEEN 1 AND 70)
   OR (bmi > 28 AND hip_cm BETWEEN 1 AND 85) OR (bmi < 30 AND hip_cm > 150)
   OR ABS(bmi - weight_kg / POWER(height_cm / 100, 2)) > 0.5
ORDER BY flag, person_id;

-- Hip and WHR against the person's own sex and age band (|z| > 3.5)
WITH b AS (
  SELECT *, CASE WHEN age < 50 THEN '40-49' WHEN age < 60 THEN '50-59' WHEN age < 70 THEN '60-69' ELSE '70+' END AS age_band
  FROM body WHERE hip_cm > 0 AND waist_cm > 0),
z AS (
  SELECT *,
         (hip_cm - AVG(hip_cm) OVER (PARTITION BY sex, age_band)) / STDDEV(hip_cm) OVER (PARTITION BY sex, age_band) AS hip_z,
         (whr    - AVG(whr)    OVER (PARTITION BY sex, age_band)) / STDDEV(whr)    OVER (PARTITION BY sex, age_band) AS whr_z
  FROM b)
SELECT person_id, measurement_date, sex, age, age_band, waist_cm, hip_cm, ROUND(whr, 2) AS whr, ROUND(bmi, 1) AS bmi,
       ROUND(hip_z, 1) AS hip_z, ROUND(whr_z, 1) AS whr_z
FROM z
WHERE ABS(hip_z) > 3.5 OR ABS(whr_z) > 3.5
ORDER BY GREATEST(ABS(hip_z), ABS(whr_z)) DESC;

-- -----------------------------------------------------------------------------
-- U10. Refraction: large difference between the two eyes
-- -----------------------------------------------------------------------------
-- Baseline (2026-10-28): 3 people with one eye about -27 D and the other near normal
WITH r AS (
  SELECT person_id, measurement_date,
         MAX(CASE WHEN field = 'viaodsph' THEN v END) AS od_sph,
         MAX(CASE WHEN field = 'viaossph' THEN v END) AS os_sph,
         MAX(CASE WHEN field = 'viaodcyl' THEN v END) AS od_cyl,
         MAX(CASE WHEN field = 'viaoscyl' THEN v END) AS os_cyl
  FROM mu WHERE field IN ('viaodsph', 'viaossph', 'viaodcyl', 'viaoscyl')
  GROUP BY 1, 2)
SELECT *, ABS(od_sph - os_sph) AS sph_difference
FROM r
WHERE ABS(od_sph - os_sph) > 10 OR od_sph < -20 OR os_sph < -20 OR od_cyl > 6 OR os_cyl > 6
ORDER BY sph_difference DESC;

-- -----------------------------------------------------------------------------
-- U11. Dates and age at measurement
-- -----------------------------------------------------------------------------
-- Baseline (2026-10-28): 5 people with every field (59) dated before enrollment
-- (wrong visit date) and 1 person with 2 fields dated 2014
SELECT person_id, measurement_date, COUNT(*) AS n_rows, COUNT(DISTINCT field) AS n_fields,
       CASE WHEN measurement_date < '2023-01-01' THEN 'before enrollment' ELSE 'in the future' END AS issue
FROM mu
WHERE measurement_date < '2023-01-01' OR measurement_date > CURRENT_DATE()
GROUP BY 1, 2 ORDER BY 2;

-- Age outside the AI-READI range (adults 40+). Age from year only (can be off by 1).
-- year_of_birth is capped on purpose (age 90; 1936 in the 2024-2026 visits), so ages near 90
-- are censored and are not flagged. Baseline (2026-10-28): 2 participants under 40.
SELECT mu.person_id, p.year_of_birth, MIN(mu.measurement_date) AS first_date, MAX(mu.measurement_date) AS last_date,
       MIN(YEAR(mu.measurement_date) - p.year_of_birth) AS min_age,
       MAX(YEAR(mu.measurement_date) - p.year_of_birth) AS max_age
FROM mu JOIN omop_survey.person p ON p.person_id = mu.person_id
GROUP BY 1, 2
HAVING min_age < 39 OR max_age > 100
ORDER BY min_age;

-- Stored age values over 89 (ages must be capped at 90 = "90 or older").
-- cage: "Age (in years)", demographics survey, concept 3022304 (value_as_number and value_as_string).
-- age_years_at_interview: MoCA import, "pull down menu of 3-4 year age spans, age in years", 2005200372.
-- Baseline (2026-10-28): cage 18 rows over 89 (90-94); age_years_at_interview added in v1.8.6, not yet checked.
-- Pass: rows_over_89 = 0 and max_value <= 90 for both fields.
SELECT tbl, field, COUNT(*) AS n, MIN(v) AS min_value, MAX(v) AS max_value,
       MAX(TRY_CAST(s AS DOUBLE)) AS max_value_string,
       SUM(CASE WHEN v > 89 OR TRY_CAST(s AS DOUBLE) > 89 THEN 1 ELSE 0 END) AS rows_over_89
FROM (
  SELECT 'observation' AS tbl, TRIM(SPLIT_PART(observation_source_value, ',', 1)) AS field,
         value_as_number AS v, value_as_string AS s
  FROM omop_survey.observation
  UNION ALL
  SELECT 'measurement', TRIM(SPLIT_PART(measurement_source_value, ',', 1)), value_as_number, CAST(NULL AS STRING)
  FROM omop_survey.measurement)
WHERE field IN ('cage', 'age_years_at_interview')
GROUP BY 1, 2;

-- -----------------------------------------------------------------------------
-- U12. Same person, date and field with different values
-- -----------------------------------------------------------------------------
-- Review: repeated entries with different values (expected 0 rows, or explained repeats)
SELECT field, person_id, measurement_date, COUNT(*) AS n_rows, COLLECT_SET(v) AS values
FROM mu
WHERE v IS NOT NULL
GROUP BY 1, 2, 3
HAVING COUNT(DISTINCT v) > 1
ORDER BY n_rows DESC, field
LIMIT 200;

-- -----------------------------------------------------------------------------
-- U13. Zeros by year (fields where 0 is not a real result)
-- -----------------------------------------------------------------------------
-- 0 usually means a missing value or a result below the reporting limit.
-- Baseline (2026-10-28): urine albumin 281 zeros (2023: 9, 2024: 221, 2025: 50,
-- 2026: 1; probably "below the reporting limit"); urine creatinine 1; calcium 1;
-- waist and hip 2 each; Snellen denominator (*sf) 8 = off-chart vision, valid.
SELECT field, YEAR(measurement_date) AS yr,
       SUM(CASE WHEN v = 0 THEN 1 ELSE 0 END) AS zeros, COUNT(*) AS n,
       MIN(CASE WHEN v > 0 THEN v END) AS min_nonzero
FROM mu
WHERE v IS NOT NULL
  AND (field LIKE 'import_%' OR field LIKE 'lbscat_%'
       OR field IN ('waist_vsorres', 'hip_vsorres', 'height_vsorres', 'weight_vsorres', 'bmi_vsorres'))
  AND field NOT IN ('import_crp_hs')               -- 0 can be a below-detection result
GROUP BY 1, 2
HAVING SUM(CASE WHEN v = 0 THEN 1 ELSE 0 END) > 0
ORDER BY 1, 2;

-- -----------------------------------------------------------------------------
-- U14. Monthly median drift (lab or assay changes)
-- -----------------------------------------------------------------------------
-- Flags months whose median is more than 20% from the field's overall median
-- (months with at least 30 results). A run of flagged months for one field
-- points to a lab, assay or import change rather than to individual errors.
-- Baseline (2026-10-28): review CO2 (import_carbon_dioxide_total) in 2026, where
-- values of 36-43 mEq/L cluster in February-June.
WITH mo AS (
  SELECT field, DATE_TRUNC('month', measurement_date) AS month, COUNT(*) AS n,
         PERCENTILE_APPROX(v, 0.5) AS med, PERCENTILE_APPROX(v, 0.99) AS p99
  FROM mu WHERE v IS NOT NULL AND (field LIKE 'import_%' OR field LIKE 'lbscat_%')
  GROUP BY 1, 2),
allm AS (
  SELECT field, PERCENTILE_APPROX(v, 0.5) AS overall_med, PERCENTILE_APPROX(v, 0.99) AS overall_p99
  FROM mu WHERE v IS NOT NULL AND (field LIKE 'import_%' OR field LIKE 'lbscat_%')
  GROUP BY 1)
SELECT mo.field, mo.month, mo.n, mo.med, a.overall_med, ROUND(mo.med / a.overall_med, 2) AS med_ratio,
       mo.p99, a.overall_p99
FROM mo JOIN allm a ON a.field = mo.field
WHERE mo.n >= 30 AND a.overall_med <> 0
  AND (mo.med / a.overall_med < 0.8 OR mo.med / a.overall_med > 1.2)
ORDER BY mo.field, mo.month;
-- =============================================================================
