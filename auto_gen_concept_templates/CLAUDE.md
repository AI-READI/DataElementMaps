There are some logic problems in autogen.py. Particularly, concept_id_2 stuff is getting disconnected from the concepts it should go with in the
output. Let's try changing the architecture a bit. Try something like this:

- Start by reading the two mapping_sources
- extract TARGET_CONCEPT_ID from both and qualifier_concept_id from RedCap
- create a concept dict with concept id as key and two dicts to be filled in: concept and
  concept_relationship with the appropriate columns (starting empty) from output_config.
- There is no reason to call some fields required. The output columns and order should match the
  columns from the appropriate manual sheet .
- All fields should be filled in if they can in the following orders:
  - for concept.csv:
    - concept_id from target concept in the mapping sheets
    - everything else from concept_manual from the matching row by concept_id
  - for concept_relationship.csv:
    - target and qualifier concept ids from mapping
    - concept_id_2 from concept_relationship_manual
    - the OMOP related concept fields from:
   
          omop_field_map = {
              'temp name': 'concept_name',
              'temp domain': 'domain_id',
              'vocabulary_id_2': 'vocabulary_id',
              'temp class': 'concept_class_id',
              'concept_code_2': 'concept_code',
              'temp standard': 'standard_concept'
          }
    - If concept_relationship_manual has a non-blank concept_id_2, raise an error if it's
      not found in the OMOP lookup
    - concept_name, SRC_CODE, vocabulary_id_1, confidence, predicate_id, mapping_source,
      mapping_justification, mapping_tool, and Notes should be filled from
      concept_relationship_manual
    - relationship_id, relationship_valid_start_date, relationship_valid_end_date,
      invalid_reason are always blank, which is fine
- There is no longer a need for the source-specific csv files. Just produce concept.csv
  and concept_relationship.csv
- Tracking information is being collected for use in validate.py, but it's not actually
  being saved and not being referenced in validate.py yet. Save it to a file, but don't
  change validate.py yet.