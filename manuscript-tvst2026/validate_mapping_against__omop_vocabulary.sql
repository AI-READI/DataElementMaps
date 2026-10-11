-- =============================================================================
-- validate_mapping_against_vocabulary.sql
-- AI-READI REDCap -> OMOP mapping: validation against the OMOP Standardized
-- Vocabularies (Databricks SQL / Spark SQL)
--
-- Checks every standard concept referenced by the mapping file
-- (TARGET_CONCEPT_ID, qualifier_concept_id, value_as_concept_id) against the
-- vocabulary tables in the `omop_vocab` schema:
--   C1  concept exists
--   C2  concept is standard (standard_concept = 'S')
--   C3  concept is valid (invalid_reason IS NULL)
--   C4  domain_id matches TARGET_DOMAIN_ID           (target concepts only)
--   C5  vocabulary_id matches TARGET_VOCABULARY_ID   (target concepts only)
--   C6  concept_code matches TARGET_CONCEPT_CODE     (target concepts only)
--   C7  concept_name matches TARGET_CONCEPT_NAME     (target concepts only; warning)
-- For any non-standard or invalid concept, the current "Maps to" replacement is shown.
--
-- Custom AI-READI concepts (concept_id >= 2,000,000,000) are excluded from C1-C7;
-- an optional block at the end checks them if they have been loaded into omop_vocab.
--
-- BEFORE RUNNING
--   1. The mapping file is read from table ai_readi_redcap_value_set_mapping_common
--      (qualify it with <catalog>.<schema>. if needed).
--   2. If your vocabulary schema is catalog-qualified, replace `omop_vocab.`
--      with `<catalog>.omop_vocab.` throughout (find/replace).
--   3. Record the vocabulary release for the manuscript (query V0).
--   csv_line holds FIELD_ID_NUM (REDCap field number); use it with SRC_CODE to
--   locate rows in the CSV.
-- =============================================================================


-- -----------------------------------------------------------------------------
-- V0. Vocabulary release (report this version in Methods)
-- -----------------------------------------------------------------------------
SELECT vocabulary_id, vocabulary_version
FROM omop_vocab.vocabulary
WHERE vocabulary_id IN ('None', 'LOINC', 'SNOMED', 'UCUM', 'PPI', 'OMOP Extension')
ORDER BY vocabulary_id;


-- -----------------------------------------------------------------------------
-- 0. Mapping table (already loaded as ai_readi_redcap_value_set_mapping_common)
--    All columns are cast to STRING so inferred column types do not matter.
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW mapping AS
SELECT
  CAST(FIELD_ID_NUM AS STRING) AS csv_line,   -- REDCap field number, used as row reference
  CAST(Map_to_OMOP AS STRING)  AS Map_to_OMOP,
  CAST(FORM_NAME AS STRING)    AS FORM_NAME,
  CAST(FIELD_ID AS STRING)     AS FIELD_ID,
  CAST(SRC_CODE AS STRING)     AS SRC_CODE,
  CAST(SRC_CD_DESCRIPTION AS STRING)   AS SRC_CD_DESCRIPTION,
  CAST(TARGET_CONCEPT_ID AS STRING)    AS TARGET_CONCEPT_ID,
  CAST(TARGET_CONCEPT_NAME AS STRING)  AS TARGET_CONCEPT_NAME,
  CAST(TARGET_DOMAIN_ID AS STRING)     AS TARGET_DOMAIN_ID,
  CAST(TARGET_VOCABULARY_ID AS STRING) AS TARGET_VOCABULARY_ID,
  CAST(TARGET_CONCEPT_CODE AS STRING)  AS TARGET_CONCEPT_CODE,
  CAST(qualifier_concept_id AS STRING) AS qualifier_concept_id,
  CAST(value_as_concept_id AS STRING)  AS value_as_concept_id
FROM ai_readi_redcap_value_set_mapping_common;

CREATE OR REPLACE TEMP VIEW mapped_elements AS
SELECT
  csv_line,
  FORM_NAME,
  FIELD_ID,
  SRC_CODE,
  SRC_CD_DESCRIPTION,
  TRY_CAST(TRIM(TARGET_CONCEPT_ID)    AS BIGINT) AS target_concept_id,
  TRIM(TARGET_CONCEPT_NAME)                      AS target_concept_name,
  TRIM(TARGET_DOMAIN_ID)                         AS target_domain_id,
  TRIM(TARGET_VOCABULARY_ID)                     AS target_vocabulary_id,
  TRIM(TARGET_CONCEPT_CODE)                      AS target_concept_code,
  TRY_CAST(TRIM(qualifier_concept_id) AS BIGINT) AS qualifier_concept_id,
  TRY_CAST(TRIM(value_as_concept_id)  AS BIGINT) AS value_as_concept_id
FROM mapping
WHERE Map_to_OMOP = 'Yes'
  AND NULLIF(TRIM(TARGET_CONCEPT_ID), '') IS NOT NULL
  -- REDCap survey start/complete timestamps are excluded from mapped counts
  AND TRY_CAST(TRIM(TARGET_CONCEPT_ID) AS BIGINT) NOT IN (2005200558, 2005200559);


-- -----------------------------------------------------------------------------
-- 1. Every standard (non-custom) concept reference, one row per use
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW concept_refs AS
SELECT csv_line, FIELD_ID, SRC_CODE, 'TARGET_CONCEPT_ID' AS ref_column,
       target_concept_id AS concept_id,
       target_concept_name, target_domain_id, target_vocabulary_id, target_concept_code
FROM mapped_elements
WHERE target_concept_id < 2000000000
UNION ALL
SELECT csv_line, FIELD_ID, SRC_CODE, 'qualifier_concept_id',
       qualifier_concept_id, NULL, NULL, NULL, NULL
FROM mapped_elements
WHERE qualifier_concept_id IS NOT NULL AND qualifier_concept_id < 2000000000
UNION ALL
SELECT csv_line, FIELD_ID, SRC_CODE, 'value_as_concept_id',
       value_as_concept_id, NULL, NULL, NULL, NULL
FROM mapped_elements
WHERE value_as_concept_id IS NOT NULL AND value_as_concept_id < 2000000000;


-- -----------------------------------------------------------------------------
-- 2. Join to CONCEPT and evaluate checks C1-C7
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW concept_checks AS
SELECT
  r.*,
  c.concept_name        AS vocab_concept_name,
  c.domain_id           AS vocab_domain_id,
  c.vocabulary_id       AS vocab_vocabulary_id,
  c.concept_code        AS vocab_concept_code,
  c.standard_concept    AS vocab_standard_concept,
  c.invalid_reason      AS vocab_invalid_reason,
  (c.concept_id IS NULL)                                             AS c1_missing,
  (c.concept_id IS NOT NULL AND COALESCE(c.standard_concept,'') <> 'S') AS c2_not_standard,
  (c.concept_id IS NOT NULL AND c.invalid_reason IS NOT NULL)        AS c3_invalid,
  (r.ref_column = 'TARGET_CONCEPT_ID' AND c.concept_id IS NOT NULL
     AND COALESCE(r.target_domain_id,'')     <> c.domain_id)         AS c4_domain_mismatch,
  (r.ref_column = 'TARGET_CONCEPT_ID' AND c.concept_id IS NOT NULL
     AND COALESCE(r.target_vocabulary_id,'') <> c.vocabulary_id)     AS c5_vocabulary_mismatch,
  (r.ref_column = 'TARGET_CONCEPT_ID' AND c.concept_id IS NOT NULL
     AND NULLIF(r.target_concept_code,'') IS NOT NULL
     AND r.target_concept_code <> c.concept_code)                    AS c6_code_mismatch,
  (r.ref_column = 'TARGET_CONCEPT_ID' AND c.concept_id IS NOT NULL
     AND LOWER(TRIM(COALESCE(r.target_concept_name,''))) <> LOWER(TRIM(c.concept_name))) AS c7_name_mismatch
FROM concept_refs r
LEFT JOIN omop_vocab.concept c
  ON c.concept_id = r.concept_id;


-- -----------------------------------------------------------------------------
-- 3. Summary: number of references and distinct concepts failing each check
--    (C1-C6 should all be 0; C7 is a warning - review the listed names)
-- -----------------------------------------------------------------------------
SELECT check_name,
       SUM(CASE WHEN failed THEN 1 ELSE 0 END)                   AS failing_references,
       COUNT(DISTINCT CASE WHEN failed THEN concept_id END)      AS failing_distinct_concepts,
       COUNT(*)                                                  AS references_checked,
       COUNT(DISTINCT concept_id)                                AS distinct_concepts_checked
FROM (
  SELECT 'C1 concept exists'        AS check_name, concept_id, c1_missing             AS failed FROM concept_checks
  UNION ALL SELECT 'C2 standard',                  concept_id, c2_not_standard               FROM concept_checks
  UNION ALL SELECT 'C3 valid (not deprecated)',    concept_id, c3_invalid                    FROM concept_checks
  UNION ALL SELECT 'C4 domain matches',            concept_id, c4_domain_mismatch            FROM concept_checks WHERE ref_column = 'TARGET_CONCEPT_ID'
  UNION ALL SELECT 'C5 vocabulary matches',        concept_id, c5_vocabulary_mismatch        FROM concept_checks WHERE ref_column = 'TARGET_CONCEPT_ID'
  UNION ALL SELECT 'C6 concept code matches',      concept_id, c6_code_mismatch              FROM concept_checks WHERE ref_column = 'TARGET_CONCEPT_ID'
  UNION ALL SELECT 'C7 concept name matches (warn)', concept_id, c7_name_mismatch            FROM concept_checks WHERE ref_column = 'TARGET_CONCEPT_ID'
) t
GROUP BY check_name
ORDER BY check_name;
-- Expected references checked for TARGET_CONCEPT_ID: 1,413 rows / 381 distinct concepts.


-- -----------------------------------------------------------------------------
-- 4. Detail: every failing row, with the current "Maps to" replacement
--    for non-standard / deprecated concepts
-- -----------------------------------------------------------------------------
SELECT
  k.csv_line,
  k.FIELD_ID,
  k.SRC_CODE,
  k.ref_column,
  k.concept_id,
  CONCAT_WS('; ',
    CASE WHEN k.c1_missing             THEN 'C1 missing'         END,
    CASE WHEN k.c2_not_standard        THEN 'C2 not standard'    END,
    CASE WHEN k.c3_invalid             THEN CONCAT('C3 invalid (', k.vocab_invalid_reason, ')') END,
    CASE WHEN k.c4_domain_mismatch     THEN CONCAT('C4 domain: file=', k.target_domain_id, ' vocab=', k.vocab_domain_id) END,
    CASE WHEN k.c5_vocabulary_mismatch THEN CONCAT('C5 vocab: file=', k.target_vocabulary_id, ' vocab=', k.vocab_vocabulary_id) END,
    CASE WHEN k.c6_code_mismatch       THEN CONCAT('C6 code: file=', k.target_concept_code, ' vocab=', k.vocab_concept_code) END,
    CASE WHEN k.c7_name_mismatch       THEN 'C7 name differs'    END
  )                                   AS issues,
  k.target_concept_name               AS file_concept_name,
  k.vocab_concept_name,
  m.concept_id_2                      AS maps_to_concept_id,
  c2.concept_name                     AS maps_to_concept_name,
  c2.domain_id                        AS maps_to_domain_id
FROM concept_checks k
LEFT JOIN omop_vocab.concept_relationship m
  ON  m.concept_id_1    = k.concept_id
  AND m.relationship_id = 'Maps to'
  AND m.invalid_reason IS NULL
  AND (k.c2_not_standard OR k.c3_invalid)
LEFT JOIN omop_vocab.concept c2
  ON c2.concept_id = m.concept_id_2
WHERE k.c1_missing OR k.c2_not_standard OR k.c3_invalid
   OR k.c4_domain_mismatch OR k.c5_vocabulary_mismatch
   OR k.c6_code_mismatch OR k.c7_name_mismatch
ORDER BY
  CASE WHEN k.c1_missing OR k.c2_not_standard OR k.c3_invalid THEN 1
       WHEN k.c4_domain_mismatch OR k.c5_vocabulary_mismatch OR k.c6_code_mismatch THEN 2
       ELSE 3 END,
  k.csv_line;


-- -----------------------------------------------------------------------------
-- 5. Laterality qualifiers: confirm the four concepts are valid
--    (expected: 45876703 Right eye, 45883829 Left eye,
--               4298982 Structure of right foot, 4320144 Structure of left foot)
-- -----------------------------------------------------------------------------
SELECT c.concept_id, c.concept_name, c.domain_id, c.vocabulary_id,
       c.standard_concept, c.invalid_reason,
       COUNT(*) AS rows_using_it
FROM mapped_elements e
JOIN omop_vocab.concept c ON c.concept_id = e.qualifier_concept_id
WHERE e.qualifier_concept_id IN (45876703, 45883829, 4298982, 4320144)
GROUP BY c.concept_id, c.concept_name, c.domain_id, c.vocabulary_id,
         c.standard_concept, c.invalid_reason
ORDER BY c.concept_id;
-- Expected rows_using_it: 78, 78, 2, 2.


-- -----------------------------------------------------------------------------
-- 6. OPTIONAL: custom AI-READI concepts (only if loaded into omop_vocab.concept)
--    Lists custom target concepts that are missing or whose name differs.
-- -----------------------------------------------------------------------------
SELECT e.csv_line, e.FIELD_ID, e.target_concept_id, e.target_concept_name,
       c.concept_name AS vocab_concept_name, c.vocabulary_id AS vocab_vocabulary_id,
       CASE WHEN c.concept_id IS NULL THEN 'missing'
            WHEN LOWER(TRIM(c.concept_name)) <> LOWER(TRIM(e.target_concept_name)) THEN 'name differs'
            WHEN c.vocabulary_id <> e.target_vocabulary_id THEN 'vocabulary differs'
       END AS issue
FROM mapped_elements e
LEFT JOIN omop_vocab.concept c ON c.concept_id = e.target_concept_id
WHERE e.target_concept_id >= 2000000000
  AND (c.concept_id IS NULL
       OR LOWER(TRIM(c.concept_name)) <> LOWER(TRIM(e.target_concept_name))
       OR c.vocabulary_id <> e.target_vocabulary_id)
ORDER BY e.csv_line;
