#!/usr/bin/env python3
"""
Automatic Generation of OMOP Concept Templates

This script processes medical/cognitive assessment data from MOCA and RedCap sources
to generate concept templates for submission to the OMOP Vocabulary committee.

The script:
1. Reads concept IDs from Google Sheets (TARGET_CONCEPT_ID, qualifier_concept_id only)
2. Gets all concept metadata including SRC_CODE from manual mapping sheets
3. Generates two output files per source:
   - concept.csv: New concept definitions
   - concept_relationship.csv: Relationships between concepts
4. Tracks source cell links and value generation sources for validation reports

Author: [Your name]
Date: 2025
"""

import gspread
from gspread_dataframe import get_as_dataframe
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, NamedTuple
import psycopg2
import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables
load_dotenv()

@dataclass
class SourceTracking:
    """Tracks where a value came from for validation reports."""
    source_type: str  # 'concept_manual', 'concept_relationship_manual', 'postgres_lookup', 'defaults'
    source_cell: Optional[str] = None  # Google Sheets cell reference like 'A5'
    source_url: Optional[str] = None   # Full URL to source cell

@dataclass
class ConceptData:
    """Represents extracted concept data with tracking."""
    concept_id: int
    src_code: str
    is_qualifier_derived: bool = False
    tracking: Optional[SourceTracking] = None

# Configuration for source data spreadsheets
# Each source contains new concepts that need to be added to OMOP vocabulary
# Only TARGET_CONCEPT_ID and qualifier_concept_id are extracted from these sources
mapping_sources = [
    {
        'spreadsheet_name': 'AIREADI MOCA Data Dictionary and Mappings v0.3',
        'worksheet_name': 'MOCA Data Dictionary with Extensions',
        'location': 'https://docs.google.com/spreadsheets/d/1knk4Qru9zhK0CePZ1rLNVMWsKEI4hQ4a8UqR5K9khXc/edit?gid=1779053680#gid=1779053680',
        'process': True,  # Whether to process this source
        'tag': 'MOCA',    # Identifier used in output filenames and processing logic
    },
    {
        'spreadsheet_name': 'REDCap Data Dictionary and OMOP Mappings',
        'worksheet_name': '_master REDCap Data Dictionary with Extensions',
        'location': 'https://docs.google.com/spreadsheets/d/1hIP0lZc5fxl-4_KO_0J6EnYLecbarXq60UNey3sJ9es/edit?gid=1423561967#gid=1423561967',
        'process': True,
        'tag': 'RedCap',
    },
]

# Manual concept mappings - contains all concept metadata and relationships
# This is the primary source for concept names, vocabularies, domains, etc.
manual_concept_mappings = {
    'spreadsheet_name': 'template_4_adding_vocabulary-2',
    'worksheet_name': 'concept_relationship_manual',
    'location': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125',
}

# Output file specifications - simplified to essential columns and defaults
output_config = {
    'concept.csv': {
        'required_columns': ['concept_name', 'SRC_CODE', 'concept_id', 'vocabulary_id', 
                           'domain_id', 'v6_domain_id', 'concept_class_id', 'standard_concept', 'valid_start_date'],
        'defaults': {
            'valid_start_date': '1/1/1970',
            'valid_end_date': '',
            'invalid_reason': ''
        }
    },
    'concept_relationship.csv': {
        'required_columns': ['concept_name', 'concept_id_1', 'SRC_CODE', 'vocabulary_id_1', 
                           'concept_id_2', 'relationship_id'],
        'defaults': {
            'concept_id_2': {'MOCA': '606671', 'RedCap': ''},  # MOCA default to Montreal Cognitive Assessment
            'relationship_id': '',
            'temp name': '',
            'temp domain': '',
            'vocabulary_id_2': '',
            'temp class': '',
            'concept_code_2': '',
            'temp standard': '',
            'relationship_valid_start_date': '',
            'relationship_valid_end_date': '',
            'invalid_reason': '',
            'confidence': '',
            'predicate_id': '',
            'mapping_source': '',
            'mapping_justification': '',
            'mapping_tool': '',
            'Notes': ''
        }
    }
}

def clean_worksheet_data(df: pd.DataFrame, id_column: str = 'concept_id_1') -> pd.DataFrame:
    """
    Clean a dataframe by removing subtitle rows and blank rows.
    Dynamically detects data boundaries instead of using hardcoded indices.
    
    Args:
        df: Raw dataframe from Google Sheets
        id_column: Column name to use for detecting data boundaries
        
    Returns:
        Cleaned dataframe with only valid data rows
    """
    if df.empty or id_column not in df.columns:
        return df
    
    # Skip first row if it contains subtitles (check if ID column is not numeric)
    start_idx = 0
    if pd.isna(pd.to_numeric(df.iloc[0][id_column], errors='coerce')):
        start_idx = 1
    
    # Find last row with data (ID column not empty)
    end_idx = len(df)
    for idx in range(len(df) - 1, -1, -1):
        if pd.notna(df.iloc[idx][id_column]) and str(df.iloc[idx][id_column]).strip() != '':
            end_idx = idx + 1
            break
    
    return df.iloc[start_idx:end_idx].fillna('')


def load_manual_concept_data(gc: gspread.Client) -> pd.DataFrame:
    """
    Load manual concept mappings that contain all concept metadata.
    This is the primary source for concept names, vocabularies, domains, etc.
    
    Args:
        gc: Authenticated Google Sheets client
        
    Returns:
        DataFrame with all manual concept data
    """
    spreadsheet = gc.open(manual_concept_mappings['spreadsheet_name'])
    
    # Try to load concept_manual sheet first, fallback to concept_relationship_manual
    try:
        worksheet = spreadsheet.worksheet('concept_manual')
        print(f"Loading from 'concept_manual' sheet")
    except:
        worksheet = spreadsheet.worksheet(manual_concept_mappings['worksheet_name'])
        print(f"Loading from '{manual_concept_mappings['worksheet_name']}' sheet")
    
    df = get_as_dataframe(worksheet)
    
    # Print debug info about columns
    print(f"Manual sheet columns: {list(df.columns)}")
    
    # Clean the dataframe - use concept_id for concept_manual, concept_id_1 for concept_relationship_manual
    id_column = 'concept_id' if 'concept_id' in df.columns else 'concept_id_1'
    df = clean_worksheet_data(df, id_column)
    
    print(f"Loaded {len(df)} rows from manual sheet")
    if len(df) > 0:
        print(f"Sample row keys: {list(df.iloc[0].keys())}")
    
    return df


def query_omop_concepts(concept_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Query OMOP concept table for given concept_id values.
    
    Args:
        concept_ids: List of concept IDs to look up
        
    Returns:
        Dictionary mapping concept_id to concept data from OMOP database
    """
    # Get database credentials from environment
    db_config = {
        'host': os.getenv('OMOP_DB_HOST'),
        'port': os.getenv('OMOP_DB_PORT', 5432),
        'database': os.getenv('OMOP_DB_NAME'),
        'user': os.getenv('OMOP_DB_USER'),
        'password': os.getenv('OMOP_DB_PASSWORD'),
        'options': f"-c search_path={os.getenv('OMOP_DB_SCHEMA', 'public')}"
    }
    
    # Filter out empty concept IDs
    valid_ids = [int(cid) for cid in concept_ids if cid and str(cid).strip() != '']
    
    if not valid_ids:
        return {}
    
    try:
        # Connect to database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Query for concept data
        placeholders = ','.join(['%s'] * len(valid_ids))
        query = f"""
            SELECT concept_id, concept_name, domain_id, vocabulary_id, 
                   concept_class_id, concept_code, standard_concept
            FROM concept
            WHERE concept_id IN ({placeholders})
        """
        
        cursor.execute(query, valid_ids)
        results = cursor.fetchall()
        
        # Convert to dictionary with tracking info
        concept_data = {}
        for row in results:
            concept_data[str(row[0])] = {
                'concept_name': row[1],
                'domain_id': row[2],
                'vocabulary_id': row[3],
                'concept_class_id': row[4],
                'concept_code': row[5],
                'standard_concept': row[6],
                '_source_tracking': SourceTracking('postgres_lookup')
            }
        
        cursor.close()
        conn.close()
        
        return concept_data
        
    except Exception as e:
        print(f"Error connecting to OMOP database: {e}")
        return {}


def extract_source_concepts(gc: gspread.Client, source: Dict[str, Any]) -> List[ConceptData]:
    """
    Extract only the concept IDs (TARGET_CONCEPT_ID, qualifier_concept_id)
    from a mapping source spreadsheet. SRC_CODE will come from manual sheets.
    
    Args:
        gc: Authenticated Google Sheets client
        source: Source configuration dictionary
        
    Returns:
        List of ConceptData objects with tracking information
    """
    tag = source['tag']
    
    # Load source data
    spreadsheet = gc.open(source['spreadsheet_name'])
    worksheet = spreadsheet.worksheet(source['worksheet_name'])
    df = get_as_dataframe(worksheet)
    
    concepts = []
    
    # Only extract concept ID columns - SRC_CODE comes from manual sheet
    required_columns = ['TARGET_CONCEPT_ID']
    optional_columns = ['qualifier_concept_id']
    
    # Verify required columns exist
    for col in required_columns:
        if col not in df.columns:
            print(f"Warning: Required column '{col}' not found in {tag} source")
            return concepts
    
    # Convert TARGET_CONCEPT_ID to numeric
    df['TARGET_CONCEPT_ID'] = pd.to_numeric(df['TARGET_CONCEPT_ID'], errors='coerce').fillna(0).astype(int)
    
    # Convert qualifier_concept_id to numeric if it exists
    if 'qualifier_concept_id' in df.columns:
        df['qualifier_concept_id'] = pd.to_numeric(df['qualifier_concept_id'], errors='coerce').fillna(0).astype(int)
    
    # Filter for new concepts (ID > 2000000000)
    filtered_df = df[df['TARGET_CONCEPT_ID'] > 2000000000].copy()
    
    # Process regular concepts
    for idx, row in filtered_df.iterrows():
        concept_id = int(row['TARGET_CONCEPT_ID'])
        
        # Create tracking info for source cell
        row_num = idx + 2  # +2 for header and 1-indexed
        # Determine TARGET_CONCEPT_ID column letter
        col_index = list(df.columns).index('TARGET_CONCEPT_ID')
        col_letter = chr(ord('A') + col_index) if col_index < 26 else f"A{chr(ord('A') + col_index - 26)}"
        cell_ref = f"{col_letter}{row_num}"
        source_url = f"{source['location']}&range={cell_ref}"
        
        tracking = SourceTracking(
            source_type='concept_manual',
            source_cell=cell_ref,
            source_url=source_url
        )
        
        concepts.append(ConceptData(
            concept_id=concept_id,
            src_code='',  # SRC_CODE will be filled from manual sheet
            is_qualifier_derived=False,
            tracking=tracking
        ))
    
    # Process qualifier concepts if qualifier_concept_id column exists
    if 'qualifier_concept_id' in df.columns:
        qualifier_df = df[df['qualifier_concept_id'] > 2000000000]
        for idx, row in qualifier_df.iterrows():
            qualifier_id = int(row['qualifier_concept_id'])
            
            # Create tracking info for qualifier source cell
            row_num = idx + 2
            # Determine qualifier_concept_id column letter (usually different from A)
            col_index = list(df.columns).index('qualifier_concept_id')
            col_letter = chr(ord('A') + col_index) if col_index < 26 else f"A{chr(ord('A') + col_index - 26)}"
            cell_ref = f"{col_letter}{row_num}"
            source_url = f"{source['location']}&range={cell_ref}"
            
            tracking = SourceTracking(
                source_type='concept_manual',
                source_cell=cell_ref,
                source_url=source_url
            )
            
            concepts.append(ConceptData(
                concept_id=qualifier_id,
                src_code='',  # SRC_CODE will be filled from manual sheet
                is_qualifier_derived=True,
                tracking=tracking
            ))
    
    return concepts


def create_concept_csv(concepts: List[ConceptData], manual_df: pd.DataFrame, tag: str) -> pd.DataFrame:
    """
    Create concept.csv output using extracted concepts and manual mapping data.
    Row order will match the manual sheet order.
    
    Args:
        concepts: List of extracted concept data
        manual_df: Manual concept mapping dataframe
        tag: Source tag (MOCA or RedCap)
        
    Returns:
        DataFrame ready for concept.csv output
    """
    config = output_config['concept.csv']
    rows = []
    
    # Determine the correct ID column
    id_column = 'concept_id' if 'concept_id' in manual_df.columns else 'concept_id_1'
    print(f"Using ID column: {id_column}")
    
    # Create lookup dictionary from manual data and preserve row order
    manual_lookup = {str(int(row[id_column])): row for _, row in manual_df.iterrows() 
                    if pd.notna(row[id_column])}
    
    # Get the order from the manual sheet
    manual_order = [str(int(row[id_column])) for _, row in manual_df.iterrows() 
                   if pd.notna(row[id_column])]
    
    print(f"Manual lookup has {len(manual_lookup)} entries")
    print(f"Manual order has {len(manual_order)} entries")
    
    # Create concept lookup for quick access
    concept_lookup = {str(concept.concept_id): concept for concept in concepts}
    
    # Process concepts in the order they appear in the manual sheet
    processed_count = 0
    for concept_id_str in manual_order:
        concept = concept_lookup.get(concept_id_str)
        if not concept:
            continue  # Skip if this concept is not in our extracted list
        
        concept_id_str = str(concept.concept_id)
        manual_row = manual_lookup.get(concept_id_str, {})
        
        if processed_count == 0:  # Debug first row
            print(f"Processing first concept {concept_id_str}")
            print(f"Manual row found: {len(manual_row) > 0}")
            if len(manual_row) > 0:
                print(f"Manual row columns: {list(manual_row.keys())}")
        
        # Build row data with tracking in the exact manual sheet order
        row_data = {
            'concept_name': '',
            'SRC_CODE': '',  # Will be filled from manual sheet
            'concept_id': concept.concept_id,
            'vocabulary_id': '',
            'domain_id': '',
            'v6_domain_id': '',
            'concept_class_id': '',
            'standard_concept': '',
            'valid_start_date': '',
            'valid_end_date': '',
            'invalid_reason': '',
            '_source_tracking': concept.tracking,
            '_column_tracking': {}
        }
        
        # Fill from manual data with tracking
        for col in config['required_columns']:
            if col == 'concept_id':
                continue  # Already handled
            
            # Handle both SRC_CODE and SRC CODE column name formats
            manual_col = col
            if col == 'SRC_CODE' and col not in manual_row and 'SRC CODE' in manual_row:
                manual_col = 'SRC CODE'
            
            if manual_col in manual_row and pd.notna(manual_row[manual_col]) and str(manual_row[manual_col]).strip():
                row_data[col] = manual_row[manual_col]
                row_data['_column_tracking'][col] = SourceTracking('concept_relationship_manual')
                if processed_count == 0:  # Debug first row
                    print(f"Filled {col} from manual: {manual_row[manual_col]}")
            else:
                # Use defaults
                row_data[col] = config['defaults'].get(col, '')
                row_data['_column_tracking'][col] = SourceTracking('defaults')
                if processed_count == 0:  # Debug first row
                    print(f"Used default for {col}: manual_col={manual_col}, in_manual={manual_col in manual_row}")
        
        processed_count += 1
        
        # Add defaults
        for col, default_val in config['defaults'].items():
            if col not in row_data:
                row_data[col] = default_val
                row_data['_column_tracking'][col] = SourceTracking('defaults')
        
        rows.append(row_data)
    
    # Convert to DataFrame with exact manual sheet column ordering
    column_order = ['concept_name', 'SRC_CODE', 'concept_id', 'vocabulary_id', 'domain_id', 
                   'v6_domain_id', 'concept_class_id', 'standard_concept', 'valid_start_date', 
                   'valid_end_date', 'invalid_reason', '_source_tracking', '_column_tracking']
    df = pd.DataFrame(rows, columns=column_order)
    
    # Ensure integer types for concept IDs
    if 'concept_id' in df.columns:
        df['concept_id'] = df['concept_id'].astype(int)
    
    return df


def create_concept_relationship_csv(concepts: List[ConceptData], manual_df: pd.DataFrame, tag: str) -> pd.DataFrame:
    """
    Create concept_relationship.csv output using extracted concepts and manual mapping data.
    Row order will match the manual sheet order.
    
    Args:
        concepts: List of extracted concept data
        manual_df: Manual concept mapping dataframe
        tag: Source tag (MOCA or RedCap)
        
    Returns:
        DataFrame ready for concept_relationship.csv output
    """
    config = output_config['concept_relationship.csv']
    rows = []
    
    # Determine the correct ID column
    id_column = 'concept_id' if 'concept_id' in manual_df.columns else 'concept_id_1'
    
    # Create lookup dictionary from manual data
    manual_lookup = {str(int(row[id_column])): row for _, row in manual_df.iterrows() 
                    if pd.notna(row[id_column])}
    
    # Get the order from the manual sheet
    manual_order = [str(int(row[id_column])) for _, row in manual_df.iterrows() 
                   if pd.notna(row[id_column])]
    
    # Create concept lookup for quick access
    concept_lookup = {str(concept.concept_id): concept for concept in concepts}
    
    # Get unique concept_id_2 values for OMOP lookup
    concept_id_2_values = []
    for concept_id_str in manual_order:
        concept = concept_lookup.get(concept_id_str)
        if not concept or concept.is_qualifier_derived:
            continue  # Skip OMOP lookups for qualifier-derived concepts
        manual_row = manual_lookup.get(concept_id_str, {})
        concept_id_2 = manual_row.get('concept_id_2', '')
        if concept_id_2 and str(concept_id_2).strip():
            concept_id_2_values.append(str(concept_id_2))
    
    # Query OMOP database for concept_id_2 data
    omop_data = query_omop_concepts(list(set(concept_id_2_values)))
    
    # Process concepts in the order they appear in the manual sheet
    for concept_id_str in manual_order:
        concept = concept_lookup.get(concept_id_str)
        if not concept:
            continue  # Skip if this concept is not in our extracted list
        concept_id_str = str(concept.concept_id)
        manual_row = manual_lookup.get(concept_id_str, {})
        
        # Build row data with tracking in exact manual sheet order
        row_data = {
            'concept_name': '',
            'concept_id_1': concept.concept_id,
            'SRC_CODE': '',  # Will be filled from manual sheet
            'vocabulary_id_1': '',
            'relationship_id': '',
            'concept_id_2': '',
            'temp name': '',
            'temp domain': '',
            'vocabulary_id_2': '',
            'temp class': '',
            'concept_code_2': '',
            'temp standard': '',
            'relationship_valid_start_date': '',
            'relationship_valid_end_date': '',
            'invalid_reason': '',
            'confidence': '',
            'predicate_id': '',
            'mapping_source': '',
            'mapping_justification': '',
            'mapping_tool': '',
            'Notes': '',
            '_source_tracking': concept.tracking,
            '_column_tracking': {}
        }
        
        # Fill concept_id_2 (with defaults for MOCA)
        concept_id_2 = manual_row.get('concept_id_2', '')
        if concept_id_2 and str(concept_id_2).strip():
            row_data['concept_id_2'] = concept_id_2
            row_data['_column_tracking']['concept_id_2'] = SourceTracking('concept_relationship_manual')
        else:
            # Use tag-specific defaults
            default_id_2 = config['defaults']['concept_id_2'].get(tag, '')
            row_data['concept_id_2'] = default_id_2
            row_data['_column_tracking']['concept_id_2'] = SourceTracking('defaults')
        
        # Fill other required columns from manual data
        for col in config['required_columns']:
            if col in ['concept_id_1', 'concept_id_2']:
                continue  # Already handled
            
            # Handle both SRC_CODE and SRC CODE column name formats
            manual_col = col
            if col == 'SRC_CODE' and col not in manual_row and 'SRC CODE' in manual_row:
                manual_col = 'SRC CODE'
            
            if manual_col in manual_row and pd.notna(manual_row[manual_col]) and str(manual_row[manual_col]).strip():
                row_data[col] = manual_row[manual_col]
                row_data['_column_tracking'][col] = SourceTracking('concept_relationship_manual')
            else:
                row_data[col] = config['defaults'].get(col, '')
                row_data['_column_tracking'][col] = SourceTracking('defaults')
        
        # Fill OMOP data if concept_id_2 exists and not qualifier-derived
        if not concept.is_qualifier_derived and str(row_data['concept_id_2']).strip():
            omop_concept = omop_data.get(str(row_data['concept_id_2']), {})
            omop_columns = ['temp name', 'temp domain', 'vocabulary_id_2', 'temp class', 
                          'concept_code_2', 'temp standard']
            omop_field_map = {
                'temp name': 'concept_name',
                'temp domain': 'domain_id',
                'vocabulary_id_2': 'vocabulary_id',
                'temp class': 'concept_class_id',
                'concept_code_2': 'concept_code',
                'temp standard': 'standard_concept'
            }
            
            for col in omop_columns:
                omop_field = omop_field_map[col]
                if omop_field in omop_concept:
                    row_data[col] = omop_concept[omop_field]
                    row_data['_column_tracking'][col] = SourceTracking('postgres_lookup')
                else:
                    row_data[col] = config['defaults'].get(col, '')
                    row_data['_column_tracking'][col] = SourceTracking('defaults')
        
        # Fill remaining defaults
        for col, default_val in config['defaults'].items():
            if col not in row_data:
                if isinstance(default_val, dict):
                    row_data[col] = default_val.get(tag, '')
                else:
                    row_data[col] = default_val
                row_data['_column_tracking'][col] = SourceTracking('defaults')
        
        rows.append(row_data)
    
    # Convert to DataFrame with exact manual sheet column ordering
    column_order = ['concept_name', 'concept_id_1', 'SRC_CODE', 'vocabulary_id_1', 'relationship_id',
                   'concept_id_2', 'temp name', 'temp domain', 'vocabulary_id_2', 'temp class', 
                   'concept_code_2', 'temp standard', 'relationship_valid_start_date', 
                   'relationship_valid_end_date', 'invalid_reason', 'confidence', 'predicate_id',
                   'mapping_source', 'mapping_justification', 'mapping_tool', 'Notes',
                   '_source_tracking', '_column_tracking']
    df = pd.DataFrame(rows, columns=column_order)
    
    # Ensure integer types for concept IDs
    if 'concept_id_1' in df.columns:
        df['concept_id_1'] = df['concept_id_1'].astype(int)
    
    return df


def process_source_data(gc: gspread.Client, source: Dict[str, Any], manual_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Process data from a single source (MOCA or RedCap).
    
    Args:
        gc: Authenticated Google Sheets client
        source: Source configuration dictionary
        manual_df: Manual concept mapping dataframe
        
    Returns:
        Dictionary of output dataframes keyed by filename
    """
    tag = source['tag']
    
    # Extract only essential concept data
    concepts = extract_source_concepts(gc, source)
    
    # Create output files
    result_dfs = {
        'concept.csv': create_concept_csv(concepts, manual_df, tag),
        'concept_relationship.csv': create_concept_relationship_csv(concepts, manual_df, tag)
    }
    
    # Add source tag to each dataframe
    for df in result_dfs.values():
        df['source'] = tag
    
    return result_dfs



def save_outputs(output_dfs: Dict[str, Dict[str, pd.DataFrame]]) -> None:
    """
    Save all output dataframes to CSV files.
    Creates both individual source files and combined files.
    Removes tracking columns before saving.
    
    Args:
        output_dfs: Nested dictionary of dataframes by source and filename
    """
    combined_dfs = {}
    
    # Save individual source files and collect for combined output
    for tag, dfs in output_dfs.items():
        for fname, df in dfs.items():
            # Remove tracking columns before saving
            clean_df = df.copy()
            tracking_columns = [col for col in clean_df.columns if col.startswith('_')]
            clean_df = clean_df.drop(columns=tracking_columns)
            
            # Save individual source file
            filename = f'output/{tag}_{fname}'
            clean_df.to_csv(filename, index=False)
            print(f"Saved {filename} with {len(clean_df)} rows")
            
            # Collect for combined file
            if fname not in combined_dfs:
                combined_dfs[fname] = []
            combined_dfs[fname].append(clean_df)
    
    # Save combined files
    for fname, dfs in combined_dfs.items():
        combined_df = pd.concat(dfs, ignore_index=True)
        filename = f'output/{fname}'
        combined_df.to_csv(filename, index=False)
        print(f"Saved {filename} with {len(combined_df)} rows")


def main() -> None:
    """
    Main function to orchestrate the concept template generation process.
    """
    try:
        # Initialize Google Sheets client
        gc = gspread.service_account()
        
        # Load manual concept mappings (primary source for concept metadata)
        print("Loading manual concept mappings...")
        manual_df = load_manual_concept_data(gc)
        print(f"Loaded {len(manual_df)} manual concept mappings")
        
        # Process each source
        output_dfs = {}
        for source in mapping_sources:
            if not source['process']:
                continue
            
            print(f"\nProcessing {source['tag']} data...")
            print(f"  Extracting concepts from: {source['worksheet_name']}")
            output_dfs[source['tag']] = process_source_data(gc, source, manual_df)
            
            # Print summary
            for fname, df in output_dfs[source['tag']].items():
                print(f"  Generated {len(df)} rows for {fname}")
        
        # Save all outputs
        print("\nSaving output files...")
        save_outputs(output_dfs)
        
        print("\nProcessing complete!")
        print("\nSummary:")
        print("- Only TARGET_CONCEPT_ID and qualifier_concept_id extracted from mapping sources")
        print("- All concept metadata including SRC_CODE comes from manual mapping sheets")
        print("- Source cell links and value generation tracking added for validation reports")
        
    except Exception as e:
        print(f"Error during processing: {e}")
        raise


if __name__ == "__main__":
    main()