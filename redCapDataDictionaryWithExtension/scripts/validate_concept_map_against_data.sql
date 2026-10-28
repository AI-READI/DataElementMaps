-- =============================================================================
-- validate_concept_map_against_data.sql
-- AI-READI concept map: release checks against the OMOP survey data (Databricks / Spark SQL)
-- Added in v1.8.4. Run with validate_concept_map_vocab.sql before every release.
--
-- READ-ONLY: only SELECT and TEMPORARY VIEWs. Nothing is written to omop_survey,
-- omop_vocab or redcapsurveydb.
--
-- Before running:
--   1. Load the release's _ai_readi_redcap_value_set_mapping_common.csv as a table
--      (all columns as STRING) and set its name in section 0 (here redcapsurveydb.concept_map_v184).
--   2. redcapsurveydb.unit_concept_lookup = the release's scripts/unit_concept_lookup.csv.
--   3. Run validate_concept_map_vocab.sql against the same table (section A lists what it must return).
--
-- Each check states PASS = the expected result for v1.8.4. Section 5 checks the rows changed in
-- v1.8.x; update it for later releases.
-- =============================================================================

-- -----------------------------------------------------------------------------
-- A. Vocabulary (validate_concept_map_vocab.sql on concept_map_v184)
-- -----------------------------------------------------------------------------
-- PASS: V0 = 2,143 rows. V1, V3, V4, V5, V6 = 0 rows.
--       V2 = only deliberate domain overrides (including pxne4 / pxne5 code 88 -> 40192520,
--            map domain Meas Value, vocabulary domain Observation).
--       V7, V8, V9 = review lists, same as v1.8.3 except: V8 no longer lists pxne16 or code 88.
--       V10 = 2 rows (monofilament msslftt, mssrftt).
--       S4 = 2 rows (mhoccur_circ, mhoccur_cvdot; mh_a1c is now standard).

-- -----------------------------------------------------------------------------
-- 0. Setup (temporary views only)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW cm AS
SELECT TRIM(Map_to_OMOP) AS map_yes, TRIM(FIELD_ID) AS field_id, TRIM(SRC_CODE) AS src_code,
       TRIM(temp_Question_or_Answer) AS row_type, TRIM(TARGET_DOMAIN_ID) AS domain_id,
       CAST(NULLIF(TRIM(TARGET_CONCEPT_ID), '') AS BIGINT) AS tid, TARGET_CONCEPT_NAME AS tname,
       TRIM(TARGET_VOCABULARY_ID) AS vocab, TRIM(TARGET_CONCEPT_CODE) AS tcode,
       TRIM(PREDICATE_ID) AS predicate, TRIM(CONFIDENCE) AS confidence, TRIM(MODIFIER) AS modifier
FROM redcapsurveydb.concept_map_v184;

-- -----------------------------------------------------------------------------
-- 1. Row count
-- -----------------------------------------------------------------------------
-- PASS: 2143
SELECT COUNT(*) AS n_rows FROM cm;

-- -----------------------------------------------------------------------------
-- 2. Standard targets that are no longer standard or valid (query 4)
-- -----------------------------------------------------------------------------
-- PASS: 0 rows
SELECT m.field_id, m.src_code, m.tid, c.concept_name, c.standard_concept, c.invalid_reason,
       r.concept_id_2 AS maps_to_id
FROM cm m
JOIN omop_vocab.concept c ON c.concept_id = m.tid
LEFT JOIN omop_vocab.concept_relationship r
       ON r.concept_id_1 = c.concept_id AND r.relationship_id = 'Maps to' AND r.invalid_reason IS NULL
WHERE m.map_yes = 'Yes' AND m.tid BETWEEN 1 AND 1999999999
  AND (c.standard_concept IS NULL OR c.standard_concept <> 'S' OR c.invalid_reason IS NOT NULL);

-- Standard targets missing from the vocabulary altogether
-- PASS: 0 rows
SELECT m.field_id, m.src_code, m.tid, m.tname
FROM cm m LEFT JOIN omop_vocab.concept c ON c.concept_id = m.tid
WHERE m.map_yes = 'Yes' AND m.tid BETWEEN 1 AND 1999999999 AND c.concept_id IS NULL;

-- -----------------------------------------------------------------------------
-- 3. Answer fan-out: at most one VALUE row (Meas Value) per (field, code)
--    Observation, Condition and Procedure answer rows are separate records by design
--    (e.g. mhoccur_yn 1 -> 46234759 Other health condition; paate_6hr 1/0 -> Non fasting / Fasting)
-- -----------------------------------------------------------------------------
-- PASS: 0 rows
SELECT field_id, src_code, COUNT(*) AS value_rows, COLLECT_LIST(tid) AS targets
FROM cm
WHERE map_yes = 'Yes' AND row_type = 'Answer' AND domain_id = 'Meas Value'
GROUP BY field_id, src_code
HAVING COUNT(*) > 1;

-- -----------------------------------------------------------------------------
-- 4. Question fan-out: at most one row per question per domain
-- -----------------------------------------------------------------------------
-- PASS: 0 rows (rtekgcmpdattim has 2 rows, Observation + Procedure, so it does not appear)
SELECT COALESCE(NULLIF(field_id, ''), src_code) AS field, domain_id, COUNT(*) AS n
FROM cm
WHERE map_yes = 'Yes' AND row_type = 'Question'
GROUP BY 1, 2
HAVING COUNT(*) > 1;

-- -----------------------------------------------------------------------------
-- 5. v1.8.4 changes are in place
-- -----------------------------------------------------------------------------
-- PASS (9 rows):
--   pxne16 (Question)              40192414  PPI     ips_16
--   pxne4  88 (Answer, Meas Value) 40192520  PPI     SDOH_9
--   pxne5  88 (Answer, Meas Value) 40192520  PPI     SDOH_9
--   mh_a1c (Question)              2005200014        modifier 4214376
--   mh_a1c 1 (Condition)           4214376   SNOMED  80394007  closeMatch 0.75
--   eos_dsvst 3 (Answer)           2005200589 AIREADI
--   import_buncreatinineratio      3033837   src_code 31045-8
--   import_ag_ratio                3020509   src_code 1759-0
--   import_bun_creatinine_ratio    3018311   src_code 3097-3 (v1.8.2, unchanged)
SELECT field_id, src_code, row_type, domain_id, tid, tname, vocab, tcode, predicate, confidence, modifier
FROM cm
WHERE (src_code IN ('pxne16', 'mh_a1c') AND row_type = 'Question')
   OR (field_id IN ('pxne4', 'pxne5') AND src_code = '88')
   OR (field_id = 'mh_a1c' AND domain_id = 'Condition')
   OR (field_id = 'eos_dsvst' AND src_code = '3')
   OR (field_id IN ('import_buncreatinineratio', 'import_ag_ratio', 'import_bun_creatinine_ratio') AND row_type = 'Question')
ORDER BY field_id, src_code;

-- Earlier v1.8.x fixes still in place
-- PASS: c_peptide_u 8842, urine_albumin_u 8840, rp_childpot 0 -> 42530854, cmdosu 2 -> 32912,
--       sumrjfr 777 present, NRBC rows Map_to_OMOP = No, rtekgcmpdattim Procedure 4145308
SELECT field_id, src_code, row_type, domain_id, tid, tname, map_yes
FROM cm
WHERE field_id IN ('import_c_peptide_u', 'import_urine_albumin_u', 'lbscat_nrbc_u')
   OR (field_id = 'rp_childpot' AND src_code = '0')
   OR (field_id = 'cmdosu' AND src_code = '2')
   OR (field_id = 'sumrjfr' AND src_code = '777')
   OR (src_code IN ('lbscat_nrbc', 'rtekgcmpdattim') AND row_type = 'Question')
ORDER BY field_id, src_code, domain_id;

-- -----------------------------------------------------------------------------
-- 6. Coverage: fields in the delivered data with no active map row
-- -----------------------------------------------------------------------------
-- PASS: 0 rows
CREATE OR REPLACE TEMPORARY VIEW map_fields AS
SELECT DISTINCT COALESCE(NULLIF(field_id, ''), src_code) AS field FROM cm WHERE map_yes = 'Yes';

SELECT t.tbl, t.field, COUNT(*) AS n
FROM (SELECT 'observation' AS tbl, SPLIT_PART(observation_source_value, ',', 1) AS field FROM omop_survey.observation
      UNION ALL
      SELECT 'measurement', SPLIT_PART(measurement_source_value, ',', 1) FROM omop_survey.measurement) t
LEFT JOIN map_fields f ON f.field = t.field
WHERE f.field IS NULL
GROUP BY ALL ORDER BY n DESC;

-- -----------------------------------------------------------------------------
-- 7. Answer codes in the data with no map row (coded questions only)
-- -----------------------------------------------------------------------------
-- PASS: only numeric-by-design codes (ages, years, counts, 1-6 scale midpoints:
--       sualcage, susmk*, suvp*, sumrj*, su*dosfr, pxne11, pxrd*, pdrx9).
--       eos_dsvst 3 must NOT appear (added in v1.8.4).
CREATE OR REPLACE TEMPORARY VIEW map_answers AS
SELECT DISTINCT field_id AS field, src_code AS code FROM cm WHERE row_type = 'Answer';

SELECT SPLIT_PART(o.observation_source_value, ',', 1) AS field,
       CAST(CAST(o.value_as_number AS BIGINT) AS STRING) AS code, COUNT(*) AS n
FROM omop_survey.observation o
JOIN (SELECT DISTINCT field FROM map_answers) af ON af.field = SPLIT_PART(o.observation_source_value, ',', 1)
LEFT JOIN map_answers a ON a.field = af.field AND a.code = CAST(CAST(o.value_as_number AS BIGINT) AS STRING)
WHERE o.value_as_number IS NOT NULL AND a.code IS NULL
GROUP BY ALL ORDER BY n DESC;

-- Summary of the same, by field (easier to scan)
SELECT SPLIT_PART(o.observation_source_value, ',', 1) AS field, COUNT(DISTINCT o.value_as_number) AS n_codes, COUNT(*) AS n
FROM omop_survey.observation o
JOIN (SELECT DISTINCT field FROM map_answers) af ON af.field = SPLIT_PART(o.observation_source_value, ',', 1)
LEFT JOIN map_answers a ON a.field = af.field AND a.code = CAST(CAST(o.value_as_number AS BIGINT) AS STRING)
WHERE o.value_as_number IS NOT NULL AND a.code IS NULL
GROUP BY 1 ORDER BY n DESC;

-- -----------------------------------------------------------------------------
-- 8. Units (unit lookup unchanged in v1.8.4; rerun for completeness)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW measurement_units_test AS
SELECT m.*,
       COALESCE(f.unit_concept_id, s.unit_concept_id, 0) AS test_unit_concept_id
FROM omop_survey.measurement m
LEFT JOIN redcapsurveydb.unit_concept_lookup f
       ON f.key_type = 'field'  AND f.lookup_key = TRIM(SPLIT_PART(m.measurement_source_value, ',', 1))
LEFT JOIN redcapsurveydb.unit_concept_lookup s
       ON s.key_type = 'string' AND s.lookup_key = NULLIF(TRIM(m.unit_source_value), '');

-- PASS: unit filled 86 fields / 337,169 rows; no unit 26 fields / 104,454 rows
SELECT CASE WHEN test_unit_concept_id = 0 THEN 'no unit' ELSE 'unit filled' END AS status,
       COUNT(DISTINCT SPLIT_PART(measurement_source_value, ',', 1)) AS fields, COUNT(*) AS n
FROM measurement_units_test WHERE value_as_number IS NOT NULL GROUP BY 1;

-- PASS: equal counts (no fan-out)
SELECT (SELECT COUNT(*) FROM measurement_units_test) AS view_rows,
       (SELECT COUNT(*) FROM omop_survey.measurement)  AS table_rows;

-- PASS: every map unit row's concept is in the Unit domain
SELECT m.field_id, m.src_code, m.tid, c.concept_name, c.domain_id
FROM cm m JOIN omop_vocab.concept c ON c.concept_id = m.tid
WHERE m.map_yes = 'Yes' AND m.domain_id = 'Unit' AND c.domain_id <> 'Unit';

-- -----------------------------------------------------------------------------
-- 9. Vocabulary class sanity for question and answer rows
-- -----------------------------------------------------------------------------
-- Question rows pointing at an Answer-class concept (the pxhic3 trap), and answer rows
-- pointing at a Question-class concept.
-- PASS: 0 rows
SELECT m.row_type, m.field_id, m.src_code, m.tid, c.concept_name, c.vocabulary_id, c.concept_class_id
FROM cm m JOIN omop_vocab.concept c ON c.concept_id = m.tid
WHERE m.map_yes = 'Yes'
  AND ((m.row_type = 'Question' AND c.concept_class_id = 'Answer')
    OR (m.row_type = 'Answer'   AND c.concept_class_id = 'Question'));
-- =============================================================================
