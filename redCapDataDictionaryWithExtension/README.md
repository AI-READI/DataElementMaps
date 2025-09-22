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
 - Map data elements to standard concepts using the OMOP CDM vocabulary and established concept relationships.
 - Apply FAIR principles (Findable, Accessible, Interoperable, Reusable) through tools such as FAIRshare.
 - Manage variable extensions and create custom concepts to address terminology gaps.
 
 ## Mapping Overview
 <img width="1805" height="692" alt="image" src="https://github.com/user-attachments/assets/1f70f5fd-debb-40f4-9fe5-7248cea21f8a" />





## Standard Terminology Mappings Explained

The following table illustrates how specific variables from the AI-READI REDCap survey instruments are mapped to standard terminology concepts (e.g., SNOMED CT, LOINC) using OHDSI's Athena vocabulary for interoperability. These mappings ensure alignment with AI-READI's data harmonization goals.

### 1. Simple Mapping Case
| Variable | Domain_id | Concept Code | Maps to Concept_id | URL | Additional Details |
|----------|-----------|--------------|--------------------|-----|--------------------|
| Marital Status | Observation | SNOMED 125680007 | [4053609](https://athena.ohdsi.org/search-terms/terms/4053609) | Value_as_concept_id: “Married” concept_id: 4338692 |
| Troponin-T | Measurement | LOINC 67151-1 | [40769783](https://athena.ohdsi.org/search-terms/terms/40769783) | Code Description: Troponin T.cardiac [Mass/volume] in Serum or Plasma by High sensitivity method |

### 2. Gaps – Survey questions that cannot be mapped when no standard terminology exists
| Survey Question | Domain_id | Concept Code | Maps to Concept_id | URL | Additional Details |
|-----------------|-----------|--------------|--------------------|-----|--------------------|
| Worrying about the future and the possibility of serious complications | Observation | [TBD] | [2005200046](https://athena.ohdsi.org/search-terms/terms/2005200046) | Likely from PAID-5 survey; Maps to diabetes distress concept |
| How often have you been treated unfairly by teachers and professors because of your race/ethnic group? | Observation | [TBD] | [2005200126](https://athena.ohdsi.org/search-terms/terms/2005200126) | Likely from Social Determinants of Health survey; Maps to racial/ethnic discrimination concept |

### 3. Complex - Both the survey question and its corresponding response must be combined to map the data accurately. A dual mapping approach was applied to capture both the answer response and the self-reported condition in the Condition domain.
| # | Survey Question                                                                 | Response Options                |
|---|----------------------------------------------------------------------------------|---------------------------------|
| First part of the question | Has a doctor or other healthcare professional ever told you that you have/had a heart attack? | ☐ Yes ☐ No ☐ Prefer not to say |
| Second part of the question - option 1| Other heart issues (e.g., pacemaker, heart valve disease, open heart surgery)    | ☐ Yes ☐ No ☐ Prefer not to say |
| Second part of the question - option 2 | Stroke                                                                           | ☐ Yes ☐ No ☐ Prefer not to say |
| Second part of the question - option 3 | Circulation problems (e.g., arteriosclerosis, atherosclerosis, blood clots in lungs or leg veins) | ☐ Yes ☐ No ☐ Prefer not to say |
| Second part of the question - option 4 | High blood cholesterol                                                           | ☐ Yes ☐ No ☐ Prefer not to say |
| Second part of the question - option 5 | High blood pressure                                                              | ☐ Yes ☐ No ☐ Prefer not to say |
| Second part of the question - option 6 | Low blood pressure                                                               | ☐ Yes ☐ No ☐ Prefer not to say |
| Second part of the question - option 7 | Parkinson’s disease                                                              | ☐ Yes ☐ No ☐ Prefer not to say |
| Second part of the question - option 8 | Dementia (e.g., Alzheimer’s disease, vascular dementia, etc.)                    | ☐ Yes ☐ No ☐ Prefer not to say |


**Notes**:
- Concept IDs are mapped to the OHDSI Athena vocabulary. URLs are provided for reference, but specific Concept Codes (e.g., SNOMED CT, LOINC) are pending confirmation.
- These questions align with AI-READI's focus on diabetes-related distress and social determinants of health, mapped to standard terminologies for interoperability.
- For full REDCap dictionary data element mapping details, see the [Core REDCap Data Dictionary Data Element Mapping Structure](#core-redcap-data-dictionary-structure) section.


[<img width="332" height="270" alt="image" src="https://github.com/user-attachments/assets/dff5f6ad-391a-4f3d-a9a3-7be49b82d8be" />](https://aireadi.org/)

The AI-READI project is funded by NIH Award 1OT2OD032644.


  
 
