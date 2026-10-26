-- =============================================================================
-- validate_concept_map_vocab.sql
-- AI-READI concept map: check every target against the deployed OMOP vocabulary
--
-- Run before every release, after loading the mapping file as a table.
-- Dialect: Databricks / Spark SQL. Each check should return 0 rows unless noted.
--
-- Set these two names for your workspace:
--   mapping table : redcapsurveydb.ai_readi_redcap_value_set_mapping_common
--   vocabulary    : omop_vocab.concept
-- The structural checks (custom concepts, predicates, duplicates, review lists)
-- are in audit_concept_map.py in this folder.
-- =============================================================================

CREATE OR REPLACE TEMPORARY VIEW cmap AS
SELECT *,
       TRY_CAST(TRIM(CAST(TARGET_CONCEPT_ID    AS STRING)) AS BIGINT) AS tid,
       TRY_CAST(TRIM(CAST(value_as_concept_id  AS STRING)) AS BIGINT) AS vid,
       TRY_CAST(TRIM(CAST(qualifier_concept_id AS STRING)) AS BIGINT) AS qid
FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common;

-- V0. Row count (v1.4 and v1.5: 2,076; v1.6: 2,079; v1.7: 2,127; v1.8: 2,142)
SELECT COUNT(*) AS n_rows FROM cmap;

-- V1. Standard (non-custom) targets missing from the vocabulary, not standard, or invalid. Expect 0 rows.
SELECT m.tid, m.TARGET_CONCEPT_NAME, c.concept_name, c.standard_concept, c.invalid_reason,
       COUNT(*) AS n_rows, MIN(m.FIELD_ID) AS example_field
FROM cmap m
LEFT JOIN omop_vocab.concept c ON c.concept_id = m.tid
WHERE m.tid IS NOT NULL AND m.tid <> 0 AND m.tid < 2000000000
  AND (c.concept_id IS NULL OR c.standard_concept IS DISTINCT FROM 'S' OR c.invalid_reason IS NOT NULL)
GROUP BY ALL
ORDER BY m.tid;

-- V2. Name, domain, vocabulary or code in the map differ from the vocabulary. Expect 0 rows.
SELECT m.tid,
       m.TARGET_CONCEPT_NAME   AS map_name,   c.concept_name  AS vocab_name,
       m.TARGET_DOMAIN_ID      AS map_domain, c.domain_id     AS vocab_domain,
       m.TARGET_VOCABULARY_ID  AS map_vocab,  c.vocabulary_id AS vocab_vocab,
       m.TARGET_CONCEPT_CODE   AS map_code,   c.concept_code  AS vocab_code,
       COUNT(*) AS n_rows
FROM cmap m
JOIN omop_vocab.concept c ON c.concept_id = m.tid
WHERE m.tid <> 0 AND m.tid < 2000000000
  AND (TRIM(m.TARGET_CONCEPT_NAME) <> c.concept_name
       OR TRIM(m.TARGET_DOMAIN_ID) <> c.domain_id
       OR TRIM(m.TARGET_VOCABULARY_ID) <> c.vocabulary_id
       OR COALESCE(TRIM(m.TARGET_CONCEPT_CODE), '') <> c.concept_code)
GROUP BY ALL
ORDER BY m.tid;
-- Note: a domain difference is expected only where the map deliberately overrides the
-- domain (for example a Meas Value answer used as an OBSERVATION value). Review each row.

-- V3. value_as_concept_id and qualifier_concept_id: missing, non-standard or invalid. Expect 0 rows.
SELECT 'value_as_concept_id' AS col, x.id, c.concept_name, c.standard_concept, c.invalid_reason, COUNT(*) AS n_rows
FROM (SELECT vid AS id FROM cmap WHERE vid IS NOT NULL AND vid <> 0 AND vid < 2000000000) x
LEFT JOIN omop_vocab.concept c ON c.concept_id = x.id
WHERE c.concept_id IS NULL OR c.standard_concept IS DISTINCT FROM 'S' OR c.invalid_reason IS NOT NULL
GROUP BY ALL
UNION ALL
SELECT 'qualifier_concept_id', x.id, c.concept_name, c.standard_concept, c.invalid_reason, COUNT(*)
FROM (SELECT qid AS id FROM cmap WHERE qid IS NOT NULL AND qid <> 0 AND qid < 2000000000) x
LEFT JOIN omop_vocab.concept c ON c.concept_id = x.id
WHERE c.concept_id IS NULL OR c.standard_concept IS DISTINCT FROM 'S' OR c.invalid_reason IS NOT NULL
GROUP BY ALL;

-- V4. Unit and route rows point at the right domain. Expect 0 rows.
SELECT m.FIELD_ID, m.SRC_CODE, m.tid, c.concept_name, c.domain_id
FROM cmap m
JOIN omop_vocab.concept c ON c.concept_id = m.tid
WHERE (TRIM(m.TARGET_DOMAIN_ID) = 'Unit'  AND c.domain_id <> 'Unit')
   OR (TRIM(m.TARGET_DOMAIN_ID) = 'Route' AND c.domain_id <> 'Route');

-- V5. Custom concepts used as Condition targets: is there a standard SNOMED condition
-- with the same name? (Informational; review each match.)
SELECT m.FIELD_ID, m.tid AS custom_id, m.TARGET_CONCEPT_NAME,
       c.concept_id AS standard_id, c.concept_name AS standard_name, c.concept_code
FROM cmap m
JOIN omop_vocab.concept c
  ON LOWER(c.concept_name) = LOWER(TRIM(m.TARGET_CONCEPT_NAME))
 AND c.standard_concept = 'S' AND c.domain_id = 'Condition' AND c.invalid_reason IS NULL
WHERE m.tid >= 2000000000 AND TRIM(m.TARGET_DOMAIN_ID) = 'Condition';

-- -----------------------------------------------------------------------------
-- Lookups for the v1.5 candidates (informational)
-- -----------------------------------------------------------------------------

-- L1. Stroke (230690007) and kidney disease (90708001)
SELECT concept_id, concept_name, domain_id, concept_class_id, concept_code, standard_concept, invalid_reason
FROM omop_vocab.concept
WHERE vocabulary_id = 'SNOMED' AND concept_code IN ('230690007', '90708001');

-- L2. A frequency answer for "A few days (<1 day/week)" (cm_* lines 690-725)
SELECT concept_id, concept_name, concept_code
FROM omop_vocab.concept
WHERE vocabulary_id = 'LOINC' AND concept_class_id = 'Answer' AND standard_concept = 'S'
  AND (concept_name ILIKE 'less than once a week%' OR concept_name ILIKE 'less than weekly%'
       OR concept_name ILIKE 'less than 1 day%week%' OR concept_name ILIKE 'less than once per week%');

-- L3. A "route of administration" question concept for cmroute (line 331)
SELECT concept_id, concept_name, vocabulary_id, domain_id, concept_class_id, concept_code
FROM omop_vocab.concept
WHERE standard_concept = 'S' AND invalid_reason IS NULL
  AND concept_name ILIKE '%route of administration%'
  AND domain_id IN ('Observation', 'Measurement');

-- -----------------------------------------------------------------------------
-- Structural checks on the table (same as audit_concept_map.py, without line numbers;
-- rows are identified by FORM_NAME, FIELD_ID and SRC_CODE)
-- -----------------------------------------------------------------------------

-- S1. Same concept_id with different name, domain, vocabulary or code. Expect 0 rows.
SELECT tid, TRIM(TARGET_CONCEPT_NAME) AS name, TRIM(TARGET_DOMAIN_ID) AS domain,
       TRIM(TARGET_VOCABULARY_ID) AS vocab, COALESCE(TRIM(CAST(TARGET_CONCEPT_CODE AS STRING)), '') AS code,
       COUNT(*) AS n_rows
FROM cmap
WHERE tid IN (SELECT tid FROM cmap WHERE tid IS NOT NULL AND tid <> 0
              GROUP BY tid
              HAVING COUNT(DISTINCT CONCAT_WS('|', TRIM(TARGET_CONCEPT_NAME), TRIM(TARGET_DOMAIN_ID),
                                         TRIM(TARGET_VOCABULARY_ID), COALESCE(TRIM(CAST(TARGET_CONCEPT_CODE AS STRING)), ''))) > 1)
GROUP BY ALL
ORDER BY tid;

-- S2. Predicate / confidence rules. Expect 0 rows.
SELECT FORM_NAME, FIELD_ID, SRC_CODE, tid, PREDICATE_ID, CONFIDENCE,
       CASE WHEN TRIM(PREDICATE_ID) = 'skos:exactMatch' AND TRY_CAST(CONFIDENCE AS DOUBLE) <> 1 THEN 'exactMatch with confidence < 1'
            WHEN tid = 0 AND COALESCE(TRIM(PREDICATE_ID), '') <> ''                             THEN 'target 0 with a predicate'
            ELSE 'target without a predicate' END AS problem
FROM cmap
WHERE (TRIM(PREDICATE_ID) = 'skos:exactMatch' AND TRY_CAST(CONFIDENCE AS DOUBLE) <> 1)
   OR (tid = 0 AND COALESCE(TRIM(PREDICATE_ID), '') <> '')
   OR (tid IS NOT NULL AND tid <> 0 AND COALESCE(TRIM(PREDICATE_ID), '') = '');

-- S3. Leading/trailing or non-breaking spaces in key columns. Expect 0 rows.
SELECT FORM_NAME, FIELD_ID, SRC_CODE, col, val
FROM (SELECT FORM_NAME, FIELD_ID, SRC_CODE,
             STACK(5, 'FIELD_ID', FIELD_ID, 'SRC_CODE', CAST(SRC_CODE AS STRING),
                      'TARGET_CONCEPT_NAME', TARGET_CONCEPT_NAME, 'SRC_CD_DESCRIPTION', SRC_CD_DESCRIPTION,
                      'MODIFIER', CAST(MODIFIER AS STRING)) AS (col, val)
      FROM cmap)
WHERE val <> TRIM(val) OR val LIKE CONCAT('%', CHAR(160), '%');

-- S4. Custom concepts used as Condition targets: check each for a standard alternative. (Review list.)
SELECT FIELD_ID, SRC_CODE, SRC_CD_DESCRIPTION, tid, TARGET_CONCEPT_NAME
FROM cmap
WHERE tid >= 2000000000 AND TRIM(TARGET_DOMAIN_ID) = 'Condition'
ORDER BY FIELD_ID;

-- S5. Answers whose text differs from the target concept name: read each row. (Review list.)
SELECT FORM_NAME, FIELD_ID, SRC_CODE, SRC_CD_DESCRIPTION, tid, TARGET_CONCEPT_NAME, TARGET_DOMAIN_ID,
       PREDICATE_ID, CONFIDENCE
FROM cmap
WHERE TRIM(temp_Question_or_Answer) = 'Answer' AND tid IS NOT NULL AND tid <> 0 AND tid < 2000000000
  AND REGEXP_REPLACE(LOWER(SRC_CD_DESCRIPTION), '[^a-z0-9]', '') <> REGEXP_REPLACE(LOWER(TARGET_CONCEPT_NAME), '[^a-z0-9]', '')
ORDER BY FORM_NAME, FIELD_ID, SRC_CODE;

-- S6. Questions mapped to standard concepts: read each row. (Review list.)
SELECT FORM_NAME, SRC_CODE, SRC_CD_DESCRIPTION, tid, TARGET_CONCEPT_NAME, TARGET_DOMAIN_ID, PREDICATE_ID, CONFIDENCE
FROM cmap
WHERE TRIM(temp_Question_or_Answer) = 'Question' AND tid IS NOT NULL AND tid <> 0 AND tid < 2000000000
ORDER BY FORM_NAME, SRC_CODE;

-- S7. Custom targets not in the deployed vocabulary (only meaningful if the AI-READI custom
-- concepts are loaded into omop_vocab.concept; otherwise every custom ID is listed).
SELECT m.tid, MIN(m.TARGET_CONCEPT_NAME) AS map_name, COUNT(*) AS n_rows
FROM cmap m
LEFT JOIN omop_vocab.concept c ON c.concept_id = m.tid
WHERE m.tid >= 2000000000 AND c.concept_id IS NULL
GROUP BY m.tid
ORDER BY m.tid;

-- -----------------------------------------------------------------------------
-- Consistency checks between questions, answers and the vocabulary (added for v1.5 review)
-- -----------------------------------------------------------------------------

-- V6. LOINC answers that are not in the answer list of their question's LOINC concept.
-- A row here means the question and the answer come from different LOINC questions
-- (e.g. a PhenX answer used under a different question). Review each row.
WITH q AS (
  SELECT TRIM(SRC_CODE) AS field, tid AS q_id, TARGET_CONCEPT_NAME AS q_name
  FROM cmap
  WHERE TRIM(temp_Question_or_Answer) = 'Question' AND TRIM(TARGET_VOCABULARY_ID) = 'LOINC' AND tid <> 0
),
a AS (
  SELECT TRIM(FIELD_ID) AS field, TRIM(CAST(SRC_CODE AS STRING)) AS code, SRC_CD_DESCRIPTION, tid AS a_id, TARGET_CONCEPT_NAME AS a_name
  FROM cmap
  WHERE TRIM(temp_Question_or_Answer) = 'Answer' AND TRIM(TARGET_VOCABULARY_ID) = 'LOINC'
    AND TRIM(TARGET_CONCEPT_CLASS_ID) = 'Answer' AND tid <> 0
),
has_list AS (   -- questions that have any answer list in the vocabulary
  SELECT DISTINCT concept_id_1 AS q_id FROM omop_vocab.concept_relationship
  WHERE relationship_id = 'Has Answer' AND invalid_reason IS NULL
)
SELECT q.field, q.q_id, q.q_name, a.code, a.SRC_CD_DESCRIPTION, a.a_id, a.a_name,
       CASE WHEN h.q_id IS NULL THEN 'question has no LOINC answer list' ELSE 'answer not in the question''s list' END AS issue
FROM q
JOIN a ON a.field = q.field
LEFT JOIN has_list h ON h.q_id = q.q_id
LEFT JOIN omop_vocab.concept_relationship r
       ON r.concept_id_1 = q.q_id AND r.concept_id_2 = a.a_id
      AND r.relationship_id = 'Has Answer' AND r.invalid_reason IS NULL
WHERE r.concept_id_1 IS NULL
  AND a.a_id NOT IN (45877994, 45878245, 36311156, 45876636, 45878142)  -- generic Yes, No, Prefer not to say, Don't know, Other
ORDER BY issue, q.field, a.code;

-- V7. For questions in V6 with answers from another list: which LOINC question owns those answers?
SELECT a.tid AS answer_id, MIN(a.TARGET_CONCEPT_NAME) AS answer_name,
       c.concept_id AS loinc_question_id, c.concept_name AS loinc_question, c.concept_code, c.standard_concept
FROM cmap a
JOIN omop_vocab.concept_relationship r ON r.concept_id_2 = a.tid AND r.relationship_id = 'Has Answer' AND r.invalid_reason IS NULL
JOIN omop_vocab.concept c ON c.concept_id = r.concept_id_1
WHERE TRIM(a.FIELD_ID) IN ('susmkdosfr')        -- put the fields reported by V6 here
GROUP BY ALL
ORDER BY answer_id, loinc_question_id;

-- V8. Custom concepts (any domain) whose name matches a standard concept exactly (case-insensitive).
SELECT TRIM(m.temp_Question_or_Answer) AS row_type, m.FIELD_ID, m.SRC_CODE, m.tid AS custom_id, m.TARGET_CONCEPT_NAME,
       c.concept_id AS standard_id, c.concept_name AS standard_name, c.domain_id, c.vocabulary_id, c.concept_code
FROM cmap m
JOIN omop_vocab.concept c
  ON LOWER(TRIM(c.concept_name)) = LOWER(TRIM(m.TARGET_CONCEPT_NAME))
 AND c.standard_concept = 'S' AND c.invalid_reason IS NULL
WHERE m.tid >= 2000000000
ORDER BY m.tid;

-- V9. Answer rows whose FIELD_ID has no question row (field-name typos stop the ETL from linking them). Expect 0 rows,
-- apart from administrative fields with no question row.
SELECT a.FORM_NAME, a.FIELD_ID, a.SRC_CODE, a.SRC_CD_DESCRIPTION, a.tid
FROM cmap a
LEFT JOIN cmap q ON TRIM(q.temp_Question_or_Answer) = 'Question' AND TRIM(CAST(q.SRC_CODE AS STRING)) = TRIM(a.FIELD_ID)
WHERE TRIM(a.temp_Question_or_Answer) = 'Answer' AND q.SRC_CODE IS NULL
  AND TRIM(CAST(a.Map_to_OMOP AS STRING)) = 'Yes'
ORDER BY a.FIELD_ID, a.SRC_CODE;

-- V10. Procedure-domain rows (v1.7 retinal imaging: "Yes" -> PROCEDURE_OCCURRENCE). The target must be a
-- standard Procedure-domain concept, and a laterality qualifier must be a CPT4 Modifier (45888271 RT,
-- 45888270 LT), which the ETL writes to PROCEDURE_OCCURRENCE.modifier_concept_id. Expect 2 rows: the
-- monofilament "Tested" rows mssrftt and msslftt (qualifiers 4298982 / 4320144 Structure of right/left foot),
-- kept unchanged in v1.7 (monofilament redesign deferred).
SELECT m.FORM_NAME, m.FIELD_ID, m.SRC_CODE, m.tid, t.domain_id AS target_domain,
       m.qid, q.concept_name AS qualifier_name, q.concept_class_id AS qualifier_class
FROM cmap m
LEFT JOIN omop_vocab.concept t ON t.concept_id = m.tid
LEFT JOIN omop_vocab.concept q ON q.concept_id = m.qid
WHERE TRIM(m.TARGET_DOMAIN_ID) = 'Procedure'
  AND TRIM(CAST(m.Map_to_OMOP AS STRING)) = 'Yes'
  AND (   (m.tid < 2000000000 AND t.domain_id IS DISTINCT FROM 'Procedure')
       OR (m.qid IS NOT NULL AND m.qid < 2000000000 AND q.concept_class_id IS DISTINCT FROM 'CPT4 Modifier'))
ORDER BY m.FORM_NAME, m.FIELD_ID;
