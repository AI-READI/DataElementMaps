# Auto Generation of OMOP Concept Templates

This project automatically generates OMOP concept and concept relationship templates from medical assessment data sources (MOCA and RedCap) for submission to the OMOP Vocabulary committee.

## Overview

The system follows a concept dictionary architecture to process new medical concepts (concept IDs > 2,000,000,000) from Google Sheets sources and generates standardized CSV files that follow OMOP vocabulary submission requirements. It ensures proper linkage between concept_id_2 relationships and their corresponding concepts.

## Key Features

- **Concept Dictionary Architecture**: Uses concept_id as key with structured sub-dictionaries for concept and concept_relationship data
- **Multi-source processing**: Extracts concepts from MOCA and RedCap assessment mappings
- **Single source of truth**: Gets all metadata from concept_relationship_manual sheet only
- **Database integration**: Queries OMOP database for concept_id_2 relationship details with immediate failure on missing data
- **Unified output**: Produces only concept.csv and concept_relationship.csv (no source-specific files)
- **Source tracking**: Maintains audit trail linking generated values back to source cells

## Project Structure

```
auto_gen_concept_templates/
├── autogen.py              # Main generation script (concept dictionary architecture)
├── validate.py             # Validation script
├── output/                 # Generated CSV files
│   ├── concept.csv         # Combined concept definitions
│   ├── concept_relationship.csv # Combined relationships
│   └── tracking_info.json  # Tracking information for validation
├── old_validation_reports/ # Historical validation reports
├── validation_report.md    # Latest validation report
├── pyproject.toml         # Project configuration
└── README.md
```

## Core Components

### autogen.py (466 lines)
The main generation script implementing the concept dictionary architecture:

**Data Sources Configuration (lines 40-89)**
- `mapping_sources`: MOCA and RedCap Google Sheets containing TARGET_CONCEPT_ID and qualifier_concept_id
- `manual_concept_mappings`: concept_relationship_manual sheet with complete concept metadata
- `output_config`: Defines column specifications for output files
- `omop_field_map`: Maps OMOP database fields to CSV columns

**Core Functions**
- `read_mapping_sources()`: Extracts TARGET_CONCEPT_ID and qualifier_concept_id from mapping sources
- `create_concept_dict()`: Creates concept dictionary with concept_id as key and concept/concept_relationship sub-dicts
- `load_concept_relationship_manual()`: Loads concept_relationship_manual sheet data
- `fill_concept_dict()`: Fills concept dict from manual data and postgres lookups
- `query_omop_concepts()`: Fetches concept_id_2 details from OMOP database
- `save_outputs()`: Saves concept.csv and concept_relationship.csv files

**Key Architecture Changes**
- Uses concept dictionary with concept_id as primary key
- Single data source: concept_relationship_manual sheet only
- No source-specific output files (only combined concept.csv and concept_relationship.csv)
- Immediate failure if concept_id_2 not found in postgres
- Leaves v6_domain_id blank in concept.csv as specified

### validate.py (725 lines)
Comprehensive validation system that compares generated CSVs against manual Google Sheets:

**Configuration (lines 26-43)**
- `validation_targets`: Defines which files to validate (concept.csv and concept_relationship.csv)
- Maps CSV outputs to corresponding Google Sheets worksheets
- Includes worksheet URLs for generating clickable links in reports

**Core Functions**
- `normalize_value()`: Standardizes values for comparison (handles whitespace, case, nulls, number formatting)
- `analyze_difference_type()`: Categorizes differences with explanations and severity levels
- `load_worksheet_data()`: Loads and cleans Google Sheets data using same logic as autogen.py
- `load_csv_data()`: Loads generated CSV files
- `compare_dataframes()`: Performs detailed row-by-row and column-by-column comparison
- `generate_markdown_report()`: Creates comprehensive validation reports

**Validation Logic**
- **Row Matching**: Matches rows by concept_id/concept_id_1 between manual sheets and generated CSVs
- **Column Comparison**: Compares all common columns with tolerance for formatting differences
- **Difference Analysis**: Categorizes differences as:
  - Whitespace-only (ignored)
  - Case differences (low severity)  
  - Missing values (medium severity)
  - Content differences (high severity)
  - Number formatting (low severity)

**Report Structure**
- **Summary Table**: Overview of match rates, errors, and discrepancies for each target
- **Unmatched Concepts**: Lists concepts present in one source but not the other
- **Errors Section**: Critical ID differences requiring immediate attention
- **Discrepancies Section**: Other differences with column match rates and detailed breakdowns
- **Interactive Links**: Clickable links to exact Google Sheets cells and CSV line numbers

**Output Management**
- Generates timestamped reports in `old_validation_reports/` for history
- Creates current `validation_report.md` for latest results
- Provides console summary with key statistics

## Data Flow

### autogen.py Data Flow (New Architecture)

**1. Initialization & Configuration**
- Load environment variables for database connection
- Initialize Google Sheets API client with service account
- Configure data sources (MOCA and RedCap mapping sheets)
- Define output file specifications and OMOP field mappings

**2. Extract Concept IDs from Mapping Sources**
- Connect to MOCA and RedCap mapping spreadsheets
- Extract only `TARGET_CONCEPT_ID` and `qualifier_concept_id` columns
- Filter for new concepts (ID > 2,000,000,000)
- Group concept IDs by source tag for tracking

**3. Create Concept Dictionary**
- Create dictionary with concept_id as key
- Initialize concept and concept_relationship sub-dictionaries with empty columns
- Track which sources each concept_id belongs to
- Set concept_id and concept_id_1 values

**4. Load Manual Data**
- Connect to `template_4_adding_vocabulary-2` spreadsheet
- Load `concept_relationship_manual` sheet only (no concept_manual)
- Clean data by removing empty rows
- Create lookup dictionary by concept_id_1

**5. Fill Concept Dictionary**
- Fill concept and concept_relationship data from manual sheet
- Map column names (handle 'SRC CODE' vs 'SRC_CODE')
- Leave v6_domain_id blank in concept data as specified
- Collect concept_id_2 values for database lookup

**6. Database Enrichment**
- Query OMOP PostgreSQL database for concept_id_2 details
- Fill OMOP-related fields using omop_field_map
- Fail immediately if any concept_id_2 not found in postgres
- Track data source for every value

**7. Output Generation**
- Generate only concept.csv and concept_relationship.csv (no source-specific files)
- Sort by concept_id for consistent ordering
- Ensure proper column order matches manual sheet structure
- Save tracking information to tracking_info.json for validation

### validate.py Data Flow

**1. Initialization & Target Setup**
- Initialize Google Sheets API client
- Define validation targets mapping CSV files to worksheet sources
- Set up comparison parameters (ID columns, worksheet URLs)

**2. Data Loading** (per validation target)
- **Manual Data**: Load from Google Sheets using same cleaning logic as autogen.py
  - Remove subtitle rows and blank entries
  - Track number of skipped rows for accurate row number calculation
- **Generated Data**: Load CSV files from `output/` directory
- Handle missing files gracefully with error reporting

**3. Data Normalization**
- Normalize all values for comparison (trim whitespace, handle nulls)
- Convert data types consistently (handle float/int conversion issues)
- Prepare lookup dictionaries for efficient row matching

**4. Row-by-Row Comparison**
- Match rows by `concept_id`/`concept_id_1` between manual and generated data
- Identify unmatched concepts in each source
- Calculate row numbers for Google Sheets and CSV linking

**5. Column-by-Column Analysis**
- Compare all common columns (excluding ignored columns like 'source', 'Notes')
- Categorize differences by type and severity:
  - Whitespace-only differences (ignored)
  - Case differences (low severity)
  - Missing values (medium severity)  
  - Content differences (high severity)
  - Number formatting differences (low severity)
- Generate column-level match rate statistics

**6. Report Generation**
- Create comprehensive markdown report with:
  - Summary table with match rates and error counts
  - Unmatched concepts sections with clickable links
  - Critical errors section (ID mismatches)
  - Detailed discrepancies with source cell links
  - Column match rate analysis
- Generate both timestamped and current report files

**7. Output & Archiving**
- Save timestamped report to `old_validation_reports/`
- Update current `validation_report.md`
- Print console summary with key statistics
- Provide clickable links to exact Google Sheets cells and CSV line numbers

## Dependencies

- **gspread**: Google Sheets API access
- **pandas**: Data manipulation and CSV generation  
- **psycopg2**: PostgreSQL database connectivity for OMOP queries
- **python-dotenv**: Environment variable management

## Configuration

The system requires:
- Google Sheets service account credentials
- OMOP database connection details in `.env` file
- Proper worksheet access permissions

## Output Files

Generated CSV files follow OMOP vocabulary submission standards:

**concept.csv**: New concept definitions with columns including concept_name, concept_id, vocabulary_id, domain_id, etc. (v6_domain_id left blank as specified)

**concept_relationship.csv**: Relationships between new concepts and existing OMOP concepts, with relationship metadata and OMOP lookups using the omop_field_map.

**tracking_info.json**: Tracking information linking each generated value back to its source for validation purposes.

The new architecture generates only combined files (no source-specific MOCA_* or RedCap_* files) to simplify the output structure while maintaining all necessary data.