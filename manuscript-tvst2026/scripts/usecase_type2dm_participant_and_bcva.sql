%sql
-- example use case the harmonized data allow a single OMOP query 
-- to identify participants who reported a professional diagnosis of type 2 diabetes and 
-- retrieve their best-corrected visual acuity separately for each eye, a cohort definition that would otherwise require reconciling REDCap form-specific variables.

-- Participants with patient-reported type 2 diabetes (dual-domain Condition record)
WITH t2d AS (
  SELECT DISTINCT person_id FROM omop_survey.condition_occurrence
  WHERE condition_concept_id = 201826 AND condition_type_concept_id = 45905770
),
bcva AS (                      -- BCVA measurement concepts, by eye, from the mapping file
  SELECT CAST(TARGET_CONCEPT_ID AS BIGINT) AS cid,
         CASE qualifier_concept_id WHEN '45876703' THEN 'right' WHEN '45883829' THEN 'left' END AS eye
  FROM redcapsurveydb.ai_readi_redcap_value_set_mapping_common
  WHERE FORM_NAME = 'bcva' AND qualifier_concept_id IN ('45876703','45883829')
)
SELECT COUNT(DISTINCT t.person_id) AS t2d_participants,
       COUNT(DISTINCT CASE WHEN b.eye = 'right' THEN m.person_id END) AS with_right_bcva,
       COUNT(DISTINCT CASE WHEN b.eye = 'left'  THEN m.person_id END) AS with_left_bcva
FROM t2d t
LEFT JOIN omop_survey.measurement m ON m.person_id = t.person_id
LEFT JOIN bcva b ON m.measurement_concept_id = b.cid;