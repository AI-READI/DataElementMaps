<div align="center">

<img src="https://freesvg.org/img/1653682897science-svgrepo-com.png" alt="logo" width="200" height="auto" />

<br />

<h1>AI-READI Survey Data Element Commons</h1>

<p>
Mappings of AI-READI REDCap survey, vision care, and cognitive assessment data elements to the OMOP Common Data Model
</p>

<br />

<p>
  <a href="https://github.com/AI-READI/DataElementMaps/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/AI-READI/DataElementMaps.svg?style=flat-square" alt="contributors" />
  </a>
  <a href="https://github.com/AI-READI/DataElementMaps/issues/">
    <img src="https://img.shields.io/github/issues/AI-READI/DataElementMaps.svg?style=flat-square" alt="open issues" />
  </a>
  <a href="https://github.com/AI-READI/DataElementMaps/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/AI-READI/DataElementMaps.svg?style=flat-square" alt="license" />
  </a>
  <a href="https://doi.org/10.5281/zenodo.23375723">
    <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.23375723.svg" alt="doi" />
  </a>
  <a href="https://fairdataihub.org/fairshare">
    <img src="https://raw.githubusercontent.com/fairdataihub/FAIRshare/main/badge.svg" alt="Curated with FAIRshare" />
  </a>
</p>

<h4>
    <a href="manuscript-tvst2026/">Manuscript artifacts</a>
  <span> · </span>
    <a href="redCapDataDictionaryWithExtension/value-set-mapping-common/">Mapping table</a>
  <span> · </span>
    <a href="CHANGELOG.md">Changelog</a>
  <span> · </span>
    <a href="https://github.com/AI-READI/DataElementMaps/issues/">Report an issue</a>
</h4>
</div>

<br />

---

## Description

This repository contains the value-set mappings that transform AI-READI REDCap survey, vision care, and cognitive assessment (MoCA) data elements into standard concepts in the OMOP Common Data Model (CDM v5.3.1). Each survey question and response option is mapped to an OMOP standard concept (LOINC, SNOMED CT, UCUM, PPI) or, where no suitable standard concept exists, to an AI-READI custom extension concept (concept IDs ≥ 2,000,000,000; vocabularies AIREADI, AIREADI-Vision, AIREADI-MOCA). Mappings carry SKOS match predicates and reviewer confidence scores, and are also published as SSSOM and LinkML artifacts.

## Manuscript artifacts (TVST 2026)

The mapping file and SQL scripts used for the manuscript *"A Generalizable Framework for Mapping Survey, Vision Care, and Cognitive Assessment Data to the OMOP Common Data Model in AI-READI"* (Translational Vision Science & Technology, 2026) are in **[`manuscript-tvst2026/`](manuscript-tvst2026/)**, with instructions for reproducing every count reported in the paper.

| Artifact | Location |
|---|---|
| Final mapping file and SQL scripts (frozen for the manuscript) | [`manuscript-tvst2026/`](manuscript-tvst2026/) |
| Working value-set mapping (actively maintained) | [`redCapDataDictionaryWithExtension/value-set-mapping-common/`](redCapDataDictionaryWithExtension/value-set-mapping-common/) |
| SSSOM mapping set | [`redCapDataDictionaryWithExtension/sssom/`](redCapDataDictionaryWithExtension/sssom/) |
| LinkML schema | [`redCapDataDictionaryWithExtension/linkml/`](redCapDataDictionaryWithExtension/linkml/) |
| AI-READI custom vocabulary (OHDSI submission) | [`redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/`](redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/) |
| Superseded mapping files (provenance only) | [`deprecated/`](deprecated/) |

Archived release cited in the paper: **v1.0-tvst** — https://doi.org/10.5281/zenodo.23375723

## Getting started

### Prerequisites/Dependencies

- The mapping files are plain CSV/TSV and can be opened in any spreadsheet tool or loaded into a database.
- To reproduce the manuscript counts locally: the [DuckDB](https://duckdb.org/) CLI, or Python with the `duckdb` package (see [`manuscript-tvst2026/README.md`](manuscript-tvst2026/README.md)).
- To validate mappings against the OMOP Standardized Vocabularies: a Databricks/Spark SQL environment with the vocabulary tables (downloadable from [Athena](https://athena.ohdsi.org/)).

### Inputs and Outputs

- **Input:** the AI-READI REDCap data dictionary ([`redCapDataDictionaryWithExtension/redcap-data-dictionary/`](redCapDataDictionaryWithExtension/redcap-data-dictionary/)).
- **Output:** the value-set mapping table, one row per survey question or response option, with OMOP target concept, domain, vocabulary, SKOS predicate, confidence, and value/qualifier concepts. Field definitions are in [`value-set-mapping-common/README.md`](redCapDataDictionaryWithExtension/value-set-mapping-common/README.md).

## Contributing

<a href="https://github.com/AI-READI/DataElementMaps/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AI-READI/DataElementMaps" />
</a>

Contributions are always welcome!

If you are interested in reporting/fixing issues and contributing directly to the code base, please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information on what we're looking for and how to get started.

## Issues and Feedback

To report an incorrect mapping, suggest an improvement, or request a new feature, please open a new issue via the [Issues](https://github.com/AI-READI/DataElementMaps/issues) tab. For mapping issues, include the FIELD_ID or SRC_CODE and the concept you believe is correct.

## License

This work is licensed under
[MIT](https://opensource.org/licenses/mit). See [LICENSE](LICENSE) for more information.

The AI-READI dataset itself is shared under a custom license developed as part of the project. Read the [AI-READI dataset license](https://zenodo.org/records/17555036) first to make sure your intended use fits its requirements.

<a href="https://aireadi.org" >
  <img src="https://www.channelfutures.com/files/2017/04/3_0.png" height="30" />
</a>

## How to cite

If you use these mappings, please cite the manuscript and the archived release:

```
Hong S, et al. A Generalizable Framework for Mapping Survey, Vision Care, and Cognitive
Assessment Data to the OMOP Common Data Model in AI-READI. Transl Vis Sci Technol. 2026.

AI-READI Survey Data Element Commons, release v1.0-tvst. Zenodo.
https://doi.org/10.5281/zenodo.23375723
```

## Acknowledgements

This project is funded by the NIH under award number 1OT2OD032644, R01AG060942, and an unrestricted research grant from Research to Prevent Blindness. 
The content is solely the responsibility of the authors and does not necessarily represent the official views of the NIH.
The funders/sponsors had no role in the design and conduct of the study; collection, management, analysis, and interpretation of the data; preparation, review, or approval of the manuscript; and decision to submit the manuscript for publication. 




<br />
