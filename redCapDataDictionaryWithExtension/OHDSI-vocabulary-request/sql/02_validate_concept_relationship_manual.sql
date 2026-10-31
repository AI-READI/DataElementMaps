-- =============================================================================
-- 02_validate_concept_relationship_manual.sql
-- Validate concept_relationship_manual.csv against the OMOP vocabulary (omop_vocab) and concept_manual.csv
-- Databricks / Spark SQL. READ-ONLY: SELECT and TEMPORARY VIEWs only.
--
-- Run 01_load_vocabulary_manual.sql first (it creates the views concept_manual and
-- concept_relationship_manual). Run each check in its own cell (Databricks shows only the
-- last result of a cell). Set omop_vocab to your vocabulary schema if it is named differently.
--
-- relationship_id rules (predicate_id keeps the SKOS mapping in every row):
--   Maps to / Concept replaced by : deprecated custom concept (invalid_reason U) -> its replacement (standard)
--   Is a                          : skos:broadMatch to a standard or classification concept in the same domain
--   blank (SKOS only)             : every other row, including cross-domain links and exact matches
--                                   to non-standard concepts
-- =============================================================================

CREATE OR REPLACE TEMPORARY VIEW rel AS
SELECT TRIM(concept_id_1) AS id1, concept_name AS name1, TRIM(relationship_id) AS rel,
       CAST(NULLIF(TRIM(concept_id_2), '') AS BIGINT) AS id2,
       `temp name` AS name2, TRIM(`temp domain`) AS dom2, TRIM(vocabulary_id_2) AS voc2,
       TRIM(concept_code_2) AS code2, TRIM(`temp standard`) AS std2, TRIM(predicate_id) AS pred
FROM concept_relationship_manual
WHERE TRIM(concept_id_1) <> '';

CREATE OR REPLACE TEMPORARY VIEW man AS
SELECT TRIM(concept_id) AS id1, concept_name, TRIM(domain_id) AS dom1
FROM concept_manual WHERE TRIM(concept_id) <> '';

-- R0. Coverage: every concept in concept_manual has a relationship row, no extras, no duplicates;
--     deprecated (U) concepts have both a Maps to and a Concept replaced by row
-- PASS: 0 rows
SELECT 'missing row' AS issue, m.id1, m.concept_name FROM man m LEFT JOIN rel r ON r.id1 = m.id1 WHERE r.id1 IS NULL
UNION ALL
SELECT 'not in concept_manual', r.id1, r.name1 FROM rel r LEFT JOIN man m ON m.id1 = r.id1 WHERE m.id1 IS NULL
UNION ALL
SELECT 'duplicate', id1, MAX(name1) FROM rel GROUP BY id1, rel HAVING COUNT(*) > 1
UNION ALL
SELECT 'U concept without both Maps to and Concept replaced by', id1, MAX(name1) FROM rel
WHERE id1 IN (SELECT id1 FROM rel WHERE rel IN ('Maps to', 'Concept replaced by'))
GROUP BY id1 HAVING COUNT(DISTINCT rel) <> 2;

-- R1. Every related concept exists and is valid
-- PASS: 0 rows
SELECT r.id1, r.rel, r.pred, r.id2, r.name2, c.concept_id IS NULL AS missing, c.invalid_reason
FROM rel r LEFT JOIN omop_vocab.concept c ON c.concept_id = r.id2
WHERE r.id2 IS NOT NULL AND (c.concept_id IS NULL OR c.invalid_reason IS NOT NULL);

-- R2. 'Maps to' / 'Concept replaced by' targets are standard; 'Is a' targets are standard or classification
-- PASS: 0 rows
SELECT r.id1, r.name1, r.rel, r.id2, c.concept_name, c.standard_concept, c.domain_id
FROM rel r JOIN omop_vocab.concept c ON c.concept_id = r.id2
WHERE (r.rel IN ('Maps to', 'Concept replaced by') AND c.standard_concept IS DISTINCT FROM 'S')
   OR (r.rel = 'Is a'    AND COALESCE(c.standard_concept, '') NOT IN ('S', 'C'));

-- R3. 'Is a' only within one domain (custom concept domain = target domain in the vocabulary)
-- PASS: 0 rows
SELECT r.id1, r.name1, m.dom1 AS custom_domain, r.id2, c.concept_name, c.domain_id AS target_domain
FROM rel r JOIN man m ON m.id1 = r.id1 JOIN omop_vocab.concept c ON c.concept_id = r.id2
WHERE r.rel = 'Is a' AND m.dom1 <> c.domain_id;

-- R4. Name, domain, vocabulary, code and standard flag recorded in the file match the vocabulary
-- Review: differences are documentation fixes (no effect on the relationship)
SELECT r.id1, r.id2,
       CASE WHEN TRIM(r.name2) <> c.concept_name THEN CONCAT('name: ', r.name2, ' -> ', c.concept_name) END AS name_diff,
       CASE WHEN r.dom2  <> c.domain_id     THEN CONCAT(r.dom2, ' -> ', c.domain_id) END     AS domain_diff,
       CASE WHEN r.voc2  <> c.vocabulary_id THEN CONCAT(r.voc2, ' -> ', c.vocabulary_id) END AS vocab_diff,
       CASE WHEN r.code2 <> c.concept_code  THEN CONCAT(r.code2, ' -> ', c.concept_code) END AS code_diff,
       CASE WHEN COALESCE(r.std2, '') <> COALESCE(c.standard_concept, '') THEN CONCAT(COALESCE(r.std2, '(blank)'), ' -> ', COALESCE(c.standard_concept, '(blank)')) END AS std_diff
FROM rel r JOIN omop_vocab.concept c ON c.concept_id = r.id2
WHERE TRIM(r.name2) <> c.concept_name OR r.dom2 <> c.domain_id OR r.voc2 <> c.vocabulary_id
   OR r.code2 <> c.concept_code OR COALESCE(r.std2, '') <> COALESCE(c.standard_concept, '')
ORDER BY r.id1;

-- R5. Related concepts that are NOT standard: their current standard via 'Maps to'
-- Review: candidates to replace concept_id_2 (then the row's rule is re-evaluated). v1.8.7: 24 rows, no change needed
SELECT r.id1, r.name1, r.rel, r.pred, r.id2, c.concept_name, c.vocabulary_id, c.standard_concept,
       cr.concept_id_2 AS maps_to_id, c2.concept_name AS maps_to_name, c2.domain_id AS maps_to_domain
FROM rel r
JOIN omop_vocab.concept c ON c.concept_id = r.id2
LEFT JOIN omop_vocab.concept_relationship cr
       ON cr.concept_id_1 = c.concept_id AND cr.relationship_id = 'Maps to' AND cr.invalid_reason IS NULL
LEFT JOIN omop_vocab.concept c2 ON c2.concept_id = cr.concept_id_2
WHERE c.standard_concept IS DISTINCT FROM 'S'
ORDER BY r.id1;

-- R6. Summary (v1.8.7: Is a 109, Maps to 9, Concept replaced by 9, SKOS only 301)
SELECT COALESCE(NULLIF(rel, ''), '(SKOS only)') AS relationship_id, pred, COUNT(*) AS n
FROM rel GROUP BY 1, 2 ORDER BY 1, 3 DESC;

-- R7. Deprecated concepts in concept_manual: U has a replacement, D has none
-- PASS: 0 rows
SELECT m.id1, m.concept_name, TRIM(cm.invalid_reason) AS invalid_reason,
       SUM(CASE WHEN r.rel = 'Maps to' THEN 1 ELSE 0 END) AS maps_to_rows
FROM man m
JOIN concept_manual cm ON TRIM(cm.concept_id) = m.id1
LEFT JOIN rel r ON r.id1 = m.id1
GROUP BY 1, 2, 3
HAVING (invalid_reason = 'U' AND maps_to_rows <> 1) OR (invalid_reason = 'D' AND maps_to_rows <> 0)
    OR (COALESCE(invalid_reason, '') = '' AND maps_to_rows > 0);
-- =============================================================================
