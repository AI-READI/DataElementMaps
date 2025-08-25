#!/usr/bin/env python3
"""
Automatic Generation of OMOP Concept Templates

This script processes medical/cognitive assessment data from MOCA and RedCap sources
to generate concept templates for submission to the OMOP Vocabulary committee.

The script follows a concept dictionary architecture:
1. Reads concept IDs from mapping sources (TARGET_CONCEPT_ID, qualifier_concept_id)
2. Creates concept dict with concept_id as key and concept/concept_relationship sub-dicts
3. Fills data from concept_relationship_manual and postgres lookups
4. Generates concept.csv and concept_relationship.csv files
5. Saves tracking information for validation

Author: [Your name]
Date: 2025
"""

import gspread
from gspread_dataframe import get_as_dataframe
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, NamedTuple
import psycopg2
import os
import json
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables
load_dotenv()

@dataclass
class SourceTracking:
    """Tracks where a value came from for validation reports."""
    source_type: str  # 'concept_relationship_manual', 'postgres_lookup', 'defaults', 'mapping_source'
    source_cell: Optional[str] = None  # Google Sheets cell reference like 'A5'
    source_url: Optional[str] = None   # Full URL to source cell

# Configuration for source data spreadsheets
mapping_sources = [
    {
        'spreadsheet_name': 'AIREADI MOCA Data Dictionary and Mappings v0.3',
        'worksheet_name': 'MOCA Data Dictionary with Extensions',
        'location': 'https://docs.google.com/spreadsheets/d/1knk4Qru9zhK0CePZ1rLNVMWsKEI4hQ4a8UqR5K9khXc/edit?gid=1779053680#gid=1779053680',
        'process': True,
        'tag': 'MOCA',
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
manual_concept_mappings = {
    'spreadsheet_name': 'template_4_adding_vocabulary-2',
    'worksheet_name': 'concept_relationship_manual',
    'location': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125',
}

# Output file specifications
output_config = {
    'concept.csv': {
        'columns': ['concept_name', 'SRC_CODE', 'concept_id', 'vocabulary_id', 'domain_id', 
                   'v6_domain_id', 'concept_class_id', 'standard_concept', 'valid_start_date',
                   'valid_end_date', 'invalid_reason']
    },
    'concept_relationship.csv': {
        'columns': ['concept_name', 'concept_id_1', 'SRC_CODE', 'vocabulary_id_1', 
                   'relationship_id', 'concept_id_2', 'temp name', 'temp domain', 
                   'vocabulary_id_2', 'temp class', 'concept_code_2', 'temp standard',
                   'relationship_valid_start_date', 'relationship_valid_end_date', 
                   'invalid_reason', 'confidence', 'predicate_id', 'mapping_source',
                   'mapping_justification', 'mapping_tool', 'Notes']
    }
}

# OMOP field mapping for concept_id_2 lookups
omop_field_map = {
    'temp name': 'concept_name',
    'temp domain': 'domain_id',
    'vocabulary_id_2': 'vocabulary_id',
    'temp class': 'concept_class_id',
    'concept_code_2': 'concept_code',
    'temp standard': 'standard_concept'
}

def read_mapping_sources(gc: gspread.Client) -> Dict[str, List[int]]:
    """
    Read the two mapping sources and extract TARGET_CONCEPT_ID and qualifier_concept_id.
    
    Args:
        gc: Authenticated Google Sheets client
        
    Returns:
        Dict mapping source tag to list of concept IDs
    """
    all_concept_ids = {}
    
    for source in mapping_sources:
        if not source['process']:
            continue
            
        tag = source['tag']
        print(f"Reading {tag} mapping source...")
        
        # Load source data
        spreadsheet = gc.open(source['spreadsheet_name'])
        worksheet = spreadsheet.worksheet(source['worksheet_name'])
        df = get_as_dataframe(worksheet)
        
        concept_ids = []
        
        # Extract TARGET_CONCEPT_ID
        if 'TARGET_CONCEPT_ID' in df.columns:
            target_ids = pd.to_numeric(df['TARGET_CONCEPT_ID'], errors='coerce').fillna(0).astype(int)
            valid_targets = target_ids[target_ids > 2000000000].tolist()
            concept_ids.extend(valid_targets)
            print(f"  Found {len(valid_targets)} TARGET_CONCEPT_ID values")
        
        # Extract qualifier_concept_id for RedCap only
        if tag == 'RedCap' and 'qualifier_concept_id' in df.columns:
            qualifier_ids = pd.to_numeric(df['qualifier_concept_id'], errors='coerce').fillna(0).astype(int)
            valid_qualifiers = qualifier_ids[qualifier_ids > 2000000000].tolist()
            concept_ids.extend(valid_qualifiers)
            print(f"  Found {len(valid_qualifiers)} qualifier_concept_id values")
        
        all_concept_ids[tag] = list(set(concept_ids))  # Remove duplicates
        print(f"  Total unique concept IDs for {tag}: {len(all_concept_ids[tag])}")
    
    return all_concept_ids

def create_concept_dict(concept_ids_by_source: Dict[str, List[int]]) -> Dict[int, Dict]:
    """
    Create concept dict with concept_id as key and two dicts to be filled in:
    concept and concept_relationship with appropriate columns starting empty.
    
    Args:
        concept_ids_by_source: Dict mapping source tag to concept ID lists
        
    Returns:
        Dict mapping concept_id to concept and concept_relationship sub-dicts
    """
    concept_dict = {}
    
    # Get all unique concept IDs across sources
    all_concept_ids = set()
    for source_ids in concept_ids_by_source.values():
        all_concept_ids.update(source_ids)
    
    print(f"Creating concept dict for {len(all_concept_ids)} unique concept IDs")
    
    for concept_id in all_concept_ids:
        concept_dict[concept_id] = {
            'concept': {col: '' for col in output_config['concept.csv']['columns']},
            'concept_relationship': {col: '' for col in output_config['concept_relationship.csv']['columns']},
            'source_tags': [],
            'tracking': {}
        }
        
        # Set the concept_id values
        concept_dict[concept_id]['concept']['concept_id'] = concept_id
        concept_dict[concept_id]['concept_relationship']['concept_id_1'] = concept_id
        
        # Determine which sources this concept_id belongs to
        for tag, ids in concept_ids_by_source.items():
            if concept_id in ids:
                concept_dict[concept_id]['source_tags'].append(tag)
    
    return concept_dict

def load_concept_manual(gc: gspread.Client) -> pd.DataFrame:
    """
    Load concept_manual sheet data.
    
    Args:
        gc: Authenticated Google Sheets client
        
    Returns:
        DataFrame with concept_manual data
    """
    print("Loading concept_manual...")
    spreadsheet = gc.open(manual_concept_mappings['spreadsheet_name'])
    worksheet = spreadsheet.worksheet('concept_manual')
    df = get_as_dataframe(worksheet)
    
    # Clean data by removing empty rows
    if 'concept_id' in df.columns:
        df = df[pd.notna(df['concept_id']) & (df['concept_id'] != '')]
        df['concept_id'] = pd.to_numeric(df['concept_id'], errors='coerce').fillna(0).astype(int)
        df = df[df['concept_id'] > 0]
    
    print(f"Loaded {len(df)} rows from concept_manual")
    if len(df) > 0:
        print(f"Columns: {list(df.columns)}")
    
    return df

def load_concept_relationship_manual(gc: gspread.Client) -> pd.DataFrame:
    """
    Load concept_relationship_manual sheet data.
    
    Args:
        gc: Authenticated Google Sheets client
        
    Returns:
        DataFrame with concept_relationship_manual data
    """
    print("Loading concept_relationship_manual...")
    spreadsheet = gc.open(manual_concept_mappings['spreadsheet_name'])
    worksheet = spreadsheet.worksheet(manual_concept_mappings['worksheet_name'])
    df = get_as_dataframe(worksheet)
    
    # Clean data by removing empty rows
    if 'concept_id_1' in df.columns:
        df = df[pd.notna(df['concept_id_1']) & (df['concept_id_1'] != '')]
        df['concept_id_1'] = pd.to_numeric(df['concept_id_1'], errors='coerce').fillna(0).astype(int)
        df = df[df['concept_id_1'] > 0]
    
    print(f"Loaded {len(df)} rows from concept_relationship_manual")
    if len(df) > 0:
        print(f"Columns: {list(df.columns)}")
    
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
    valid_ids = []
    for cid in concept_ids:
        if cid and str(cid).strip() != '' and str(cid).lower() != 'nan':
            try:
                valid_ids.append(int(float(cid)))  # Handle float strings like '123.0'
            except (ValueError, TypeError):
                continue
    
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
        
        # Convert to dictionary
        concept_data = {}
        for row in results:
            concept_data[str(row[0])] = {
                'concept_name': row[1],
                'domain_id': row[2],
                'vocabulary_id': row[3],
                'concept_class_id': row[4],
                'concept_code': row[5],
                'standard_concept': row[6] or ''
            }
        
        cursor.close()
        conn.close()
        
        print(f"Retrieved OMOP data for {len(concept_data)} concept_id_2 values")
        return concept_data
        
    except Exception as e:
        print(f"Error connecting to OMOP database: {e}")
        return {}

def get_column_letter(col_index: int) -> str:
    """Convert column index to Excel-style column letter (0=A, 1=B, etc.)"""
    result = ""
    while col_index >= 0:
        result = chr(col_index % 26 + ord('A')) + result
        col_index = col_index // 26 - 1
        if col_index < 0:
            break
    return result

def create_tracking_info(sheet_type: str, row_index: int, column_name: str, df: pd.DataFrame) -> SourceTracking:
    """Create tracking information for a specific cell"""
    # Get column index
    if column_name in df.columns:
        col_index = list(df.columns).index(column_name)
    else:
        return SourceTracking(sheet_type)
    
    # Generate cell reference (Excel style)
    col_letter = get_column_letter(col_index)
    row_num = row_index + 2  # +2 because row_index is 0-based and there's a header row
    cell_ref = f"{col_letter}{row_num}"
    
    # Generate URL based on sheet type
    if sheet_type == 'concept_manual':
        base_url = "https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=0"  # concept_manual sheet
    else:  # concept_relationship_manual
        base_url = manual_concept_mappings['location']
    
    source_url = f"{base_url}&range={cell_ref}"
    
    return SourceTracking(sheet_type, cell_ref, source_url)

def fill_concept_dict(concept_dict: Dict[int, Dict], concept_manual_df: pd.DataFrame, concept_relationship_manual_df: pd.DataFrame) -> Dict[int, Dict]:
    """
    Fill concept dict from concept_manual and concept_relationship_manual sheets and postgres lookups.
    
    Args:
        concept_dict: The concept dictionary to fill
        concept_manual_df: Manual concept data for concept.csv
        concept_relationship_manual_df: Manual concept relationship data for concept_relationship.csv
        
    Returns:
        Updated concept dictionary
    """
    print("Filling concept dict from manual data and postgres lookups...")
    
    # Create lookup from concept_manual data with row indices for tracking
    concept_manual_lookup = {}
    for idx, row in concept_manual_df.iterrows():
        concept_id = int(row.get('concept_id', 0))
        if concept_id > 0:
            concept_manual_lookup[concept_id] = {
                'data': row.to_dict(),
                'row_index': idx
            }
    
    # Create lookup from concept_relationship_manual data with row indices for tracking
    concept_relationship_manual_lookup = {}
    for idx, row in concept_relationship_manual_df.iterrows():
        concept_id_1 = int(row.get('concept_id_1', 0))
        if concept_id_1 > 0:
            concept_relationship_manual_lookup[concept_id_1] = {
                'data': row.to_dict(),
                'row_index': idx
            }
    
    # Collect concept_id_2 values for postgres lookup
    concept_id_2_values = []
    for concept_id, data in concept_dict.items():
        if concept_id in concept_relationship_manual_lookup:
            manual_row = concept_relationship_manual_lookup[concept_id]['data']
            concept_id_2 = manual_row.get('concept_id_2', '')
            if concept_id_2 and pd.notna(concept_id_2) and str(concept_id_2).strip() and str(concept_id_2).lower() != 'nan':
                concept_id_2_values.append(str(concept_id_2))
    
    # Get OMOP data for concept_id_2 values
    omop_data = query_omop_concepts(list(set(concept_id_2_values)))
    
    filled_count = 0
    missing_concept_count = 0
    missing_relationship_count = 0
    
    for concept_id, data in concept_dict.items():
        # Fill concept data from concept_manual
        if concept_id in concept_manual_lookup:
            manual_entry = concept_manual_lookup[concept_id]
            manual_row = manual_entry['data']
            row_index = manual_entry['row_index']
            concept_data = data['concept']
            
            for col in output_config['concept.csv']['columns']:
                if col == 'concept_id':
                    continue  # Already set
                
                # Map column names if needed
                manual_col = col
                if col == 'SRC_CODE' and 'SRC CODE' in manual_row:
                    manual_col = 'SRC CODE'
                
                if manual_col in manual_row and pd.notna(manual_row[manual_col]):
                    concept_data[col] = manual_row[manual_col]
                    data['tracking'][f'concept.{col}'] = create_tracking_info('concept_manual', row_index, manual_col, concept_manual_df)
        else:
            missing_concept_count += 1
            print(f"Warning: concept_id {concept_id} not found in concept_manual")
        
        # Fill concept_relationship data from concept_relationship_manual
        if concept_id in concept_relationship_manual_lookup:
            manual_entry = concept_relationship_manual_lookup[concept_id]
            manual_row = manual_entry['data']
            row_index = manual_entry['row_index']
            rel_data = data['concept_relationship']
            
            # Specific fields from concept_relationship_manual as per instructions
            relationship_fields = ['concept_name', 'SRC_CODE', 'vocabulary_id_1', 'concept_id_2', 
                                 'confidence', 'predicate_id', 'mapping_source', 
                                 'mapping_justification', 'mapping_tool', 'Notes']
            
            for col in relationship_fields:
                if col == 'concept_id_1':
                    continue  # Already set
                
                # Map column names if needed
                manual_col = col
                if col == 'SRC_CODE' and 'SRC CODE' in manual_row:
                    manual_col = 'SRC CODE'
                
                if manual_col in manual_row and pd.notna(manual_row[manual_col]):
                    rel_data[col] = manual_row[manual_col]
                    data['tracking'][f'concept_relationship.{col}'] = create_tracking_info('concept_relationship_manual', row_index, manual_col, concept_relationship_manual_df)
            
            # Fill OMOP data for concept_id_2 if present
            concept_id_2 = rel_data.get('concept_id_2', '')
            if concept_id_2 and pd.notna(concept_id_2) and str(concept_id_2).strip() and str(concept_id_2).lower() != 'nan':
                concept_id_2_str = str(concept_id_2)
                if concept_id_2_str not in omop_data:
                    print(f"ERROR: concept_id_2 {concept_id_2_str} not found in postgres for concept_id_1 {concept_id}")
                    # Fail immediately as specified
                    raise ValueError(f"concept_id_2 {concept_id_2_str} not found in postgres database")
                
                omop_concept = omop_data[concept_id_2_str]
                for csv_col, omop_field in omop_field_map.items():
                    if omop_field in omop_concept:
                        rel_data[csv_col] = omop_concept[omop_field]
                        data['tracking'][f'concept_relationship.{csv_col}'] = SourceTracking('postgres_lookup')
            
            filled_count += 1
        else:
            missing_relationship_count += 1
            print(f"Warning: concept_id {concept_id} not found in concept_relationship_manual")
    

    print(f"Filled data for {filled_count} concepts")
    if missing_concept_count > 0:
        print(f"Missing from concept_manual: {missing_concept_count} concepts")
    if missing_relationship_count > 0:
        print(f"Missing from concept_relationship_manual: {missing_relationship_count} concepts")
    
    return concept_dict

def save_outputs(concept_dict: Dict[int, Dict], concept_ids_by_source: Dict[str, List[int]]) -> None:
    """
    Save concept.csv and concept_relationship.csv files (no source-specific files).
    
    Args:
        concept_dict: The filled concept dictionary
        concept_ids_by_source: Original concept IDs by source for ordering
    """
    os.makedirs('output', exist_ok=True)
    
    # Prepare concept.csv data
    concept_rows = []
    for concept_id in sorted(concept_dict.keys()):
        data = concept_dict[concept_id]
        row = data['concept'].copy()
        # Remove tracking columns
        concept_rows.append(row)
    
    concept_df = pd.DataFrame(concept_rows)
    concept_df = concept_df[output_config['concept.csv']['columns']]  # Ensure column order
    concept_df.to_csv('output/concept.csv', index=False)
    print(f"Saved output/concept.csv with {len(concept_df)} rows")
    
    # Prepare concept_relationship.csv data
    relationship_rows = []
    for concept_id in sorted(concept_dict.keys()):
        data = concept_dict[concept_id]
        row = data['concept_relationship'].copy()
        # Remove tracking columns
        relationship_rows.append(row)
    
    relationship_df = pd.DataFrame(relationship_rows)
    relationship_df = relationship_df[output_config['concept_relationship.csv']['columns']]  # Ensure column order
    relationship_df.to_csv('output/concept_relationship.csv', index=False)
    print(f"Saved output/concept_relationship.csv with {len(relationship_df)} rows")

def save_tracking_info(concept_dict: Dict[int, Dict]) -> None:
    """
    Save tracking information to a file for use in validate.py.
    
    Args:
        concept_dict: The concept dictionary with tracking info
    """
    tracking_data = {}
    
    for concept_id, data in concept_dict.items():
        tracking_data[str(concept_id)] = {
            'source_tags': data['source_tags'],
            'tracking': {}
        }
        
        # Convert SourceTracking objects to serializable format
        for key, tracking in data['tracking'].items():
            tracking_data[str(concept_id)]['tracking'][key] = {
                'source_type': tracking.source_type,
                'source_cell': tracking.source_cell,
                'source_url': tracking.source_url
            }
    
    with open('output/tracking_info.json', 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    print(f"Saved tracking information for {len(tracking_data)} concepts")

def main() -> None:
    """
    Main function implementing the new concept dictionary architecture.
    """
    try:
        # Initialize Google Sheets client
        gc = gspread.service_account()
        
        # 1. Read the two mapping sources
        print("Step 1: Reading mapping sources...")
        concept_ids_by_source = read_mapping_sources(gc)
        
        # 2. Create concept dict with concept_id as key
        print("\nStep 2: Creating concept dictionary...")
        concept_dict = create_concept_dict(concept_ids_by_source)
        
        # 3. Load both manual sheets and fill concept dict
        print("\nStep 3: Loading manual data and filling concept dict...")
        concept_manual_df = load_concept_manual(gc)
        concept_relationship_manual_df = load_concept_relationship_manual(gc)
        concept_dict = fill_concept_dict(concept_dict, concept_manual_df, concept_relationship_manual_df)
        
        # 4. Save outputs
        print("\nStep 4: Saving output files...")
        save_outputs(concept_dict, concept_ids_by_source)
        
        # 5. Save tracking information
        print("\nStep 5: Saving tracking information...")
        save_tracking_info(concept_dict)
        
        print("\nProcessing complete!")
        print("Generated files:")
        print("- output/concept.csv")
        print("- output/concept_relationship.csv") 
        print("- output/tracking_info.json")
        
    except Exception as e:
        print(f"Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()