----------------------------------------------
--concept map validation counts
-- VALIDATES TABLE 3 - count of distinct standard concepts --
SELECT TARGET_VOCABULARY_ID, count(DISTINCT TARGET_CONCEPT_ID) as cnt
FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common
WHERE TARGET_STANDARD_CONCEPT = 'S' and local_concept_id is null
AND TARGET_CONCEPT_ID < 2000000000
GROUP BY 1
ORDER BY 2 DESC

-- VALIDATES TABLE 3 - instances of records
SELECT TARGET_VOCABULARY_ID, count( TARGET_CONCEPT_ID) as cnt
FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common
WHERE TARGET_STANDARD_CONCEPT = 'S' and local_concept_id is null
AND TARGET_CONCEPT_ID < 2000000000
GROUP BY 1
ORDER BY 2 DESC

----------------------------------------------
-- %sql --Custom concept creation (AI-READI Extensions) | 343 | count of new custom concepts created to map the ai-readi survey data |
-- -- custom concept counts by vocabulary id
with custom_concept_count as (
select  q.TARGET_VOCABULARY_ID as vocabulary_id, count(distinct q.target_concept_id) as n_custom_concepts
from redcapsurveydb.ai_readi_redcap_value_set_mapping_common q
where q.TARGET_CONCEPT_ID > 2000000000 --2005200011 custom concepts are in the 2billion range
group by 1
)

%sql
select  q.TARGET_VOCABULARY_ID as vocabulary_id, count(distinct q.target_concept_id) as n_custom_concepts
from redcapsurveydb.ai_readi_redcap_value_set_mapping_common q
where q.TARGET_CONCEPT_ID > 2000000000 --2005200011 custom concepts are in the 2billion range
group by 1


-- add total at the end
SELECT custom_concept_count.vocabulary_id, custom_concept_count.n_custom_concepts, 0 AS sort_key FROM custom_concept_count
UNION ALL
SELECT 'TOTAL', SUM(n_custom_concepts), 1 FROM custom_concept_count
ORDER BY sort_key, n_custom_concepts DESC
-- custom concept counts by vocabulary id
----------------------------------------------
-- question concept with multiple responses
--%sql -- after excluding the rows that have only one answer to the question
    SELECT    "Question–response pair mapping" AS strategy
            , q.SRC_CODE AS q_code
            , r.SRC_CODE AS r_code
            , q.SRC_CD_DESCRIPTION AS question
            , r.SRC_CD_DESCRIPTION AS answer
    FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common q
    JOIN redcapsurveydb.ai_readi_redcap_value_set_mapping_common r ON q.SRC_CODE = r.FIELD_ID
    QUALIFY COUNT(*) OVER (PARTITION BY q.SRC_CODE) = 1 -- 56 rows to exclude (single-answer questions)-
--%sql

----------------------------------------------
--%sql -- various mapping strategy
WITH
  std_concepts AS (
    select "Direct standard concept mapping" AS strategy,
           TARGET_concept_id, target_concept_name,  count(*) from redcapsurveydb.ai_readi_redcap_value_set_mapping_common 
    where target_concept_id < 2000000000 --2005200011 custom concepts are in the 2billion range
    and LOCAL_CONCEPT_ID is null 
    and TARGET_STANDARD_CONCEPT = 'S'
    group by 1, 2, 3
  ) 
  , q_r_pairs AS (
    SELECT    "Question–response pair mapping" AS strategy
            , q.SRC_CODE AS q_code
            , r.SRC_CODE AS r_code
            , q.SRC_CD_DESCRIPTION AS question
            , r.SRC_CD_DESCRIPTION AS answer
    FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common q
    JOIN redcapsurveydb.ai_readi_redcap_value_set_mapping_common r ON q.SRC_CODE = r.FIELD_ID
    --QUALIFY COUNT(*) OVER (PARTITION BY q.SRC_CODE) = 1 -- 56 rows to exclude (single-answer questions)
    QUALIFY COUNT(*) OVER (PARTITION BY q.SRC_CODE) > 1 -- excluding single-answer questions
)
/*, custom_concepts AS (
    with custom_concept_count as (
    select  q.TARGET_VOCABULARY_ID as vocabulary_id, count(distinct q.target_concept_id) as n_custom_concepts
    from redcapsurveydb.ai_readi_redcap_value_set_mapping_common q
    where q.TARGET_CONCEPT_ID > 2000000000 --2005200011 custom concepts are in the 2billion range
    group by 1
    )
   SELECT 'Custom concept creation (AI-READI Extensions)' AS strategy, SUM(n_custom_concepts), 1 FROM custom_concept_count
)*/

SELECT    strategy AS `Mapping Strategy`
        , COUNT(DISTINCT *) AS `Number of Data Elements`
        , 'Distinct count of standard concepts used to map the ai-readi survey data elements' AS Comments
FROM std_concepts GROUP BY strategy
UNION ALL
SELECT    strategy
        , COUNT(DISTINCT *)
        , 'List of question concepts that have permissble answer response' AS Comments
FROM q_r_pairs GROUP BY strategy
/*UNION ALL
SELECT    strategy
        , COUNT(DISTINCT *)
        , 'Count of new custom concepts created to map the ai-readi data' AS Comments
FROM custom_concepts GROUP BY strategy
*/


--SELECT DISTINCT * FROM q_r_pairs ORDER BY 2,3
--SELECT strategy, COUNT(DISTINCT r.s) cnt from q_r_pairs GROUP BY 1

----------------------------------------------
--well vetted survey instruments used in ai-readi redCapForms
%sql
-- select the list of form_names that are part of the questions from the well vetted survey instruments
-- count the standard and non-standard data elements 
-- we count all of the permissible question-answer pair as well as the question with a value as concept - count both single and multiple answers 
select distinct form_name --, SRC_CODE, count(distinct *) --37 survey instruments 
FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common_v_4 q --
where form_name in ('substance_use_survey','demographics_survey', 'lab_results', 'ditary_survey','px_food_insecurity_survey','px_neighborhood_environment_survey','px_sdoh_combined_survey','px_racial_ethnic_discrimination_survey','cesd10_survey','paid5_dm_survey','diabetes_survey')
--Validated survey instrument subscale mapping	122	count of instruments used for capturing the ai-readi data elements -122


----------------------------------------------
---38 survey forms
%sql
%sql
select distinct form_name, count(*) --38
FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common_v_4 q GROUP BY form_name


----------------------------------------------
--Validated survey instrument subscale mapping%sql
WITH q_r_pairs AS (
    SELECT    "Question–response pair mapping" AS strategy
            , q.SRC_CODE AS q_code
            , r.SRC_CODE AS r_code
            , q.SRC_CD_DESCRIPTION AS question
            , r.SRC_CD_DESCRIPTION AS answer
    FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common_v_4 q
    JOIN redcapsurveydb.ai_readi_redcap_value_set_mapping_common_v_4 r ON q.SRC_CODE = r.FIELD_ID
    --QUALIFY COUNT(*) OVER (PARTITION BY q.SRC_CODE) = 1 -- 56 rows to exclude (single-answer questions)
    QUALIFY COUNT(*) OVER (PARTITION BY q.SRC_CODE) > 1 -- excluding single-answer questions
)
select distinct form_name --, SRC_CODE, count(distinct *) --37 survey instruments 
FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common_v_4 q
--GROUP BY form_name, SRC_CODE
--Validated survey instrument subscale mapping	122	count of instruments used for capturing the ai-readi data elements -122

----------------------------------------------
--distinct concepts by vocab id
%sql
SELECT TARGET_VOCABULARY_ID, count(DISTINCT TARGET_CONCEPT_ID) as cnt
FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common_v_4
WHERE TARGET_STANDARD_CONCEPT = 'S'
GROUP BY 1

-- TARGET_VOCABULARY_ID	cnt
-- UCUM	23
-- PPI	5
-- AIREADI-MOCA	30
-- AIREADI	266
-- SNOMED	71
-- LOINC	281
-- AIREADI-Vision	47
-- OMOP Extension	1
----------------------------------------------