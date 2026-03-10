# Value-Set Mapping Table Field Definitions

The **value-set mapping table** documents the transformation of survey data elements into standardized **OMOP concepts**. Each row represents a mapping between a survey question or response option and the corresponding OMOP vocabulary concept, along with metadata describing the mapping process.

This table serves as a structured artifact supporting semantic harmonization of survey instruments into the **OMOP Common Data Model (CDM)**.

---

## AI-READI Value-set Mapping Table Field Categories and Definitions

| Field Category | Field | Description |
|---|---|---|
| **Source Survey Metadata** | FORM_NAME | Name of the survey instrument or questionnaire. |
| **Source Survey Metadata** | FIELD_ID | Unique identifier for the survey item within the instrument. |
| **Source Survey Metadata** | FIELD_ID_NUM | Numeric index used to preserve the original question ordering. |
| **Source Survey Metadata** | FIELD_TYPE | Data type of the survey item (e.g., categorical, numeric). |
| **Source Survey Metadata** | SRC_CODE | Source code representing the original survey question or response. |
| **Source Survey Metadata** | SRC_CODE_ID | Internal identifier for the source concept. |
| **Source Survey Metadata** | SRC_CD_DESCRIPTION | Text description of the survey question or response option. |
| **OMOP Target Concept Mapping** | TARGET_CONCEPT_ID | OMOP standard concept identifier assigned during mapping, including UCUM concept IDs. |
| **OMOP Target Concept Mapping** | TARGET_CONCEPT_NAME | Standardized concept name from the OMOP vocabulary. |
| **OMOP Target Concept Mapping** | TARGET_DOMAIN_ID | OMOP domain to which the concept belongs (e.g., Observation, Condition, Measurement). |
| **OMOP Target Concept Mapping** | TARGET_VOCABULARY_ID | Source vocabulary of the OMOP concept (e.g., SNOMED CT, LOINC, RxNorm). |
| **OMOP Target Concept Mapping** | TARGET_CONCEPT_CLASS_ID | OMOP concept class describing the concept type. |
| **OMOP Target Concept Mapping** | TARGET_CONCEPT_CODE | Source vocabulary code corresponding to the concept. |
| **OMOP Target Concept Mapping** | TARGET_STANDARD_CONCEPT | Indicator showing whether the concept is a standard OMOP concept. |
| **Mapping Governance Metadata** | Extension_Needed | Flags cases where a new extension concept was required. |
| **Mapping Governance Metadata** | PREDICATE_ID | Mapping relationship used to represent semantic correspondence. |
| **Mapping Governance Metadata** | CONFIDENCE | Reviewer-assigned confidence score for the mapping decision. |
| **Mapping Governance Metadata** | MODIFIER | Additional contextual modifier used during mapping. |
| **Survey Response Values and Contextual Attributes** | value_as_concept_id | OMOP concept identifier representing the response value (e.g., Yes, No, Prefer not to say). |
| **Survey Response Values and Contextual Attributes** | qualifier_concept_id | Concept used to encode contextual qualifiers (e.g., laterality). |
| **Survey Response Values and Contextual Attributes** | qualifier_source_value | Source text representing the qualifier value. |

---

## Purpose

This mapping table supports:

- **Semantic harmonization** of heterogeneous survey instruments  
- **Standardized representation** of patient-reported data within the OMOP CDM  
- **Reproducible survey-to-OMOP transformations**  
- **Interoperable analytics and cohort definition workflows**

The mapping artifacts are designed to facilitate reuse by other investigators seeking to harmonize **survey-derived data into OMOP-based research environments**.
