# Background 
* The Artificial Intelligence Ready and Equitable Atlas for Diabetes Insights (AI-READI) project is part of the NIH Bridge2AI Common Fund Program, aimed at establishing a robust foundation for the integration of artificial intelligence (AI) in health research.
* This project is specifically designed to advance AI and machine learning (ML) research for Type 2 Diabetes Mellitus (T2DM) by generating ethically sourced and comprehensive datasets from 4,000 participants representing diverse backgrounds and varying T2DM severity levels.

# Introduction - Salutogenesis (AI-READI DGP)
* Data collection utilized 47 custom-designed and well validated survey instruments to capture a broad spectrum of information.
* To maximize data utility, each survey question and answer option were standardized to fit externally managed standard terminology (i.e. ICD10CM, SNOMED, LOINC, RxNorm, etc.), allowing for consistent, interoperable data representations. 
* Used transformation ready value-set mapping table structure for terminology translation
* Utilized Simple Standard for Sharing Ontological Mappings (SSSOM) concept to provide metadata about concept mapping confidence and mapping relationships
* Data was then transformed into the Observational Medical Outcomes Partnership (OMOP) Common Data Model (CDM), ensuring uniformity in format and harmonized to OMOP standard concept.

# Survey Instruments -Participants Exclusion Criteria and Eligibility
* The questionnaire asks participants if they are pregnant or have Type 1 Diabetes, which are both exclusion criteria for the AI-READI study.
* Those who are 40 or older, are not pregnant, and do not have Type 1 Diabetes were then presented with a series of additional questions on previous diabetes diagnoses, diabetes-related medications, biological sex assigned at birth, and race/ethnicity.
* If the answers show that the individual qualifies, then he/she was formally invited to participate.

# Survey Instrument Questionnaires  
- [Demographics Survey](https://docs.aireadi.org/v2/questionnaires/demographics.pdf)
- [General health](https://docs.aireadi.org/v2/questionnaires/general-health.pdf)
- [Diabetes self care](https://docs.aireadi.org/v2/questionnaires/diabetes-self-care.pdf)
- [Center for Epidemiological Studies Depression Scale (CES-D-10) ](https://docs.aireadi.org/v2/questionnaires/depression.pdf)
- [Social Determinants of Health ](https://docs.aireadi.org/v2/questionnaires/sdoh.pdf)
- [Food insecurity](https://docs.aireadi.org/v2/questionnaires/food-security.pdf)
- [Neighborhood environment](https://docs.aireadi.org/v2/questionnaires/neighborhood.pdf)
- [Racial and Ethnic Discrimination](https://docs.aireadi.org/v2/questionnaires/racial.pdf)
- [Problem Areas In Diabetes (PAID-5)](https://docs.aireadi.org/v2/questionnaires/sdoh.pdf)
- [Vision and access to eye care](https://docs.aireadi.org/v2/questionnaires/visual.pdf)
- [Dietary Survey](https://docs.aireadi.org/v2/questionnaires/dietary.pdf)
- [Substance use](https://docs.aireadi.org/v2/questionnaires/substance-use.pdf)
- Medications - Each participant was asked to provide a list of medications. However, these are not currently included in the publicly accessible version 1 dataset.

 # Mapped Survey Instrument Questionairs to Standard Terminology 
 Each survey question was reviewed and mapped to standard terminology concepts (e.g., NIH CDEs, SNOMED CT, LOINC or OMOP standards) to ensure interoperability and alignment with AI-READI's data harmonization goals.
 ## Mapping Overview
 <img width="1805" height="692" alt="image" src="https://github.com/user-attachments/assets/1f70f5fd-debb-40f4-9fe5-7248cea21f8a" />





## Standard Terminology Mappings

The following table illustrates how specific variables from the AI-READI REDCap survey instruments are mapped to standard terminology concepts (e.g., SNOMED CT, LOINC) using OHDSI's Athena vocabulary for interoperability. These mappings ensure alignment with AI-READI's data harmonization goals.

### Simple Mapping Case
| Variable | Domain_id | Concept Code | Maps to Concept_id | URL | Additional Details |
|----------|-----------|--------------|--------------------|-----|--------------------|
| Marital Status | Observation | SNOMED 125680007 | [4053609](https://athena.ohdsi.org/search-terms/terms/4053609) | Value_as_concept_id: “Married” concept_id: 4338692 |
| Troponin-T | Measurement | LOINC 67151-1 | [40769783](https://athena.ohdsi.org/search-terms/terms/40769783) | Code Description: Troponin T.cardiac [Mass/volume] in Serum or Plasma by High sensitivity method |

### Gaps - Survey Questions Not Mappable with existing concepts when 



![The AI-READI project is funded by NIH Award 1OT2OD032644.][(<img width="332" height="270" alt="image" src="https://github.com/user-attachments/assets/dff5f6ad-391a-4f3d-a9a3-7be49b82d8be" />
)
  
 
