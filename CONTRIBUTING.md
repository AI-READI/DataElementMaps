# Contributing to the AI-READI Survey Data Element Commons

Thank you for helping improve the AI-READI survey-to-OMOP mappings. Contributions of all kinds are welcome: reporting an incorrect mapping, suggesting a better standard concept, improving documentation, or fixing scripts.

## Code of Conduct

Everyone participating in this project is expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to <contact@aireadi.org>.

## Asking a question or reporting a mapping issue

Please [open an issue](https://github.com/AI-READI/DataElementMaps/issues/new) and first search [existing issues](https://github.com/AI-READI/DataElementMaps/issues) to avoid duplicates. For a mapping issue, include:

- The `FIELD_ID` and `SRC_CODE` (and the CSV line number, if known)
- The current `TARGET_CONCEPT_ID` and the concept you believe is correct (concept ID, vocabulary and concept code)
- Why the proposed concept is a better fit (e.g., domain, semantics, standard status in the current OMOP vocabulary release)

Do **not** post participant-level data, protected health information, or restricted-access AI-READI data in issues or pull requests.

## Proposing changes

1. Create a branch from `main` for each piece of work (e.g., `fix-moca-src-codes`); do not commit directly to `main`.
2. Edit the working mapping in [`redCapDataDictionaryWithExtension/value-set-mapping-common/`](redCapDataDictionaryWithExtension/value-set-mapping-common/). Files in [`manuscript-tvst2026/`](manuscript-tvst2026/) are a frozen snapshot of the published release and should not be changed.
3. Follow the mapping conventions:
   - Prefer standard OMOP concepts (LOINC, SNOMED CT, UCUM, PPI); create an AI-READI custom concept (ID ≥ 2,000,000,000) only when no suitable standard concept exists, and add it to the OHDSI vocabulary request files in [`redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/`](redCapDataDictionaryWithExtension/OHDSI-vocabulary-request/).
   - Record the SKOS predicate (`skos:exactMatch`, `skos:closeMatch`, `skos:relatedMatch`) and a confidence score; mappings below an exact/close match at 0.75 are flagged for working group review.
   - Record laterality and other context in the qualifier fields.
4. Avoid editing the CSV in Excel, which silently converts long codes to scientific notation and answer ranges (e.g., `3-4`) to dates. Use a text editor, or import all columns as text.
5. Before opening a pull request, run the checks in [`manuscript-tvst2026/`](manuscript-tvst2026/README.md): `count_concept_map.sql` (integrity checks 6a–6d should return zero rows) and, if you have the OMOP vocabulary tables, `validate_mapping_against__omop_vocabulary.sql`.
6. Open a pull request into `main` describing what changed and why, with the affected `FIELD_ID`s. A working group member will review it.

## Commit messages

Use a short, descriptive summary in the imperative (e.g., "Map heart rate to LOINC 8867-4"), referencing CSV line numbers or issue numbers where helpful.

## License

By contributing, you agree that your contributions are your own work and will be licensed under the project's [MIT License](LICENSE).
