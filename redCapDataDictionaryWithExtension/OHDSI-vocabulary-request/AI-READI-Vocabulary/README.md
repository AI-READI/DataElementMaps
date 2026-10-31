 The submission was organized into three groups: AI-READI survey constructs, vision care terms, and MoCA terms. The custom concepts were presented to the monthly OHDSI Survey Working Group meetings, where various mapping strategies were discussed and reviewed.

## Files in this folder (current custom vocabulary, v1.8.7)

| File | Rows | Valid (S) | Deprecated (U / D) |
|---|---|---|---|
| `concept_manual_AIREADI.csv` | 335 | 323 | 9 / 3 |
| `concept_manual_AIREADI-Vision.csv` | 54 | 54 | 0 |
| `concept_manual_AIREADI-MOCA.csv` | 30 | 30 | 0 |
| `concept_relationship_manual_AIREADI.csv` | 344 (326 concepts + 18 `Maps to` / `Concept replaced by` rows) | | |
| `concept_relationship_manual_AIREADI-Vision.csv` | 54 | | |
| `concept_relationship_manual_AIREADI-MOCA.csv` | 30 | | |

These files were regenerated on 2026-10-29 (concept map release v1.8.7) from `../concept_manual.csv` and `../concept_relationship_manual.csv`, split by `vocabulary_id` (`vocabulary_id_1` for the relationship file). Together they contain exactly the 419 concepts and 428 relationship rows of the main files, with the same columns and values; the main files also have a blank line 2, which the splits do not. Regenerate them whenever a main file changes, and check them with `../sql/01_load_vocabulary_manual.sql` (L3, L5).

`standard_concept` is S for the 407 valid concepts and blank for the 12 deprecated ones; see `../README.md` for the deprecated concepts and the relationship_id rules.

## Frozen October 2025 submission

The files submitted to the OHDSI Vocabulary Working Group on October 2, 2025 ([Vocabulary-v5.0 issue #1176](https://github.com/OHDSI/Vocabulary-v5.0/issues/1176)) are kept unchanged in `AIREADi_OMOP_Vocabulary_Request/split_concept_manual/` and `split_concept_relationship_manual/` at the repository root. Differences from the current files:

- Retired since the submission (removed from the concept map and from `concept_manual.csv` in v1.4): 2005200193, 2005200236, 2005200239, 2005200560. 2005200222 "Puff" was also removed in v1.4 and is restored in v1.8.7 as deprecated (U, replaced by 45744809 Actuation), because the v1.0-tvst concept map uses it.
- Deprecated in v1.8.7 (kept, with `valid_end_date` and `invalid_reason`): 9 upgraded (U) and 3 deleted (D) concepts; see `../README.md`.
- `standard_concept` set to S for every valid concept (v1.8.7).
- `SRC_CODE` of 2005200364, 2005200365, 2005200368 and 2005200369 set to the REDCap field names (`fluency_language`, `fluency_language_time`, `delayed_recall_with_no_clue`, `delayed_recall_with_no_clue_time`), as in the concept map (v1.8.7).
- Added since the submission: 2005200455, 2005200632, 2005200633, 2005200634, 2005200635, 2005200636 (v1.5).
- `valid_start_date` now filled (1/1/1970) for 15 MoCA concepts (2005200359–2005200373), and `v6_domain_id` set to `survey_conduct` for 2005200451, 2005200459 and 2005200629.
- Non-breaking spaces removed from the names of 2005200027, 2005200037, 2005200093, 2005200096 and 2005200550.
