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
from gspread_dataframe import get_as_dataframe, set_with_dataframe
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

# Spreadsheet configuration - contains all manual and generated worksheets
spreadsheet_config = {
    'spreadsheet_name': 'template_4_adding_vocabulary-2',
    'spreadsheet_id': '1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY',
    'base_url': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit',
    'worksheets': {
        'concept_manual': {
            'gid': '535320917',
            'url': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917'
        },
        'concept_relationship_manual': {
            'gid': '933853125', 
            'url': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125'
        },
        'concept_generated': {
            'gid': 'TBD',  # Will be determined dynamically
            'url': 'TBD'   # Will be determined dynamically
        },
        'concept_relationship_generated': {
            'gid': 'TBD',  # Will be determined dynamically
            'url': 'TBD'   # Will be determined dynamically
        }
    }
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
    spreadsheet = gc.open(spreadsheet_config['spreadsheet_name'])
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
    spreadsheet = gc.open(spreadsheet_config['spreadsheet_name'])
    worksheet = spreadsheet.worksheet('concept_relationship_manual')
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
    row_num = row_index + 3  # +3 because row_index is 0-based, plus header row, plus subheader row
    cell_ref = f"{col_letter}{row_num}"
    
    # Generate URL based on sheet type
    if sheet_type in spreadsheet_config['worksheets']:
        base_url = spreadsheet_config['worksheets'][sheet_type]['url']
    else:
        base_url = f"{spreadsheet_config['base_url']}?gid=0#gid=0"
    
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

def copy_subheader_and_formatting(source_worksheet, target_worksheet, target_df: pd.DataFrame) -> None:
    """
    Copy subheader row and formatting from source worksheet to target worksheet.
    
    Args:
        source_worksheet: Source worksheet to copy from
        target_worksheet: Target worksheet to copy to
        target_df: The data dataframe being written
    """
    print(f"Copying subheader and formatting from {source_worksheet.title} to {target_worksheet.title}...")
    
    try:
        # Get the subheader row (row 1, 0-indexed) from source
        source_raw = get_as_dataframe(source_worksheet, header=None)
        if len(source_raw) < 2:
            print("Source sheet doesn't have a subheader row")
            return
            
        subheader_row = source_raw.iloc[1].tolist()  # Get row 1 (subheader)
        
        # Prepare batch update requests
        requests = []
        
        # Get target sheet ID 
        target_sheet_metadata = target_worksheet.spreadsheet.fetch_sheet_metadata()
        target_sheet_id = None
        for sheet in target_sheet_metadata['sheets']:
            if sheet['properties']['title'] == target_worksheet.title:
                target_sheet_id = sheet['properties']['sheetId']
                break
        
        if target_sheet_id is None:
            print(f"Could not find target sheet ID for {target_worksheet.title}")
            return
            
        # Set reasonable column widths
        standard_widths = {
            0: 400,   # concept_name - much wider for long descriptions
            1: 120,   # SRC_CODE 
            2: 100,   # concept_id
            3: 120,   # vocabulary_id
            4: 120,   # domain_id
            5: 120,   # v6_domain_id
            6: 140,   # concept_class_id
            7: 100,   # standard_concept
            8: 120,   # dates and other fields
        }
        
        # Apply column widths
        for col_index in range(min(len(target_df.columns), 20)):  # Don't go beyond reasonable number
            width = standard_widths.get(col_index, 120)  # Default width
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': target_sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': col_index,
                        'endIndex': col_index + 1
                    },
                    'properties': {
                        'pixelSize': width
                    },
                    'fields': 'pixelSize'
                }
            })
        
        # Insert a blank row at the top for the subheader
        requests.append({
            'insertDimension': {
                'range': {
                    'sheetId': target_sheet_id,
                    'dimension': 'ROWS',
                    'startIndex': 1,  # Insert after header row
                    'endIndex': 2
                },
                'inheritFromBefore': False
            }
        })
        
        # Execute the insert first
        if requests:
            target_worksheet.spreadsheet.batch_update({'requests': requests})
        
        # Now add the subheader content and formatting
        requests = []
        
        # Add subheader row content (matching columns from target_df)
        subheader_values = []
        for col_name in target_df.columns:
            col_idx = list(source_raw.iloc[0]).index(col_name) if col_name in source_raw.iloc[0].values else -1
            if col_idx >= 0 and col_idx < len(subheader_row):
                subheader_values.append(subheader_row[col_idx] if pd.notna(subheader_row[col_idx]) else "")
            else:
                subheader_values.append("")
        
        # Update subheader row with values
        if subheader_values:
            # Convert to the range format that gspread expects
            cell_range = f"A2:{get_column_letter(len(subheader_values)-1)}2"
            target_worksheet.update(values=[subheader_values], range_name=cell_range)
        
        # Format header row (bold, dark gray background)
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': target_sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': len(target_df.columns)
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {
                            'bold': True
                        },
                        'backgroundColor': {
                            'red': 0.8,
                            'green': 0.8,
                            'blue': 0.8,
                            'alpha': 1.0
                        }
                    }
                },
                'fields': 'userEnteredFormat(textFormat,backgroundColor)'
            }
        })
        
        # Format subheader row (italic, light gray background)
        requests.append({
            'repeatCell': {
                'range': {
                    'sheetId': target_sheet_id,
                    'startRowIndex': 1,
                    'endRowIndex': 2,
                    'startColumnIndex': 0,
                    'endColumnIndex': len(target_df.columns)
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {
                            'italic': True,
                            'fontSize': 9
                        },
                        'backgroundColor': {
                            'red': 0.95,
                            'green': 0.95,
                            'blue': 0.95,
                            'alpha': 1.0
                        },
                        'wrapStrategy': 'WRAP'
                    }
                },
                'fields': 'userEnteredFormat(textFormat,backgroundColor,wrapStrategy)'
            }
        })
        
        # Execute formatting batch update
        if requests:
            target_worksheet.spreadsheet.batch_update({'requests': requests})
            print(f"Applied subheader and {len(requests)} formatting updates successfully")
    
    except Exception as e:
        print(f"Error copying subheader and formatting: {e}")
        import traceback
        traceback.print_exc()

def save_outputs(concept_dict: Dict[int, Dict], concept_ids_by_source: Dict[str, List[int]], gc: gspread.Client) -> None:
    """
    Save data to concept_generated and concept_relationship_generated worksheets.
    Copy formatting and column widths from manual sheets.
    
    Args:
        concept_dict: The filled concept dictionary
        concept_ids_by_source: Original concept IDs by source for ordering
        gc: Authenticated Google Sheets client
    """
    # Prepare concept data
    concept_rows = []
    for concept_id in sorted(concept_dict.keys()):
        data = concept_dict[concept_id]
        row = data['concept'].copy()
        # Remove tracking columns
        concept_rows.append(row)
    
    concept_df = pd.DataFrame(concept_rows)
    concept_df = concept_df[output_config['concept.csv']['columns']]  # Ensure column order
    
    # Prepare concept_relationship data
    relationship_rows = []
    for concept_id in sorted(concept_dict.keys()):
        data = concept_dict[concept_id]
        row = data['concept_relationship'].copy()
        # Remove tracking columns
        relationship_rows.append(row)
    
    relationship_df = pd.DataFrame(relationship_rows)
    relationship_df = relationship_df[output_config['concept_relationship.csv']['columns']]  # Ensure column order
    
    # Open the spreadsheet
    spreadsheet = gc.open(spreadsheet_config['spreadsheet_name'])
    
    # For now, save to CSV files - Google Sheets writing needs manual worksheet creation
    # TODO: Manually create concept_generated and concept_relationship_generated worksheets first
    # Then uncomment the Google Sheets writing code below
    
    # Save to CSV files with blank first row to match subheader structure
    os.makedirs('output', exist_ok=True)
    
    # Add blank first row to concept CSV for subheader space
    concept_df_with_blank = pd.concat([pd.DataFrame([[''] * len(concept_df.columns)], columns=concept_df.columns), concept_df], ignore_index=True)
    concept_df_with_blank.to_csv('output/concept.csv', index=False)
    
    # Add blank first row to relationship CSV for subheader space
    relationship_df_with_blank = pd.concat([pd.DataFrame([[''] * len(relationship_df.columns)], columns=relationship_df.columns), relationship_df], ignore_index=True)
    relationship_df_with_blank.to_csv('output/concept_relationship.csv', index=False)
    
    print(f"Saved concept.csv with {len(concept_df)} data rows (plus blank subheader row)")
    print(f"Saved concept_relationship.csv with {len(relationship_df)} data rows (plus blank subheader row)")
    print("NOTE: To write to Google Sheets, manually create 'concept_generated' and 'concept_relationship_generated' worksheets first")
    
    try:
        concept_worksheet = spreadsheet.worksheet('concept_generated')
        print("Found existing concept_generated worksheet, clearing it...")
        concept_worksheet.clear()
        print(f"Writing {len(concept_df)} rows to concept_generated worksheet...")
        set_with_dataframe(concept_worksheet, concept_df, include_index=False)
        print(f"Saved concept_generated worksheet with {len(concept_df)} rows")
        
        # Copy subheader and formatting from concept_manual
        try:
            concept_manual_worksheet = spreadsheet.worksheet('concept_manual')
            copy_subheader_and_formatting(concept_manual_worksheet, concept_worksheet, concept_df)
        except Exception as e:
            print(f"Could not copy subheader and formatting from concept_manual: {e}")
            
    except Exception as e:
        print(f"concept_generated worksheet not found or error occurred: {e}")

    try:
        relationship_worksheet = spreadsheet.worksheet('concept_relationship_generated')
        print("Found existing concept_relationship_generated worksheet, clearing it...")
        relationship_worksheet.clear()
        print(f"Writing {len(relationship_df)} rows to concept_relationship_generated worksheet...")
        set_with_dataframe(relationship_worksheet, relationship_df, include_index=False)
        print(f"Saved concept_relationship_generated worksheet with {len(relationship_df)} rows")
        
        # Copy subheader and formatting from concept_relationship_manual
        try:
            concept_relationship_manual_worksheet = spreadsheet.worksheet('concept_relationship_manual')
            copy_subheader_and_formatting(concept_relationship_manual_worksheet, relationship_worksheet, relationship_df)
        except Exception as e:
            print(f"Could not copy subheader and formatting from concept_relationship_manual: {e}")
            
    except Exception as e:
        print(f"concept_relationship_generated worksheet not found or error occurred: {e}")

def save_tracking_info(concept_dict: Dict[int, Dict], gc: gspread.Client) -> None:
    """
    Save tracking information to a file for use in validate.py.
    
    Args:
        concept_dict: The concept dictionary with tracking info
        gc: Authenticated Google Sheets client
    """
    # Try to get actual gids for generated worksheets
    concept_generated_gid = 'TBD'
    concept_relationship_generated_gid = 'TBD'
    
    try:
        spreadsheet = gc.open(spreadsheet_config['spreadsheet_name'])
        
        # Try to get concept_generated gid
        try:
            concept_worksheet = spreadsheet.worksheet('concept_generated')
            concept_generated_gid = concept_worksheet.id
        except:
            pass
            
        # Try to get concept_relationship_generated gid  
        try:
            relationship_worksheet = spreadsheet.worksheet('concept_relationship_generated')
            concept_relationship_generated_gid = relationship_worksheet.id
        except:
            pass
    except:
        pass
    
    # URL lookup at the top
    url_lookup = {}
    for sheet_name, sheet_info in spreadsheet_config['worksheets'].items():
        if sheet_name == 'concept_generated':
            url_lookup[sheet_name] = f'{spreadsheet_config["base_url"]}?gid={concept_generated_gid}#gid={concept_generated_gid}'
        elif sheet_name == 'concept_relationship_generated':
            url_lookup[sheet_name] = f'{spreadsheet_config["base_url"]}?gid={concept_relationship_generated_gid}#gid={concept_relationship_generated_gid}'
        else:
            url_lookup[sheet_name] = sheet_info['url']
    
    tracking_data = {
        'url_lookup': url_lookup,
        'concepts': {}
    }
    
    for concept_id, data in concept_dict.items():
        tracking_data['concepts'][str(concept_id)] = {
            'source_tags': data['source_tags'],
            'tracking': {}
        }
        
        # Convert SourceTracking objects to serializable format
        for key, tracking in data['tracking'].items():
            tracking_data['concepts'][str(concept_id)]['tracking'][key] = {
                'source_type': tracking.source_type,
                'source_cell': tracking.source_cell,
                'source_url': tracking.source_url
            }
    
    with open('output/tracking_info.json', 'w') as f:
        json.dump(tracking_data, f, indent=2)
    
    print(f"Saved tracking information for {len(tracking_data['concepts'])} concepts")

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
        save_outputs(concept_dict, concept_ids_by_source, gc)
        
        # 5. Save tracking information
        print("\nStep 5: Saving tracking information...")
        save_tracking_info(concept_dict, gc)
        
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