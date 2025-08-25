# Auto Generation of OMOP Concept Templates

This project automatically generates OMOP concept and concept relationship templates from medical assessment data sources (MOCA and RedCap) for submission to the OMOP Vocabulary committee.

## Overview

The system processes new medical concepts (concept IDs > 2,000,000,000) from multiple Google Sheets sources and generates standardized CSV files that follow OMOP vocabulary submission requirements. It combines data extraction, metadata enrichment, and validation reporting to ensure accuracy.

## Key Features

- **Multi-source processing**: Extracts concepts from MOCA and RedCap assessment mappings
- **Metadata enrichment**: Combines concept IDs from mapping sources with full metadata from manual template sheets
- **Database integration**: Queries OMOP database for relationship concept details
- **Validation reporting**: Comprehensive validation with discrepancy tracking and clickable links
- **Source tracking**: Maintains audit trail linking generated values back to source cells

## Project Structure

```
auto_gen_concept_templates/
├── autogen.py              # Main generation script
├── validate.py             # Validation script
├── output/                 # Generated CSV files
│   ├── concept.csv         # Combined concept definitions
│   ├── concept_relationship.csv # Combined relationships
│   ├── MOCA_concept.csv    # MOCA-specific concepts
│   ├── MOCA_concept_relationship.csv
│   ├── RedCap_concept.csv  # RedCap-specific concepts
│   └── RedCap_concept_relationship.csv
├── old_validation_reports/ # Historical validation reports
├── validation_report.md    # Latest validation report
├── pyproject.toml         # Project configuration
└── README.md
```

## Core Components

### autogen.py (722 lines)
The main generation script with several key modules:

**Data Sources Configuration (lines 50-109)**
- `mapping_sources`: MOCA and RedCap Google Sheets containing new concepts
- `manual_concept_mappings`: Template sheet with full concept metadata
- `output_config`: Defines required columns and defaults for output files

**Core Functions**
- `extract_source_concepts()`: Extracts only concept IDs from mapping sources
- `load_manual_concept_data()`: Loads complete concept metadata from manual template
- `query_omop_concepts()`: Fetches relationship concept details from OMOP database
- `create_concept_csv()`: Generates concept definition output
- `create_concept_relationship_csv()`: Generates relationship output

**Key Architecture Decisions**
- Separates concept ID extraction from metadata population
- Preserves manual sheet row ordering in outputs
- Tracks data sources for every value (Google Sheets cells, database lookups, defaults)
- Supports both individual and combined output files

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

### autogen.py Data Flow

**1. Initialization & Configuration**
- Load environment variables for database connection
- Initialize Google Sheets API client with service account
- Configure data sources (MOCA and RedCap mapping sheets)
- Define output file specifications and column defaults

**2. Manual Template Loading**
- Connect to `template_4_adding_vocabulary-2` spreadsheet
- Load `concept_manual` sheet (fallback to `concept_relationship_manual`)
- Clean data by removing subtitle rows and blank entries
- Create lookup dictionaries for concept metadata

**3. Source Data Extraction** (per source: MOCA, RedCap)
- Connect to mapping source spreadsheet (MOCA or RedCap)
- Extract only `TARGET_CONCEPT_ID` and `qualifier_concept_id` columns
- Filter for new concepts (ID > 2,000,000,000) or extension-needed concepts
- Create `ConceptData` objects with source cell tracking information
- Generate Google Sheets URLs linking back to source cells

**4. Database Enrichment**
- Collect unique `concept_id_2` values from manual template
- Query OMOP PostgreSQL database for relationship concept details
- Retrieve concept names, domains, vocabularies, classes for relationships
- Add database lookup tracking to enriched data

**5. CSV Generation** (per source)
- **concept.csv**: Combine extracted concept IDs with manual template metadata
- **concept_relationship.csv**: Add OMOP database lookups for relationship concepts
- Preserve manual sheet row ordering in outputs
- Apply tag-specific defaults (e.g., MOCA concepts default to Montreal Cognitive Assessment)
- Track data source for every value (manual sheet, database, defaults)

**6. Output Management**
- Generate individual source files (`MOCA_concept.csv`, `RedCap_concept.csv`, etc.)
- Create combined files (`concept.csv`, `concept_relationship.csv`)
- Remove internal tracking columns before saving
- Save all outputs to `output/` directory

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

**concept.csv**: New concept definitions with columns like concept_name, concept_id, vocabulary_id, domain_id, etc.

**concept_relationship.csv**: Relationships between new concepts and existing OMOP concepts, with relationship metadata and OMOP lookups.

Both individual source files (MOCA_*, RedCap_*) and combined files are generated for submission flexibility.