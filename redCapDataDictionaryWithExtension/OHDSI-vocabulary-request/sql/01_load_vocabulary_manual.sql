-- =============================================================================
-- 01_load_vocabulary_manual.sql
-- AI-READI custom vocabulary: load concept_manual.csv and concept_relationship_manual.csv,
-- build the three vocabulary splits of both files, and check that the split CSV files in
-- AI-READI-Vocabulary/ match them.
--
-- Dialect: Databricks / Spark SQL. READ-ONLY: SELECT and TEMPORARY VIEWs only.
-- Every column is read as text (STRING). Line 2 of both main files is a blank row (kept so
-- line numbers do not shift); it is filtered out below.
--
-- Set the paths to your copies of the files, then run once per session before
-- 02_validate_concept_relationship_manual.sql. Run each check in its own cell
-- (Databricks shows only the last result of a cell).
-- =============================================================================

-- Source files ---------------------------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW concept_manual_file
USING csv OPTIONS (path '/Volumes/<catalog>/<schema>/<volume>/concept_manual.csv',               -- <-- set this
                   header 'true', encoding 'UTF-8', multiLine 'true');

CREATE OR REPLACE TEMPORARY VIEW concept_relationship_manual_file
USING csv OPTIONS (path '/Volumes/<catalog>/<schema>/<volume>/concept_relationship_manual.csv',  -- <-- set this
                   header 'true', encoding 'UTF-8', multiLine 'true');

CREATE OR REPLACE TEMPORARY VIEW split_aireadi_file
USING csv OPTIONS (path '/Volumes/<catalog>/<schema>/<volume>/concept_manual_AIREADI.csv',        -- <-- set this
                   header 'true', encoding 'UTF-8', multiLine 'true');

CREATE OR REPLACE TEMPORARY VIEW split_moca_file
USING csv OPTIONS (path '/Volumes/<catalog>/<schema>/<volume>/concept_manual_AIREADI-MOCA.csv',   -- <-- set this
                   header 'true', encoding 'UTF-8', multiLine 'true');

CREATE OR REPLACE TEMPORARY VIEW split_vision_file
USING csv OPTIONS (path '/Volumes/<catalog>/<schema>/<volume>/concept_manual_AIREADI-Vision.csv', -- <-- set this
                   header 'true', encoding 'UTF-8', multiLine 'true');

CREATE OR REPLACE TEMPORARY VIEW rel_split_aireadi_file
USING csv OPTIONS (path '/Volumes/<catalog>/<schema>/<volume>/concept_relationship_manual_AIREADI.csv',        -- <-- set this
                   header 'true', encoding 'UTF-8', multiLine 'true');

CREATE OR REPLACE TEMPORARY VIEW rel_split_moca_file
USING csv OPTIONS (path '/Volumes/<catalog>/<schema>/<volume>/concept_relationship_manual_AIREADI-MOCA.csv',   -- <-- set this
                   header 'true', encoding 'UTF-8', multiLine 'true');

CREATE OR REPLACE TEMPORARY VIEW rel_split_vision_file
USING csv OPTIONS (path '/Volumes/<catalog>/<schema>/<volume>/concept_relationship_manual_AIREADI-Vision.csv', -- <-- set this
                   header 'true', encoding 'UTF-8', multiLine 'true');

-- Alternative: if the files are already loaded as tables, point the views at them instead, e.g.
-- CREATE OR REPLACE TEMPORARY VIEW concept_manual_file AS SELECT * FROM <catalog>.<schema>.concept_manual;

-- Main views (blank rows removed) --------------------------------------------
CREATE OR REPLACE TEMPORARY VIEW concept_manual AS
SELECT * FROM concept_manual_file WHERE TRIM(COALESCE(concept_id, '')) <> '';

CREATE OR REPLACE TEMPORARY VIEW concept_relationship_manual AS
SELECT * FROM concept_relationship_manual_file WHERE TRIM(COALESCE(concept_id_1, '')) <> '';

-- Splits generated from concept_manual (one per vocabulary_id) -----------------
CREATE OR REPLACE TEMPORARY VIEW concept_manual_aireadi AS
SELECT * FROM concept_manual WHERE TRIM(vocabulary_id) = 'AIREADI';

CREATE OR REPLACE TEMPORARY VIEW concept_manual_aireadi_moca AS
SELECT * FROM concept_manual WHERE TRIM(vocabulary_id) = 'AIREADI-MOCA';

CREATE OR REPLACE TEMPORARY VIEW concept_manual_aireadi_vision AS
SELECT * FROM concept_manual WHERE TRIM(vocabulary_id) = 'AIREADI-Vision';

-- L1. Counts. v1.8.7: concept_manual 419 (AIREADI 335, AIREADI-MOCA 30, AIREADI-Vision 54),
--     standard_concept S 407, deprecated U 9, D 3;
--     concept_relationship_manual 428 (AIREADI 344, AIREADI-MOCA 30, AIREADI-Vision 54)
SELECT 'concept_manual' AS file, COUNT(*) AS n FROM concept_manual
UNION ALL SELECT 'concept_manual AIREADI', COUNT(*) FROM concept_manual_aireadi
UNION ALL SELECT 'concept_manual AIREADI-MOCA', COUNT(*) FROM concept_manual_aireadi_moca
UNION ALL SELECT 'concept_manual AIREADI-Vision', COUNT(*) FROM concept_manual_aireadi_vision
UNION ALL SELECT 'concept_manual invalid_reason U', COUNT(*) FROM concept_manual WHERE TRIM(invalid_reason) = 'U'
UNION ALL SELECT 'concept_manual invalid_reason D', COUNT(*) FROM concept_manual WHERE TRIM(invalid_reason) = 'D'
UNION ALL SELECT 'concept_manual standard_concept S', COUNT(*) FROM concept_manual WHERE TRIM(standard_concept) = 'S'
UNION ALL SELECT 'concept_relationship_manual', COUNT(*) FROM concept_relationship_manual
UNION ALL SELECT 'concept_relationship_manual AIREADI', COUNT(*) FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI'
UNION ALL SELECT 'concept_relationship_manual AIREADI-MOCA', COUNT(*) FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI-MOCA'
UNION ALL SELECT 'concept_relationship_manual AIREADI-Vision', COUNT(*) FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI-Vision';

-- L2. concept_manual: every vocabulary_id belongs to a split; concept_id unique; SRC_CODE unique among valid
--     concepts (a deprecated concept may share it with its successor; 72 header concepts have no SRC_CODE);
--     standard_concept is S exactly when invalid_reason is blank (deprecated concepts are not standard)
-- PASS: 0 rows
SELECT 'vocabulary_id not in a split' AS issue, concept_id, vocabulary_id AS value FROM concept_manual
WHERE TRIM(vocabulary_id) NOT IN ('AIREADI', 'AIREADI-MOCA', 'AIREADI-Vision')
UNION ALL
SELECT 'duplicate concept_id', concept_id, CAST(COUNT(*) AS STRING) FROM concept_manual GROUP BY concept_id HAVING COUNT(*) > 1
UNION ALL
SELECT 'duplicate SRC_CODE among valid concepts', MAX(concept_id), SRC_CODE FROM concept_manual
WHERE COALESCE(TRIM(invalid_reason), '') = '' AND COALESCE(TRIM(SRC_CODE), '') <> ''
GROUP BY SRC_CODE HAVING COUNT(*) > 1
UNION ALL
SELECT 'standard_concept does not follow invalid_reason', concept_id,
       CONCAT('standard_concept=', COALESCE(standard_concept, ''), ' invalid_reason=', COALESCE(invalid_reason, ''))
FROM concept_manual
WHERE COALESCE(TRIM(standard_concept), '') <> CASE WHEN COALESCE(TRIM(invalid_reason), '') = '' THEN 'S' ELSE '' END;

-- L3. Split CSV files match the splits generated from concept_manual (all 11 columns, both directions)
-- PASS: 0 rows
SELECT 'AIREADI: only in split file' AS issue, * FROM (SELECT * FROM split_aireadi_file WHERE TRIM(COALESCE(concept_id, '')) <> ''
                                                     EXCEPT ALL SELECT * FROM concept_manual_aireadi)
UNION ALL
SELECT 'AIREADI: only in concept_manual', * FROM (SELECT * FROM concept_manual_aireadi
                                                 EXCEPT ALL SELECT * FROM split_aireadi_file WHERE TRIM(COALESCE(concept_id, '')) <> '')
UNION ALL
SELECT 'AIREADI-MOCA: only in split file', * FROM (SELECT * FROM split_moca_file WHERE TRIM(COALESCE(concept_id, '')) <> ''
                                                  EXCEPT ALL SELECT * FROM concept_manual_aireadi_moca)
UNION ALL
SELECT 'AIREADI-MOCA: only in concept_manual', * FROM (SELECT * FROM concept_manual_aireadi_moca
                                                      EXCEPT ALL SELECT * FROM split_moca_file WHERE TRIM(COALESCE(concept_id, '')) <> '')
UNION ALL
SELECT 'AIREADI-Vision: only in split file', * FROM (SELECT * FROM split_vision_file WHERE TRIM(COALESCE(concept_id, '')) <> ''
                                                    EXCEPT ALL SELECT * FROM concept_manual_aireadi_vision)
UNION ALL
SELECT 'AIREADI-Vision: only in concept_manual', * FROM (SELECT * FROM concept_manual_aireadi_vision
                                                        EXCEPT ALL SELECT * FROM split_vision_file WHERE TRIM(COALESCE(concept_id, '')) <> '');

-- L4. concept_relationship_manual agrees with concept_manual on name, SRC_CODE and vocabulary
-- PASS: 0 rows
SELECT r.concept_id_1, r.concept_name AS rel_name, m.concept_name AS manual_name,
       r.SRC_CODE AS rel_src_code, m.SRC_CODE AS manual_src_code,
       r.vocabulary_id_1, m.vocabulary_id
FROM concept_relationship_manual r
JOIN concept_manual m ON TRIM(m.concept_id) = TRIM(r.concept_id_1)
WHERE TRIM(r.concept_name) <> TRIM(m.concept_name)
   OR TRIM(r.SRC_CODE) <> TRIM(m.SRC_CODE)
   OR TRIM(r.vocabulary_id_1) <> TRIM(m.vocabulary_id);

-- L5. Relationship split CSV files match concept_relationship_manual split by vocabulary_id_1 (all columns, both directions)
-- PASS: 0 rows
SELECT 'AIREADI: only in split file' AS issue, * FROM (SELECT * FROM rel_split_aireadi_file
                                                     EXCEPT ALL SELECT * FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI')
UNION ALL
SELECT 'AIREADI: only in main file', * FROM (SELECT * FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI'
                                            EXCEPT ALL SELECT * FROM rel_split_aireadi_file)
UNION ALL
SELECT 'AIREADI-MOCA: only in split file', * FROM (SELECT * FROM rel_split_moca_file
                                                  EXCEPT ALL SELECT * FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI-MOCA')
UNION ALL
SELECT 'AIREADI-MOCA: only in main file', * FROM (SELECT * FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI-MOCA'
                                                 EXCEPT ALL SELECT * FROM rel_split_moca_file)
UNION ALL
SELECT 'AIREADI-Vision: only in split file', * FROM (SELECT * FROM rel_split_vision_file
                                                    EXCEPT ALL SELECT * FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI-Vision')
UNION ALL
SELECT 'AIREADI-Vision: only in main file', * FROM (SELECT * FROM concept_relationship_manual WHERE TRIM(vocabulary_id_1) = 'AIREADI-Vision'
                                                   EXCEPT ALL SELECT * FROM rel_split_vision_file);
-- =============================================================================
