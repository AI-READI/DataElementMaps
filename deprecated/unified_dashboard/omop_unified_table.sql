-- Create comprehensive unified OMOP data quality table
-- This replaces the need for complex UNION queries in dashboards
-- Includes all major domain-specific fields for analysis

DROP TABLE IF EXISTS ehr_dqp.omop_unified_summary;

CREATE TABLE ehr_dqp.omop_unified_summary AS

-- Column Reference (all columns with contributing source tables):
-- domain                    -- ALL: person, condition_occurrence, observation, procedure_occurrence, measurement, visit_occurrence, drug_exposure, device_exposure, death
-- domain_record_id          -- ALL except person/death: condition_occurrence_id, observation_id, procedure_occurrence_id, measurement_id, visit_occurrence_id, drug_exposure_id, device_exposure_id
-- person_id                 -- ALL: person, condition_occurrence, observation, procedure_occurrence, measurement, visit_occurrence, drug_exposure, device_exposure, death
-- concept_id                -- ALL except person: condition_concept_id, observation_concept_id, procedure_concept_id, measurement_concept_id, visit_concept_id, drug_concept_id, device_concept_id, cause_concept_id
-- concept_name              -- ALL except person: condition_concept_name, observation_concept_name, procedure_concept_name, measurement_concept_name, visit_concept_name, drug_concept_name, device_concept_name, cause_concept_name
-- domain_date               -- ALL except person: condition_start_date, observation_date, procedure_date, measurement_date, visit_start_date, drug_exposure_start_date, device_exposure_start_date, death_date
-- domain_end_date           -- condition_occurrence, visit_occurrence, drug_exposure, device_exposure: condition_end_date, visit_end_date, drug_exposure_end_date, device_exposure_end_date
-- visit_occurrence_id       -- ALL except person/death: condition_occurrence, observation, procedure_occurrence, measurement, visit_occurrence, drug_exposure, device_exposure
-- provider_id               -- ALL except person/death: condition_occurrence, observation, procedure_occurrence, measurement, visit_occurrence, drug_exposure, device_exposure
-- data_partner_id           -- ALL: person, condition_occurrence, observation, procedure_occurrence, measurement, visit_occurrence, drug_exposure, device_exposure, death
-- site_name                 -- ALL: derived from data_partner_id mapping
-- gender_concept_id         -- person: gender_concept_id
-- gender_concept_name       -- person: gender_concept_name
-- year_of_birth             -- person: year_of_birth
-- month_of_birth            -- person: month_of_birth
-- day_of_birth              -- person: day_of_birth
-- race_concept_id           -- person: race_concept_id
-- race_concept_name         -- person: race_concept_name
-- ethnicity_concept_id      -- person: ethnicity_concept_id
-- ethnicity_concept_name    -- person: ethnicity_concept_name
-- type_concept_id           -- ALL except person: condition_type_concept_id, observation_type_concept_id, procedure_type_concept_id, measurement_type_concept_id, visit_type_concept_id, drug_type_concept_id, device_type_concept_id, death_type_concept_id
-- type_concept_name         -- ALL except person: condition_type_concept_name, observation_type_concept_name, procedure_type_concept_name, measurement_type_concept_name, visit_type_concept_name, drug_type_concept_name, device_type_concept_name, death_type_concept_name
-- value_as_number           -- observation, measurement: value_as_number
-- value_as_concept_id       -- observation, measurement: value_as_concept_id
-- value_as_concept_name     -- observation, measurement: value_as_concept_name
-- unit_concept_id           -- observation, measurement: unit_concept_id
-- unit_concept_name         -- measurement: unit_concept_name
-- range_low                 -- measurement: range_low
-- range_high                -- measurement: range_high
-- quantity                  -- procedure_occurrence, drug_exposure, device_exposure: quantity
-- days_supply               -- drug_exposure: days_supply
-- refills                   -- drug_exposure: refills
-- route_concept_id          -- drug_exposure: route_concept_id
-- route_concept_name        -- drug_exposure: route_concept_name

WITH site_mapping AS (
  SELECT 8469 AS data_partner_id, 'UAB' AS site_name
  UNION ALL SELECT 2084, 'UCSD'
  UNION ALL SELECT 3058, 'UW'
),

-- Person domain (demographic data)
-- NOTE: Fixed issue - person domain doesn't have a "person_concept_id", so gender fields are kept as-is
person_data AS (
  SELECT 
    'person' as domain,
    CAST(NULL AS BIGINT) as domain_record_id,
    p.person_id,
    CAST(NULL AS BIGINT) as concept_id,
    CAST(NULL AS STRING) as concept_name,
    CAST(NULL AS DATE) as domain_date,
    CAST(NULL AS DATE) as domain_end_date,
    CAST(NULL AS BIGINT) as visit_occurrence_id,
    CAST(NULL AS BIGINT) as provider_id,
    p.data_partner_id,
    s.site_name,
    -- Person-specific demographic fields
    p.gender_concept_id,
    p.gender_concept_name,
    p.year_of_birth,
    p.month_of_birth,
    p.day_of_birth,
    p.race_concept_id,
    p.race_concept_name,
    p.ethnicity_concept_id,
    p.ethnicity_concept_name,
    -- Type concepts
    CAST(NULL AS BIGINT) as type_concept_id,
    CAST(NULL AS STRING) as type_concept_name,
    -- Measurement/observation values
    CAST(NULL AS DOUBLE) as value_as_number,
    CAST(NULL AS BIGINT) as value_as_concept_id,
    CAST(NULL AS STRING) as value_as_concept_name,
    CAST(NULL AS BIGINT) as unit_concept_id,
    CAST(NULL AS STRING) as unit_concept_name,
    CAST(NULL AS DOUBLE) as range_low,
    CAST(NULL AS DOUBLE) as range_high,
    -- Drug-specific fields
    CAST(NULL AS DOUBLE) as quantity,
    CAST(NULL AS INTEGER) as days_supply,
    CAST(NULL AS INTEGER) as refills,
    CAST(NULL AS BIGINT) as route_concept_id,
    CAST(NULL AS STRING) as route_concept_name
  FROM ehr_union.person p
  JOIN site_mapping s ON p.data_partner_id = s.data_partner_id
),

-- Condition occurrences
condition_data AS (
  SELECT 
    'condition_occurrence' as domain,
    co.condition_occurrence_id as domain_record_id,
    co.person_id,
    co.condition_concept_id as concept_id,
    co.condition_concept_name as concept_name,
    co.condition_start_date as domain_date,
    co.condition_end_date as domain_end_date,
    co.visit_occurrence_id,
    co.provider_id,
    co.data_partner_id,
    s.site_name,
    -- Person demographics (not applicable)
    CAST(NULL AS BIGINT) as gender_concept_id,
    CAST(NULL AS STRING) as gender_concept_name,
    CAST(NULL AS INTEGER) as year_of_birth,
    CAST(NULL AS INTEGER) as month_of_birth,
    CAST(NULL AS INTEGER) as day_of_birth,
    CAST(NULL AS BIGINT) as race_concept_id,
    CAST(NULL AS STRING) as race_concept_name,
    CAST(NULL AS BIGINT) as ethnicity_concept_id,
    CAST(NULL AS STRING) as ethnicity_concept_name,
    -- Type concepts
    co.condition_type_concept_id as type_concept_id,
    co.condition_type_concept_name as type_concept_name,
    -- Measurement/observation values (not applicable)
    CAST(NULL AS DOUBLE) as value_as_number,
    CAST(NULL AS BIGINT) as value_as_concept_id,
    CAST(NULL AS STRING) as value_as_concept_name,
    CAST(NULL AS BIGINT) as unit_concept_id,
    CAST(NULL AS STRING) as unit_concept_name,
    CAST(NULL AS DOUBLE) as range_low,
    CAST(NULL AS DOUBLE) as range_high,
    -- Drug-specific fields (not applicable)
    CAST(NULL AS DOUBLE) as quantity,
    CAST(NULL AS INTEGER) as days_supply,
    CAST(NULL AS INTEGER) as refills,
    CAST(NULL AS BIGINT) as route_concept_id,
    CAST(NULL AS STRING) as route_concept_name
  FROM ehr_union.condition_occurrence co
  JOIN site_mapping s ON co.data_partner_id = s.data_partner_id
),

-- Observations
observation_data AS (
  SELECT 
    'observation' as domain,
    o.observation_id as domain_record_id,
    o.person_id,
    o.observation_concept_id as concept_id,
    o.observation_concept_name as concept_name,
    o.observation_date as domain_date,
    CAST(NULL AS DATE) as domain_end_date,
    o.visit_occurrence_id,
    o.provider_id,
    o.data_partner_id,
    s.site_name,
    -- Person demographics (not applicable)
    CAST(NULL AS BIGINT) as gender_concept_id,
    CAST(NULL AS STRING) as gender_concept_name,
    CAST(NULL AS INTEGER) as year_of_birth,
    CAST(NULL AS INTEGER) as month_of_birth,
    CAST(NULL AS INTEGER) as day_of_birth,
    CAST(NULL AS BIGINT) as race_concept_id,
    CAST(NULL AS STRING) as race_concept_name,
    CAST(NULL AS BIGINT) as ethnicity_concept_id,
    CAST(NULL AS STRING) as ethnicity_concept_name,
    -- Type concepts
    o.observation_type_concept_id as type_concept_id,
    o.observation_type_concept_name as type_concept_name,
    -- Measurement/observation values
    o.value_as_number,
    o.value_as_concept_id,
    o.value_as_concept_name,
    o.unit_concept_id,
    o.unit_concept_name,
    CAST(NULL AS DOUBLE) as range_low,
    CAST(NULL AS DOUBLE) as range_high,
    -- Drug-specific fields (not applicable)
    CAST(NULL AS DOUBLE) as quantity,
    CAST(NULL AS INTEGER) as days_supply,
    CAST(NULL AS INTEGER) as refills,
    CAST(NULL AS BIGINT) as route_concept_id,
    CAST(NULL AS STRING) as route_concept_name
  FROM ehr_union.observation o
  JOIN site_mapping s ON o.data_partner_id = s.data_partner_id
),

-- Procedures
procedure_data AS (
  SELECT 
    'procedure_occurrence' as domain,
    po.procedure_occurrence_id as domain_record_id,
    po.person_id,
    po.procedure_concept_id as concept_id,
    po.procedure_concept_name as concept_name,
    po.procedure_date as domain_date,
    CAST(NULL AS DATE) as domain_end_date,
    po.visit_occurrence_id,
    po.provider_id,
    po.data_partner_id,
    s.site_name,
    -- Person demographics (not applicable)
    CAST(NULL AS BIGINT) as gender_concept_id,
    CAST(NULL AS STRING) as gender_concept_name,
    CAST(NULL AS INTEGER) as year_of_birth,
    CAST(NULL AS INTEGER) as month_of_birth,
    CAST(NULL AS INTEGER) as day_of_birth,
    CAST(NULL AS BIGINT) as race_concept_id,
    CAST(NULL AS STRING) as race_concept_name,
    CAST(NULL AS BIGINT) as ethnicity_concept_id,
    CAST(NULL AS STRING) as ethnicity_concept_name,
    -- Type concepts
    po.procedure_type_concept_id as type_concept_id,
    po.procedure_type_concept_name as type_concept_name,
    -- Measurement/observation values (not applicable)
    CAST(NULL AS DOUBLE) as value_as_number,
    CAST(NULL AS BIGINT) as value_as_concept_id,
    CAST(NULL AS STRING) as value_as_concept_name,
    CAST(NULL AS BIGINT) as unit_concept_id,
    CAST(NULL AS STRING) as unit_concept_name,
    CAST(NULL AS DOUBLE) as range_low,
    CAST(NULL AS DOUBLE) as range_high,
    -- Drug-specific fields
    CAST(po.quantity AS DOUBLE) as quantity,
    CAST(NULL AS INTEGER) as days_supply,
    CAST(NULL AS INTEGER) as refills,
    CAST(NULL AS BIGINT) as route_concept_id,
    CAST(NULL AS STRING) as route_concept_name
  FROM ehr_union.procedure_occurrence po
  JOIN site_mapping s ON po.data_partner_id = s.data_partner_id
),

-- Measurements
measurement_data AS (
  SELECT 
    'measurement' as domain,
    m.measurement_id as domain_record_id,
    m.person_id,
    m.measurement_concept_id as concept_id,
    m.measurement_concept_name as concept_name,
    m.measurement_date as domain_date,
    CAST(NULL AS DATE) as domain_end_date,
    m.visit_occurrence_id,
    m.provider_id,
    m.data_partner_id,
    s.site_name,
    -- Person demographics (not applicable)
    CAST(NULL AS BIGINT) as gender_concept_id,
    CAST(NULL AS STRING) as gender_concept_name,
    CAST(NULL AS INTEGER) as year_of_birth,
    CAST(NULL AS INTEGER) as month_of_birth,
    CAST(NULL AS INTEGER) as day_of_birth,
    CAST(NULL AS BIGINT) as race_concept_id,
    CAST(NULL AS STRING) as race_concept_name,
    CAST(NULL AS BIGINT) as ethnicity_concept_id,
    CAST(NULL AS STRING) as ethnicity_concept_name,
    -- Type concepts
    m.measurement_type_concept_id as type_concept_id,
    m.measurement_type_concept_name as type_concept_name,
    -- Measurement/observation values
    m.value_as_number,
    m.value_as_concept_id,
    m.value_as_concept_name,
    m.unit_concept_id,
    m.unit_concept_name,
    m.range_low,
    m.range_high,
    -- Drug-specific fields (not applicable)
    CAST(NULL AS DOUBLE) as quantity,
    CAST(NULL AS INTEGER) as days_supply,
    CAST(NULL AS INTEGER) as refills,
    CAST(NULL AS BIGINT) as route_concept_id,
    CAST(NULL AS STRING) as route_concept_name
  FROM ehr_union.measurement m
  JOIN site_mapping s ON m.data_partner_id = s.data_partner_id
),

-- Visits
visit_data AS (
  SELECT 
    'visit_occurrence' as domain,
    vo.visit_occurrence_id as domain_record_id,
    vo.person_id,
    vo.visit_concept_id as concept_id,
    vo.visit_concept_name as concept_name,
    vo.visit_start_date as domain_date,
    vo.visit_end_date as domain_end_date,
    vo.visit_occurrence_id,
    vo.provider_id,
    vo.data_partner_id,
    s.site_name,
    -- Person demographics (not applicable)
    CAST(NULL AS BIGINT) as gender_concept_id,
    CAST(NULL AS STRING) as gender_concept_name,
    CAST(NULL AS INTEGER) as year_of_birth,
    CAST(NULL AS INTEGER) as month_of_birth,
    CAST(NULL AS INTEGER) as day_of_birth,
    CAST(NULL AS BIGINT) as race_concept_id,
    CAST(NULL AS STRING) as race_concept_name,
    CAST(NULL AS BIGINT) as ethnicity_concept_id,
    CAST(NULL AS STRING) as ethnicity_concept_name,
    -- Type concepts
    vo.visit_type_concept_id as type_concept_id,
    vo.visit_type_concept_name as type_concept_name,
    -- Measurement/observation values (not applicable)
    CAST(NULL AS DOUBLE) as value_as_number,
    CAST(NULL AS BIGINT) as value_as_concept_id,
    CAST(NULL AS STRING) as value_as_concept_name,
    CAST(NULL AS BIGINT) as unit_concept_id,
    CAST(NULL AS STRING) as unit_concept_name,
    CAST(NULL AS DOUBLE) as range_low,
    CAST(NULL AS DOUBLE) as range_high,
    -- Drug-specific fields (not applicable)
    CAST(NULL AS DOUBLE) as quantity,
    CAST(NULL AS INTEGER) as days_supply,
    CAST(NULL AS INTEGER) as refills,
    CAST(NULL AS BIGINT) as route_concept_id,
    CAST(NULL AS STRING) as route_concept_name
  FROM ehr_union.visit_occurrence vo
  JOIN site_mapping s ON vo.data_partner_id = s.data_partner_id
),

-- Drug exposures
drug_data AS (
  SELECT 
    'drug_exposure' as domain,
    de.drug_exposure_id as domain_record_id,
    de.person_id,
    de.drug_concept_id as concept_id,
    de.drug_concept_name as concept_name,
    de.drug_exposure_start_date as domain_date,
    de.drug_exposure_end_date as domain_end_date,
    de.visit_occurrence_id,
    de.provider_id,
    de.data_partner_id,
    s.site_name,
    -- Person demographics (not applicable)
    CAST(NULL AS BIGINT) as gender_concept_id,
    CAST(NULL AS STRING) as gender_concept_name,
    CAST(NULL AS INTEGER) as year_of_birth,
    CAST(NULL AS INTEGER) as month_of_birth,
    CAST(NULL AS INTEGER) as day_of_birth,
    CAST(NULL AS BIGINT) as race_concept_id,
    CAST(NULL AS STRING) as race_concept_name,
    CAST(NULL AS BIGINT) as ethnicity_concept_id,
    CAST(NULL AS STRING) as ethnicity_concept_name,
    -- Type concepts
    de.drug_type_concept_id as type_concept_id,
    de.drug_type_concept_name as type_concept_name,
    -- Measurement/observation values (not applicable)
    CAST(NULL AS DOUBLE) as value_as_number,
    CAST(NULL AS BIGINT) as value_as_concept_id,
    CAST(NULL AS STRING) as value_as_concept_name,
    CAST(NULL AS BIGINT) as unit_concept_id,
    CAST(NULL AS STRING) as unit_concept_name,
    CAST(NULL AS DOUBLE) as range_low,
    CAST(NULL AS DOUBLE) as range_high,
    -- Drug-specific fields
    de.quantity,
    de.days_supply,
    de.refills,
    de.route_concept_id,
    de.route_concept_name
  FROM ehr_union.drug_exposure de
  JOIN site_mapping s ON de.data_partner_id = s.data_partner_id
),

-- Device exposures
device_data AS (
  SELECT 
    'device_exposure' as domain,
    dev.device_exposure_id as domain_record_id,
    dev.person_id,
    dev.device_concept_id as concept_id,
    dev.device_concept_name as concept_name,
    dev.device_exposure_start_date as domain_date,
    dev.device_exposure_end_date as domain_end_date,
    dev.visit_occurrence_id,
    dev.provider_id,
    dev.data_partner_id,
    s.site_name,
    -- Person demographics (not applicable)
    CAST(NULL AS BIGINT) as gender_concept_id,
    CAST(NULL AS STRING) as gender_concept_name,
    CAST(NULL AS INTEGER) as year_of_birth,
    CAST(NULL AS INTEGER) as month_of_birth,
    CAST(NULL AS INTEGER) as day_of_birth,
    CAST(NULL AS BIGINT) as race_concept_id,
    CAST(NULL AS STRING) as race_concept_name,
    CAST(NULL AS BIGINT) as ethnicity_concept_id,
    CAST(NULL AS STRING) as ethnicity_concept_name,
    -- Type concepts
    dev.device_type_concept_id as type_concept_id,
    dev.device_type_concept_name as type_concept_name,
    -- Measurement/observation values (not applicable)
    CAST(NULL AS DOUBLE) as value_as_number,
    CAST(NULL AS BIGINT) as value_as_concept_id,
    CAST(NULL AS STRING) as value_as_concept_name,
    CAST(NULL AS BIGINT) as unit_concept_id,
    CAST(NULL AS STRING) as unit_concept_name,
    CAST(NULL AS DOUBLE) as range_low,
    CAST(NULL AS DOUBLE) as range_high,
    -- Drug-specific fields (quantity applicable)
    CAST(dev.quantity AS DOUBLE) as quantity,
    CAST(NULL AS INTEGER) as days_supply,
    CAST(NULL AS INTEGER) as refills,
    CAST(NULL AS BIGINT) as route_concept_id,
    CAST(NULL AS STRING) as route_concept_name
  FROM ehr_union.device_exposure dev
  JOIN site_mapping s ON dev.data_partner_id = s.data_partner_id
),

-- Death records
death_data AS (
  SELECT 
    'death' as domain,
    CAST(NULL AS BIGINT) as domain_record_id,
    d.person_id,
    d.cause_concept_id as concept_id,
    d.cause_concept_name as concept_name,
    d.death_date as domain_date,
    CAST(NULL AS DATE) as domain_end_date,
    CAST(NULL AS BIGINT) as visit_occurrence_id,
    CAST(NULL AS BIGINT) as provider_id,
    d.data_partner_id,
    s.site_name,
    -- Person demographics (not applicable)
    CAST(NULL AS BIGINT) as gender_concept_id,
    CAST(NULL AS STRING) as gender_concept_name,
    CAST(NULL AS INTEGER) as year_of_birth,
    CAST(NULL AS INTEGER) as month_of_birth,
    CAST(NULL AS INTEGER) as day_of_birth,
    CAST(NULL AS BIGINT) as race_concept_id,
    CAST(NULL AS STRING) as race_concept_name,
    CAST(NULL AS BIGINT) as ethnicity_concept_id,
    CAST(NULL AS STRING) as ethnicity_concept_name,
    -- Type concepts
    d.death_type_concept_id as type_concept_id,
    d.death_type_concept_name as type_concept_name,
    -- Measurement/observation values (not applicable)
    CAST(NULL AS DOUBLE) as value_as_number,
    CAST(NULL AS BIGINT) as value_as_concept_id,
    CAST(NULL AS STRING) as value_as_concept_name,
    CAST(NULL AS BIGINT) as unit_concept_id,
    CAST(NULL AS STRING) as unit_concept_name,
    CAST(NULL AS DOUBLE) as range_low,
    CAST(NULL AS DOUBLE) as range_high,
    -- Drug-specific fields (not applicable)
    CAST(NULL AS DOUBLE) as quantity,
    CAST(NULL AS INTEGER) as days_supply,
    CAST(NULL AS INTEGER) as refills,
    CAST(NULL AS BIGINT) as route_concept_id,
    CAST(NULL AS STRING) as route_concept_name
  FROM ehr_union.death d
  JOIN site_mapping s ON d.data_partner_id = s.data_partner_id
)

-- Union all domains
SELECT * FROM person_data
UNION ALL SELECT * FROM condition_data
UNION ALL SELECT * FROM observation_data
UNION ALL SELECT * FROM procedure_data
UNION ALL SELECT * FROM measurement_data
UNION ALL SELECT * FROM visit_data
UNION ALL SELECT * FROM drug_data
UNION ALL SELECT * FROM device_data
UNION ALL SELECT * FROM death_data;

