Submitter: AI-READI Data Standards Team:  Stephanie S. Hong, Jessical Mitchell, Monique Bangudi, Yvette Chen, Sigfried Gold, Christopher Chute

Organization: [AI-READI Data Standards Team](https://aireadi.org/)

Email: shong59@jh.edu

Data of Submission: Oct 2nd, 2025

[GitHub issue page submitted to OHDSI Vocabulary WG](https://github.com/OHDSI/Vocabulary-v5.0/issues/1176)

## Current custom vocabulary (v1.8.7, 2026-10-29)

This folder holds the current AI-READI custom vocabulary. The October 2025 submission is kept unchanged in `AIREADi_OMOP_Vocabulary_Request/` at the repository root.

| File | Content |
|---|---|
| `concept_manual.csv` | 419 custom concepts (concept IDs 2005200004–2005200636): 407 valid (`standard_concept` = S) and 12 deprecated (`standard_concept` blank) |
| `concept_relationship_manual.csv` | 428 rows: one per custom concept, plus a `Concept replaced by` row for each of the 9 upgraded concepts |
| `AI-READI-Vocabulary/` | Both files split by vocabulary: AIREADI, AIREADI-MOCA, AIREADI-Vision |
| `sql/01_load_vocabulary_manual.sql` | Loads the files (Databricks), builds the splits, and checks that the split files match (L1–L5) |
| `sql/02_validate_concept_relationship_manual.sql` | Checks the relationship file against the OMOP vocabulary and `concept_manual.csv` (R0–R7) |

`SRC_CODE` is the REDCap field name (questions) or `<field>_<code>` (answers), as in the concept map. For four MoCA concepts it differs from the MoCA data dictionary and the October 2025 submission, which use the MoCA names (changed in v1.8.7, as in the concept map since v1.4): 2005200364 `fluency_language` (MoCA `verbal_fluency_language`), 2005200365 `fluency_language_time` (`verbal_fluency_language_time`), 2005200368 `delayed_recall_with_no_clue` (`delayed_recall_with_no_cue`), 2005200369 `delayed_recall_with_no_clue_time` (`delayed_recall_with_no_cue_time`).

Line 2 of `concept_manual.csv` and `concept_relationship_manual.csv` is a blank row, kept so that line numbers do not shift. Rows are only appended.

### Standard and deprecated concepts

- **Valid concepts are standard (S).** The concept map uses every valid custom concept as a target, value or qualifier (`*_concept_id` in OMOP), so each is the standard concept for its meaning.
- **Deprecated concepts** keep their row, so that earlier releases still resolve, with `valid_end_date` and `invalid_reason`, and are not standard:
  - `U` (upgraded, 9): replaced by a standard OMOP concept, given by `Maps to` and `Concept replaced by`.

    | Concept | Name | Replaced by | End date |
    |---|---|---|---|
    | 2005200017 | Kidney problems | 198124 Kidney disease | 10/19/2026 |
    | 2005200121 | The crime rate in my neighborhood makes it unsafe to go on walks… | 40192414 (PPI ips_16) | 10/28/2026 |
    | 2005200182 | White Blood Cells (WBC) - x10E3/µL | 3000905 Leukocytes [#/volume] in Blood by Automated count | 10/16/2026 |
    | 2005200183 | Red Blood Cells (RBC) - x10E6/µL | 3020416 Erythrocytes [#/volume] in Blood by Automated count | 10/16/2026 |
    | 2005200222 | Puff | 45744809 Actuation | 10/19/2026 |
    | 2005200268 | Does not apply to my neighborhood | 40192520 (PPI SDOH_9) | 10/28/2026 |
    | 2005200280 | Did not meet Inclusion/Exclusion criteria | 40480675 Does not meet eligibility criteria for clinical trial | 10/16/2026 |
    | 2005200547 | Elevated A1C levels (elevated blood sugars) | 4214376 Hyperglycemia | 10/29/2026 |
    | 2005200628 | Stroke | 381316 Cerebrovascular accident | 10/19/2026 |

  - `D` (deleted, 3): no replacement; never used by a released concept map: 2005200025, 2005200044, 2005200306 (end date 10/29/2026).
- "Puff" (2005200222) was used by the concept map in v1.0-tvst through v1.3 and removed from `concept_manual.csv` in v1.4. It is restored in v1.8.7 as deprecated (U) so the v1.0-tvst map still resolves.

### relationship_id rules

`predicate_id` keeps the SKOS mapping on every row. `relationship_id` is filled only where OMOP allows it:

| relationship_id | Rule | Rows |
|---|---|---|
| `Maps to`, `Concept replaced by` | Deprecated custom concept (U) to its standard replacement | 9 + 9 |
| `Is a` | `skos:broadMatch` to a standard or classification concept in the same domain | 109 |
| blank (SKOS only) | Every other row: cross-domain links, related, close and narrow matches, exact matches to non-standard concepts, and concepts with no related concept | 301 |
