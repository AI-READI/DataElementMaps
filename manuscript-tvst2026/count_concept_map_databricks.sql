-- =============================================================================
-- count_concept_map_databricks.sql
-- AI-READI REDCap -> OMOP CDM mapping: element and concept counts
-- Dialect: Databricks SQL / Spark SQL
--
-- Reproduces the counts reported in the manuscript (Table 2, Results, Abstract)
-- from the mapping table:
--     ai_readi_redcap_value_set_mapping_common
-- (If the table is catalog/schema-qualified, find/replace the table name with
--  <catalog>.<schema>.ai_readi_redcap_value_set_mapping_common.)
--
-- Counting rules
--   * Designated for mapping    : Map_to_OMOP = 'Yes'
--   * Mapped                    : designated AND TARGET_CONCEPT_ID populated
--   * Custom (AI-READI) concept : TARGET_CONCEPT_ID >= 2,000,000,000
--   * Standard concept          : TARGET_CONCEPT_ID <  2,000,000,000
--   * Excluded from mapped counts: REDCap survey start/complete timestamps
--     (custom concepts 2005200558 "Survey Started Timestamp" and
--      2005200559 "Survey Completed Timestamp"); these are REDCap system
--     metadata, not survey content, and are reported as designated-but-unmapped.
--   * Not designated = 2,906 curated REDCap data elements minus rows in the
--     mapping table.
--
-- All columns are cast to STRING before use, so the script works whether the
-- table was loaded with inferred types or as all-string columns.
-- 
-- modify the from statements to point to 
-- where the mapping table is created/uploaded
-- i.e.
-- from <yourdb>.ai_readi_redcap_value_set_mapping_common
-- =============================================================================


-- -----------------------------------------------------------------------------
-- 0. Classified view
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW mapping_classified AS
WITH src AS (
  SELECT
    TRIM(CAST(Map_to_OMOP          AS STRING)) AS map_to_omop,
    TRIM(CAST(FORM_NAME            AS STRING)) AS form_name,
    TRIM(CAST(FIELD_ID             AS STRING)) AS field_id,
    TRIM(CAST(SRC_CODE             AS STRING)) AS src_code,
    TRY_CAST(TRIM(CAST(TARGET_CONCEPT_ID AS STRING)) AS BIGINT) AS target_id,
    NULLIF(TRIM(CAST(LOCAL_CONCEPT_ID    AS STRING)), '')       AS local_concept_id,
    TRIM(CAST(TARGET_VOCABULARY_ID AS STRING)) AS target_vocabulary_id,
    TRIM(CAST(PREDICATE_ID         AS STRING)) AS predicate_id,
    TRY_CAST(TRIM(CAST(CONFIDENCE  AS STRING)) AS DOUBLE) AS confidence,
    NULLIF(TRIM(CAST(qualifier_concept_id   AS STRING)), '') AS qualifier_concept_id,
    TRIM(CAST(qualifier_source_value AS STRING)) AS qualifier_source_value
   
  FROM ai_readi_redcap_value_set_mapping_common
)
SELECT
  src.*,
  CASE
    WHEN map_to_omop <> 'Yes' OR map_to_omop IS NULL         THEN 'Designated but unmapped'
    WHEN target_id IS NULL                                   THEN 'Designated but unmapped'
    WHEN target_id IN (2005200558, 2005200559)               THEN 'Designated but unmapped'
    WHEN target_id >= 2000000000                             THEN 'Custom'
    ELSE                                                          'Standard'
  END AS mapping_category,
  CASE
    WHEN target_id IN (2005200558, 2005200559)               THEN 'REDCap survey timestamp'
    WHEN COALESCE(map_to_omop, '') <> 'Yes'
         AND src_code LIKE 'moca_paper%'                     THEN 'MoCA paper-administration flag'
    WHEN target_id IS NOT NULL
         AND map_to_omop = 'Yes'                             THEN NULL
    WHEN field_id RLIKE '^import_.*_(min|max)'               THEN 'Laboratory reference range'
    WHEN field_id RLIKE '^import_(collection_dt|process_dt|notes)' THEN 'Specimen handling'
    WHEN form_name = 'bcva'                                  THEN 'BCVA not-done / sign modifier'
    WHEN form_name = 'device_return'                         THEN 'REDCap administrative'
    ELSE                                                          'Other'
  END AS unmapped_reason
FROM src;


-- -----------------------------------------------------------------------------
-- 1. Coverage summary (Table 2)
-- -----------------------------------------------------------------------------
WITH params AS (SELECT 2906 AS total_curated),
by_cat AS (
  SELECT mapping_category,
         COUNT(*) AS n,
         COUNT(DISTINCT CASE WHEN mapping_category IN ('Standard', 'Custom')
                             THEN target_id END) AS distinct_concepts
  FROM mapping_classified
  GROUP BY mapping_category
),
all_rows AS (
  SELECT mapping_category AS category, n,
         CASE WHEN mapping_category IN ('Standard', 'Custom') THEN distinct_concepts END AS distinct_concepts
  FROM by_cat
  UNION ALL
  SELECT 'Mapped total',
         (SELECT SUM(n) FROM by_cat WHERE mapping_category IN ('Standard', 'Custom')),
         (SELECT COUNT(DISTINCT target_id) FROM mapping_classified
           WHERE mapping_category IN ('Standard', 'Custom'))
  UNION ALL
  SELECT 'Not designated',
         (SELECT total_curated FROM params) - (SELECT COUNT(*) FROM mapping_classified),
         CAST(NULL AS BIGINT)
  UNION ALL
  SELECT 'Total curated elements', (SELECT total_curated FROM params), CAST(NULL AS BIGINT)
)
SELECT category,
       n,
       ROUND(100.0 * n / (SELECT total_curated FROM params), 1) AS pct_of_2906,
       distinct_concepts
FROM all_rows
ORDER BY CASE category
           WHEN 'Standard'                THEN 1
           WHEN 'Custom'                  THEN 2
           WHEN 'Mapped total'            THEN 3
           WHEN 'Designated but unmapped' THEN 4
           WHEN 'Not designated'          THEN 5
           ELSE 6 END;
-- Expected: Standard 1,413 (48.6%) / 381; Custom 487 (16.8%) / 342;
--           Mapped total 1,900 (65.4%) / 723; Designated but unmapped 104 (3.6%);
--           Not designated 902 (31.0%); Total 2,906.


-- -----------------------------------------------------------------------------
-- 2. Elements and distinct concepts by vocabulary
-- -----------------------------------------------------------------------------
SELECT mapping_category,
       target_vocabulary_id          AS vocabulary,
       COUNT(*)                      AS elements,
       COUNT(DISTINCT target_id)     AS distinct_concepts
FROM mapping_classified
WHERE mapping_category IN ('Standard', 'Custom')
GROUP BY mapping_category, target_vocabulary_id
ORDER BY mapping_category DESC, elements DESC;
-- Expected: LOINC 1,200/281; SNOMED 138/71; UCUM 69/23; PPI 5/5; OMOP Extension 1/1;
--           AIREADI 388/265; AIREADI-Vision 69/47; AIREADI-MOCA 30/30.


-- -----------------------------------------------------------------------------
-- 3. Designated-but-unmapped breakdown
-- -----------------------------------------------------------------------------
SELECT unmapped_reason, COUNT(*) AS n
FROM mapping_classified
WHERE mapping_category = 'Designated but unmapped'
GROUP BY unmapped_reason
ORDER BY n DESC;
-- Expected: reference range 46; survey timestamp 34; specimen handling 12;
--           BCVA 10; REDCap administrative 1; MoCA paper flag 1 (total 104).


-- -----------------------------------------------------------------------------
-- 4. SKOS predicate and confidence distribution
-- -----------------------------------------------------------------------------
-- 4a. Predicate totals
SELECT mapping_category, predicate_id, COUNT(*) AS n
FROM mapping_classified
WHERE mapping_category IN ('Standard', 'Custom')
GROUP BY mapping_category, predicate_id
ORDER BY mapping_category DESC, n DESC;
-- Expected (standard): exactMatch 1,173; closeMatch 237; relatedMatch 3.
-- Expected (custom):   exactMatch 487.

-- 4b. Confidence totals
SELECT mapping_category, confidence, COUNT(*) AS n
FROM mapping_classified
WHERE mapping_category IN ('Standard', 'Custom')
GROUP BY mapping_category, confidence
ORDER BY mapping_category DESC, confidence DESC;
-- Expected (standard): 1.0 = 1,327; 0.75 = 84; 0.5 = 2.
-- Expected (custom):   1.0 = 487.


-- -----------------------------------------------------------------------------
-- 5. Laterality qualifiers
-- -----------------------------------------------------------------------------
SELECT qualifier_concept_id, qualifier_source_value, COUNT(*) AS n
FROM mapping_classified
WHERE mapping_category IN ('Standard', 'Custom')
  AND qualifier_concept_id IN ('45876703', '45883829', '4298982', '4320144')
GROUP BY qualifier_concept_id, qualifier_source_value
ORDER BY qualifier_concept_id;
-- Expected: Right eye 78; Left eye 78; Structure of right foot 2; Structure of left foot 2.


-- -----------------------------------------------------------------------------
-- 6. Integrity checks (each should return 0 rows)
-- -----------------------------------------------------------------------------
-- 6a. Custom concepts missing LOCAL_CONCEPT_ID
SELECT 'custom_missing_local_id' AS check_name, field_id, src_code, target_id
FROM mapping_classified
WHERE mapping_category = 'Custom' AND local_concept_id IS NULL;

-- 6b. Mapped rows missing predicate or confidence
SELECT 'mapped_missing_predicate_or_confidence' AS check_name, field_id, src_code
FROM mapping_classified
WHERE mapping_category IN ('Standard', 'Custom')
  AND (NULLIF(predicate_id, '') IS NULL OR confidence IS NULL);

-- 6c. Custom concept IDs whose vocabulary is not an AI-READI vocabulary
SELECT 'custom_wrong_vocabulary' AS check_name, field_id, target_id, target_vocabulary_id
FROM mapping_classified
WHERE mapping_category = 'Custom'
  AND target_vocabulary_id NOT IN ('AIREADI', 'AIREADI-Vision', 'AIREADI-MOCA');

-- 6d. Survey timestamps mapped to the wrong start/complete concept
--     (start-timestamp fields end in "startts"; completion fields end in "cmpts")
SELECT 'timestamp_start_complete_swapped' AS check_name, field_id, src_code, target_id
FROM mapping_classified
WHERE (src_code RLIKE 'startts$' AND target_id = 2005200559)
   OR (src_code RLIKE 'cmpts$'   AND target_id = 2005200558);
