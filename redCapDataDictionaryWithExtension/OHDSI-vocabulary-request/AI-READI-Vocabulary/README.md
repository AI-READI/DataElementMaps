 The submission was organized into three groups: AI-READI survey constructs, vision care terms, and MoCA terms. The custom concepts were presented to the monthly OHDSI Survey Working Group meetings, where various mapping strategies were discussed and reviewed.

## Files in this folder (current custom vocabulary)

| File | Concepts |
|---|---|
| `concept_manual_AIREADI.csv` | 334 |
| `concept_manual_AIREADI-Vision.csv` | 54 |
| `concept_manual_AIREADI-MOCA.csv` | 30 |

These files were generated on 2026-10-18 (concept map release v1.3.1) from `../concept_manual.csv`, split by `vocabulary_id`. Together they contain exactly the 418 AI-READI custom concepts in `concept_manual.csv`, with the same columns and values. Regenerate them whenever `concept_manual.csv` changes.

## Frozen October 2025 submission

The files submitted to the OHDSI Vocabulary Working Group on October 2, 2025 ([Vocabulary-v5.0 issue #1176](https://github.com/OHDSI/Vocabulary-v5.0/issues/1176)) are kept unchanged in `AIREADi_OMOP_Vocabulary_Request/split_concept_manual/` at the repository root. Differences from the current files:

- Retired since the submission (not used in the concept map): 2005200193, 2005200236, 2005200239, 2005200560.
- Added since the submission: 2005200455, 2005200632, 2005200633, 2005200634, 2005200635.
- `valid_start_date` now filled (1/1/1970) for 15 MoCA concepts (2005200359–2005200373), and `v6_domain_id` set to `survey_conduct` for 2005200451, 2005200459 and 2005200629.
- Non-breaking spaces removed from the names of 2005200027, 2005200037, 2005200093, 2005200096 and 2005200550.
