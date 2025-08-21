# autogen.py Development History

## Initial Request (Session 1)

**User's Initial Instructions:**
"First, can you clean up and add some documentation for autogen.py? I wrote it, but was rushed and dealt with changes sloppily. If the intent of any part of it isn't clear, just ask. There ended up being fewer differences between MOCA and RedCap than I thought there would be, and the way I handle it might be simplified.

The last change I made was to fill concept_relationship_manual.concept_id_2 from another spreadsheet. The next change, after the cleanup, will be to fill temp name, temp domain, vocabulary_id_2, temp class, concept_code_2, temp standard with values from another source."

## Notes
- The script processes MOCA and RedCap data sources to generate OMOP concept templates
- Outputs are used for submission to the OMOP Vocabulary committee
- Individual source files are kept for validation purposes
- The next major task will be filling in the columns after concept_id_2 from another source

## Clarification Q&A

### 1. Purpose of the script
**Question**: It appears to be mapping medical/cognitive assessment data from MOCA and RedCap sources to OMOP CDM format. Is this correct?

**Answer**: The two main source worksheets contain new concepts my team needs added to the OMOP concept tables.
The purpose of the output is to submit to the OMOP Vocabulary committee for them to add them in the next release.
concept_id_2 from the other worksheet (concept_rel_man_old) are mappings others on my team found/added manually as the
best available concepts from the existing OMOP concept table. (It's possible that some of these are not ideal, and,
perhaps after doing everything else, we could look at verifying and maybe improving them.)

Others on the team composed concept_manual and concept_relationship_manual (concept_rel_man_old) manually, and
we know there are problems with them. My script is meant to make more reliable versions of these.

### 2. Hardcoded row slice (lines 80-81)
**Question**: You have `crm_df.iloc[1:415]` with a comment about subtitle row and blank rows. Should I make this more dynamic by detecting the actual data boundaries?

**Answer**: Sure.

### 3. concept_id_2 logic (lines 110-114)
**Question**: For MOCA, it uses values from the `cid2` lookup or defaults to '606671', while RedCap uses the lookup or leaves blank. Is this intentional? What does concept_id_2 represent?

**Answer**: That is correct. The MOCA concepts all come from the Montreal Cognitive Assessment version 8.1 (OMOP:606671)
but if more specific concepts were found, those are used.

### 4. The defaultMOCA values
**Question**: There are many MOCA-specific defaults (like 'Montreal Cognitive Assessment version 8.1', SNOMED codes, etc.). Are these specific to MOCA assessments, and should RedCap have different defaults or truly remain blank?

**Answer**: Most or all of the MOCA defaults will be replaced in the next step. You can leave all columns to the
right of concept_id_2 blank for now and we'll fill them in in the next steps.

### 5. Output structure
**Question**: The script generates both individual files per source (MOCA_*.csv, RedCap_*.csv) and combined files. Is this dual output intentional?

**Answer**: Yeah, it makes it easier (for someone else on my team) to validate against the manually generated
worksheets. Maybe after everything else, we'll write some code to do that validation automatically. Also, I
realize, it would probably make more sense for our outputs to be concept.csv and concept_relationship.csv; 
'_manual' was added to those worksheet names, presumably, because they were manually composed.

None of the worksheets are publicly accessible. If you would like to view their contents, tell me the easiest way
to provide them.

### Additional Note
**User**: "Actually, since I've already validated that concept_id_1 is perfectly fine as a primary key, I don't know if we need those checking functions anymore"

## Completed Tasks

1. ✅ Analyze code structure and identify areas needing clarification
2. ✅ Add module-level docstring and improve imports organization
3. ✅ Add documentation to data structures (mapping_sources, outputs)
4. ✅ Refactor main() function with proper documentation and structure
5. ✅ Simplify MOCA/RedCap handling logic
6. ✅ Document and improve primary key validation functions (removed per user request)
7. ✅ Add type hints and improve error handling
8. ✅ Make row slicing dynamic instead of hardcoded
9. ✅ Rename output files from *_manual.csv to *.csv
10. ✅ Remove MOCA-specific defaults for columns right of concept_id_2

## Summary of Changes Made

### Code Organization
- Split monolithic main() function into smaller, focused functions:
  - `clean_dataframe()`: Dynamically detects and removes subtitle/blank rows
  - `load_concept_mappings()`: Loads existing concept_id mappings
  - `process_source_data()`: Processes data from a single source
  - `process_output_file()`: Handles output file specification
  - `save_outputs()`: Saves all dataframes to CSV files

### Documentation Improvements
- Added comprehensive module-level docstring
- Added detailed comments for data structures
- Added proper docstrings with type hints for all functions

### Code Improvements
- Replaced hardcoded row slicing with dynamic boundary detection
- Added type hints throughout
- Improved error handling with try/except
- Removed primary key validation functions (no longer needed)
- Renamed output files from `*_manual.csv` to `*.csv`
- Set all columns after concept_id_2 to blank defaults (to be filled in next step)

### Simplified Logic
- Made MOCA/RedCap handling more consistent
- Extracted repeated logic into helper functions
- Improved readability and maintainability

## Next Steps / Future Instructions

**Place for subsequent instructions:**

### Session 2 Instructions:
For these columns:
    temp name, temp domain, vocabulary_id_2, temp class, concept_code_2, temp standard
we will get values from the OMOP concept table based on concept_id_2 with these column
mappings:
    temp name: concept_name
    temp domain: domain_id
    vocabulary_id_2: vocabulary_id
    temp class: concept_class_id
    concept_code_2: concept_code
    temp standard: standard_concept
I have a copy of the OMOP concept table in a local postgres server. How should I provide
the credentials?

These:
    relationship_valid_start_date, relationship_valid_end_date, invalid_reason 
can be left blank

For these columns:
    confidence, predicate_id, mapping_source, mapping_justification, mapping_tool
take the values from concept_rel_man_old.

## Session 2 Summary

### Completed Tasks
1. ✅ Added database connection functionality using .env file
2. ✅ Created function to query OMOP concept table for concept_id_2 values  
3. ✅ Updated process_output_file to fill temp columns from OMOP database
4. ✅ Loaded additional columns from concept_rel_man_old spreadsheet
5. ✅ Added error handling for missing concept_id_2 values
6. ✅ Created supporting files (.env.example)

### Implementation Details

#### Database Integration
- Added PostgreSQL connectivity using psycopg2
- Implemented `get_omop_concepts()` function to query OMOP concept table
- Uses environment variables from .env file (including OMOP_DB_SCHEMA)
- Handles missing/invalid concept IDs gracefully

#### Column Mappings Implemented
**From OMOP concept table (based on concept_id_2):**
- temp name ← concept_name
- temp domain ← domain_id  
- vocabulary_id_2 ← vocabulary_id
- temp class ← concept_class_id
- concept_code_2 ← concept_code
- temp standard ← standard_concept

**From concept_rel_man_old spreadsheet:**
- confidence
- predicate_id
- mapping_source
- mapping_justification
- mapping_tool

**Left blank as specified:**
- relationship_valid_start_date
- relationship_valid_end_date
- invalid_reason

### Key Changes to Code Structure
- Modified `load_concept_mappings()` to return full DataFrame instead of dictionary
- Updated `process_output_file()` to handle database queries and additional column population
- Changed function signatures to pass crm_df instead of simple mapping dictionary
- Added type conversion for concept IDs to help identify data errors

### User Notes
- User uses Poetry instead of pip (packages added to pyproject.toml)
- User modified line 177 to convert concept IDs to int for better error detection
- Database credentials provided via .env file with additional OMOP_DB_SCHEMA parameter

### Session 3 Instructions:
Now let's add validation against the manually generated worksheets. This can go
in a separate script and compare the generated CSVs against the worksheets. 

    concept = {
        'spreadsheet_name': 'template_4_adding_vocabulary-2',
        'worksheet_name': 'concept_manual',
        'csv': 'output/concept.csv'
    }
    concept_relationship = {
        'spreadsheet_name': 'template_4_adding_vocabulary-2',
        'worksheet_name': 'concept_relationship_manual',
        'csv': 'output/concept_relationship.csv'
    }

#### Session 3 Clarification Questions:

**1. Comparison scope**: Should I compare all columns, or are there specific columns that are most important to validate?

**Answer**: 
I guess just compare all columns.


**2. Matching strategy**: How should I match rows between the CSV and worksheet? By concept_id/concept_id_1, or by a combination of fields like (concept_name, SRC_CODE)?

**Answer**: Just concept_id and concept_id_1 will suffice


**3. Report format**: Would you prefer:
   - A summary report (e.g., "95% match, 10 discrepancies found")
   - Detailed row-by-row differences 
   - Both?

**Answer**: Both


**4. Output format**: Console output, CSV file, or both?

**Answer**: Markdown might be good


**5. Tolerance for differences**: Should the comparison be exact match only, or should I handle things like:
   - Whitespace differences
   - Case sensitivity
   - Empty strings vs NaN/null values

**Answer**: I think you can ignore those differences

## Response

I've created a comprehensive validation script (validate.py) that addresses all your requirements:

### Features:

#### Data Loading & Matching

  - Loads data from Google Sheets (manual worksheets) and CSV files (generated)
  - Matches rows using concept_id/concept_id_1 as specified
  - Handles data cleaning similar to autogen.py

#### Comparison Logic

  - Compares all columns between manual and generated data
  - Handles tolerance for whitespace, case sensitivity, and null/empty value differences
  - Excludes the 'source' column that only exists in generated data

#### Report Generation

  - Summary Report: Overall match rates, row counts, unmatched rows
  - Detailed Report: Row-by-row differences, column-specific match rates
  - Markdown Output: Clean, readable format saved to timestamped files

#### Key Components

  1. normalize_value(): Handles whitespace/case/null differences
  2. compare_dataframes(): Main comparison logic
  3. generate_markdown_report(): Creates comprehensive markdown reports

### Usage

  poetry run python validate.py

### Output

  - Console summary with key statistics
  - Detailed markdown report saved as validation_report_YYYYMMDD_HHMMSS.md

  The script will:
  1. Compare both concept.csv and concept_relationship.csv against their manual worksheets
  2. Show match rates for each column
  3. List unmatched rows (IDs that exist in one but not the other)
  4. Detail specific differences for rows that exist in both but have different values
  5. Handle edge cases like empty dataframes or missing files

  This should give you a comprehensive view of how well your generated files match the manual worksheets!
  
### Addendum
