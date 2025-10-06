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

# [Survey Instruments](https://github.com/AI-READI/DataElementMaps/wiki/Survey-Instruments)


# [Map Survey Instruments to Standard Terminology](https://github.com/AI-READI/DataElementMaps/wiki/Map-Survey-Instruments-to-Standard-Terminology)

# [AI‐READI Survey Data Element Mapping Table Guide](https://github.com/AI-READI/DataElementMaps/wiki/AI%E2%80%90READI-Survey-Data-Element-Mapping-Table-Guide)

**Notes**:
- Concept IDs are mapped to the OHDSI Athena vocabulary. URLs are provided for reference, but specific Concept Codes (e.g., SNOMED CT, LOINC, AI-READI custom concepts) are pending confirmation.
- These questions align with AI-READI's focus on diabetes-related distress and social determinants of health, mapped to standard terminologies for interoperability.
- For full REDCap dictionary data element mapping details, see the [Core REDCap Data Dictionary Data Element Mapping Structure](https://github.com/AI-READI/DataElementMaps/blob/main/redCapDataDictionaryWithExtension/redcap-data-dictionary/_master_red_cap_data_dictionary_with_extensions.csv) section.

<p align="center">
  <a href="https://aireadi.org/">
    <img width="332" height="270" alt="image" src="https://github.com/user-attachments/assets/dff5f6ad-391a-4f3d-a9a3-7be49b82d8be" />
  </a>
</p>

The AI-READI project is funded by NIH Award 1OT2OD032644.

[This work was presented at the Bridge2AI Leadership Meeting Science Talk](https://bridge2ai.org/event/bridge2ai-fall-2024-leadership-meeting/))


  
 
