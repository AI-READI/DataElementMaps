-- =============================================================================
-- count_mapping_concepts.sql
-- AI-READI REDCap -> OMOP CDM mapping: element and concept counts
--
-- Reproduces the counts reported in the manuscript (Table 2, Results, Abstract)
-- from the mapping file:
--     ai_readi_redcap_value_set_mapping_common.csv
--
-- Dialect: DuckDB (>= 0.10). Run with:
--     duckdb -c ".read count_mapping_concepts.sql"
-- or set the file path below and run in the DuckDB CLI.
-- For PostgreSQL, load the CSV into a table named `mapping` (all columns TEXT)
-- and run the queries from section 1 onward unchanged.
--
-- Counting rules
--   * Designated for mapping   : Map_to_OMOP = 'Yes'
--   * Mapped                   : designated AND TARGET_CONCEPT_ID populated
--   * Custom (AI-READI) concept: TARGET_CONCEPT_ID >= 2,000,000,000
--   * Standard concept         : TARGET_CONCEPT_ID <  2,000,000,000
--   * Excluded from mapped counts: REDCap survey start/complete timestamps
--     (custom concepts 2005200558 "Survey Started Timestamp" and
--      2005200559 "Survey Completed Timestamp"); these are REDCap system
--     metadata, not survey content, and are reported as designated-but-unmapped.
--   * Not designated (902) = REDCap data elements in the curated dictionary
--     (2,906) that are not rows in this mapping file.
-- =============================================================================

-- 0. Load ------------------------------------------------------------------------
CREATE OR REPLACE TABLE mapping AS
SELECT *
FROM read_csv('ai_readi_redcap_value_set_mapping_common.csv',
              header = true, all_varchar = true);

-- Constants
CREATE OR REPLACE MACRO total_curated_elements() AS 2906;   -- curated REDCap data dictionary
CREATE OR REPLACE MACRO custom_floor()           AS 2000000000;

-- Classified view ------------------------------------------------------------------
CREATE OR REPLACE VIEW mapping_classified AS
SELECT
    m.*,
    TRY_CAST(NULLIF(TRIM(TARGET_CONCEPT_ID), '') AS BIGINT) AS target_id,
    CASE
        WHEN Map_to_OMOP <> 'Yes'                                        THEN 'Designated but unmapped'
        WHEN NULLIF(TRIM(TARGET_CONCEPT_ID), '') IS NULL                 THEN 'Designated but unmapped'
        WHEN TRY_CAST(TARGET_CONCEPT_ID AS BIGINT) IN (2005200558, 2005200559)
                                                                         THEN 'Designated but unmapped'
        WHEN TRY_CAST(TARGET_CONCEPT_ID AS BIGINT) >= custom_floor()     THEN 'Custom'
        ELSE                                                                  'Standard'
    END AS mapping_category,
    CASE
        WHEN TRY_CAST(TARGET_CONCEPT_ID AS BIGINT) IN (2005200558, 2005200559)
                                                                    THEN 'REDCap survey timestamp'
        WHEN Map_to_OMOP <> 'Yes' AND SRC_CODE LIKE 'moca_paper%'   THEN 'MoCA paper-administration flag'
        WHEN NULLIF(TRIM(TARGET_CONCEPT_ID), '') IS NOT NULL         THEN NULL
        WHEN FIELD_ID LIKE 'import\_%\_min%' ESCAPE '\'
          OR FIELD_ID LIKE 'import\_%\_max%' ESCAPE '\'             THEN 'Laboratory reference range'
        WHEN FIELD_ID LIKE 'import\_collection\_dt%' ESCAPE '\'
          OR FIELD_ID LIKE 'import\_process\_dt%'    ESCAPE '\'
          OR FIELD_ID LIKE 'import\_notes%'          ESCAPE '\'     THEN 'Specimen handling'
        WHEN FORM_NAME = 'bcva'                                     THEN 'BCVA not-done / sign modifier'
        WHEN FORM_NAME = 'device_return'                            THEN 'REDCap administrative'
        ELSE                                                             'Other'
    END AS unmapped_reason
FROM mapping m;

-- 1. Coverage summary (Table 2) -------------------------------------------------------
WITH c AS (
    SELECT mapping_category, COUNT(*) AS n,
           NULLIF(COUNT(DISTINCT CASE WHEN mapping_category IN ('Standard','Custom')
                                      THEN target_id END), 0) AS distinct_concepts
    FROM mapping_classified
    GROUP BY mapping_category
),
rows AS (
    SELECT mapping_category, n, distinct_concepts FROM c
    UNION ALL
    SELECT 'Mapped total', SUM(n),
           (SELECT COUNT(DISTINCT target_id) FROM mapping_classified
             WHERE mapping_category IN ('Standard','Custom'))
    FROM c WHERE mapping_category IN ('Standard','Custom')
    UNION ALL
    SELECT 'Not designated', total_curated_elements() - (SELECT COUNT(*) FROM mapping), NULL
    UNION ALL
    SELECT 'Total curated elements', total_curated_elements(), NULL
)
SELECT mapping_category AS category,
       n,
       ROUND(100.0 * n / total_curated_elements(), 1) AS pct_of_2906,
       distinct_concepts
FROM rows
ORDER BY CASE category
           WHEN 'Standard' THEN 1 WHEN 'Custom' THEN 2 WHEN 'Mapped total' THEN 3
           WHEN 'Designated but unmapped' THEN 4 WHEN 'Not designated' THEN 5 ELSE 6 END;
-- Expected: Standard 1,413 (48.6%) / 381; Custom 487 (16.8%) / 342;
--           Mapped 1,900 (65.4%) / 723; Designated-unmapped 104 (3.6%);
--           Not designated 902 (31.0%); Total 2,906.

-- 2. Elements and distinct concepts by vocabulary ----------------------------------
SELECT mapping_category,
       TARGET_VOCABULARY_ID           AS vocabulary,
       COUNT(*)                       AS elements,
       COUNT(DISTINCT target_id)      AS distinct_concepts
FROM mapping_classified
WHERE mapping_category IN ('Standard','Custom')
GROUP BY mapping_category, TARGET_VOCABULARY_ID
ORDER BY mapping_category DESC, elements DESC;
-- Expected: LOINC 1,200/281; SNOMED 138/71; UCUM 69/23; PPI 5/5; OMOP Extension 1/1;
--           AIREADI 388/265; AIREADI-Vision 69/47; AIREADI-MOCA 30/30.

-- 3. Designated-but-unmapped breakdown -------------------------------------------------
SELECT unmapped_reason, COUNT(*) AS n
FROM mapping_classified
WHERE mapping_category = 'Designated but unmapped'
GROUP BY unmapped_reason
ORDER BY n DESC;
-- Expected: reference range 46; survey timestamp 34; specimen handling 12;
--           BCVA 10; REDCap administrative 1; MoCA paper flag 1 (total 104).

-- 4. Confidence and SKOS predicate distribution -----------------------------------------
SELECT mapping_category,
       PREDICATE_ID,
       CONFIDENCE,
       COUNT(*) AS n
FROM mapping_classified
WHERE mapping_category IN ('Standard','Custom')
GROUP BY mapping_category, PREDICATE_ID, CONFIDENCE
ORDER BY mapping_category DESC, PREDICATE_ID, CONFIDENCE DESC;
-- Expected (standard): exact 1,173; close 237; related 3;
--                      confidence 1.0 = 1,327; 0.75 = 84; 0.5 = 2.
-- Expected (custom):   all 487 exact match at confidence 1.0.

-- 5. Laterality qualifiers ---------------------------------------------------------------
SELECT qualifier_concept_id, qualifier_source_value, COUNT(*) AS n
FROM mapping_classified
WHERE mapping_category IN ('Standard','Custom')
  AND qualifier_concept_id IN ('45876703','45883829','4298982','4320144')
GROUP BY qualifier_concept_id, qualifier_source_value
ORDER BY qualifier_concept_id;
-- Expected: Right eye 78; Left eye 78; Structure of right foot 2; Structure of left foot 2.

-- 6. Integrity checks (each should return 0 rows) ---------------------------------------
-- 6a. Custom concepts missing LOCAL_CONCEPT_ID
SELECT 'custom_missing_local_id' AS check_name, FIELD_ID, SRC_CODE, TARGET_CONCEPT_ID
FROM mapping_classified
WHERE mapping_category = 'Custom' AND NULLIF(TRIM(LOCAL_CONCEPT_ID), '') IS NULL;

-- 6b. Mapped rows missing predicate or confidence
SELECT 'mapped_missing_predicate_or_confidence' AS check_name, FIELD_ID, SRC_CODE
FROM mapping_classified
WHERE mapping_category IN ('Standard','Custom')
  AND (NULLIF(TRIM(PREDICATE_ID), '') IS NULL OR NULLIF(TRIM(CONFIDENCE), '') IS NULL);

-- 6c. Custom concept IDs whose vocabulary is not an AI-READI vocabulary
SELECT 'custom_wrong_vocabulary' AS check_name, FIELD_ID, TARGET_CONCEPT_ID, TARGET_VOCABULARY_ID
FROM mapping_classified
WHERE mapping_category = 'Custom'
  AND TARGET_VOCABULARY_ID NOT IN ('AIREADI','AIREADI-Vision','AIREADI-MOCA');

-- 6d. Survey timestamps mapped to the wrong start/complete concept
--     (start-timestamp fields end in "startts"; completion fields end in "cmpts")
SELECT 'timestamp_start_complete_swapped' AS check_name, FIELD_ID, SRC_CODE, TARGET_CONCEPT_ID
FROM mapping_classified
WHERE (regexp_matches(SRC_CODE, 'startts$') AND target_id = 2005200559)
   OR (regexp_matches(SRC_CODE, 'cmpts$')   AND target_id = 2005200558);
