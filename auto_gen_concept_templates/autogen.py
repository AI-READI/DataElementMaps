#!/usr/bin/env python3
"""
Automatic Generation of OMOP Concept Templates

This script processes medical/cognitive assessment data from MOCA and RedCap sources
to generate concept templates for submission to the OMOP Vocabulary committee.

The script:
1. Reads mapping data from Google Sheets containing new concepts to be added to OMOP
2. Merges with existing concept relationships from a manual mapping sheet
3. Generates two output files per source:
   - concept.csv: New concept definitions
   - concept_relationship.csv: Relationships between concepts

Author: [Your name]
Date: 2025
"""

import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import pandas as pd
from typing import Dict, List, Any, Optional
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration for source data spreadsheets
# Each source contains new concepts that need to be added to OMOP vocabulary
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

# Existing manual concept relationships mapping
# Contains concept_id_2 values that map new concepts to existing OMOP concepts
concept_rel_man_old = {
        'spreadsheet_name': 'template_4_adding_vocabulary-2',
        'worksheet_name': 'concept_relationship_manual',
        'location': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125',
}

# Output file specifications
# Defines the structure and column mappings for each output CSV file
outputs = [
    {
        'name': 'concept.csv',  # Changed from concept_manual.csv
        'columns': {
            # Column mappings: 'both' means use the same source column for both MOCA and RedCap
            'concept_name':     {'both': 'TARGET_CONCEPT_NAME'},
            'SRC_CODE':         {'both': 'SRC_CODE'},
            'concept_id':       {'both': 'TARGET_CONCEPT_ID'},
            'vocabulary_id':    {'both': 'TARGET_VOCABULARY_ID'},
            'domain_id':        {'both': 'TARGET_DOMAIN_ID'},
            'v6_domain_id':     {'default': 'survey_conduct'},
            'concept_class_id': {'both': 'TARGET_CONCEPT_CLASS_ID'},
            'standard_concept': {'both': 'TARGET_STANDARD_CONCEPT'},
            'valid_start_date': {'default': '1/1/1970'},
            'valid_end_date':   {'default': ''},
            'invalid_reason':   {'default': ''},
        }
    },
    {
        'name': 'concept_relationship.csv',  # Changed from concept_relationship_manual.csv
        'columns': {
            'concept_name': {'both': 'TARGET_CONCEPT_NAME'},
            'concept_id_1': {'both': 'TARGET_CONCEPT_ID'},
            'SRC_CODE': {'both': 'SRC_CODE'},
            'vocabulary_id_1': {'both': 'TARGET_VOCABULARY_ID'},
            'relationship_id': {'default': ''},
            # concept_id_2 uses lookup from existing manual mappings or defaults
            # MOCA: defaults to 606671 (Montreal Cognitive Assessment v8.1)
            # RedCap: no default, left blank
            'concept_id_2': {'defaultMOCA': '606671'},
            # The following columns will be filled in a future step
            'temp name': {'default': ''},
            'temp domain': {'default': ''},
            'vocabulary_id_2': {'default': ''},
            'temp class': {'default': ''},
            'concept_code_2': {'default': ''},
            'temp standard': {'default': ''},
            'relationship_valid_start_date': {'default': ''},
            'relationship_valid_end_date': {'default': ''},
            'invalid_reason': {'default': ''},
            'confidence': {'default': ''},
            'predicate_id': {'default': ''},
            'mapping_source': {'default': ''},
            'mapping_justification': {'default': ''},
            'mapping_tool': {'default': ''},
            'Notes': {'default': ''},
        }
    },
]

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean a dataframe by removing subtitle rows and blank rows.
    Dynamically detects data boundaries instead of using hardcoded indices.
    
    Args:
        df: Raw dataframe from Google Sheets
        
    Returns:
        Cleaned dataframe with only valid data rows
    """
    # Skip first row if it contains subtitles (check if concept_id_1 is not numeric)
    start_idx = 0
    if pd.isna(pd.to_numeric(df.iloc[0]['concept_id_1'], errors='coerce')):
        start_idx = 1
    
    # Find last row with data (concept_id_1 not empty)
    end_idx = len(df)
    for idx in range(len(df) - 1, -1, -1):
        if pd.notna(df.iloc[idx]['concept_id_1']) and str(df.iloc[idx]['concept_id_1']).strip() != '':
            end_idx = idx + 1
            break
    
    return df.iloc[start_idx:end_idx].fillna('')


def load_concept_mappings(gc: gspread.Client) -> pd.DataFrame:
    """
    Load existing concept mappings from the manual concept relationship sheet.
    
    Args:
        gc: Authenticated Google Sheets client
        
    Returns:
        DataFrame with all concept relationship data
    """
    crm_old_spreadsheet = gc.open(concept_rel_man_old['spreadsheet_name'])
    crm_old_worksheet = crm_old_spreadsheet.worksheet(concept_rel_man_old['worksheet_name'])
    crm_df = get_as_dataframe(crm_old_worksheet)
    
    # Clean the dataframe
    crm_df = clean_dataframe(crm_df)
    
    # Return the full dataframe for later use
    return crm_df


def get_omop_concepts(concept_ids: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Query OMOP concept table for given concept_id_2 values.
    
    Args:
        concept_ids: List of concept IDs to look up
        
    Returns:
        Dictionary mapping concept_id to concept data
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
        
        # Convert to dictionary
        concept_data = {}
        for row in results:
            concept_data[str(row[0])] = {
                'concept_name': row[1],
                'domain_id': row[2],
                'vocabulary_id': row[3],
                'concept_class_id': row[4],
                'concept_code': row[5],
                'standard_concept': row[6]
            }
        
        cursor.close()
        conn.close()
        
        return concept_data
        
    except Exception as e:
        print(f"Error connecting to OMOP database: {e}")
        return {}


def process_source_data(gc: gspread.Client, source: Dict[str, Any], crm_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Process data from a single source (MOCA or RedCap).
    
    Args:
        gc: Authenticated Google Sheets client
        source: Source configuration dictionary
        crm_df: DataFrame with existing concept relationships
        
    Returns:
        Dictionary of output dataframes keyed by filename
    """
    tag = source['tag']
    result_dfs = {}
    
    # Load source data
    spreadsheet = gc.open(source['spreadsheet_name'])
    mapping = spreadsheet.worksheet(source['worksheet_name'])
    df_all = get_as_dataframe(mapping)
    
    # Convert TARGET_CONCEPT_ID to numeric
    df_all['TARGET_CONCEPT_ID'] = pd.to_numeric(df_all['TARGET_CONCEPT_ID'], errors='coerce').fillna(0).astype(int)
    
    # Filter for new concepts (ID > 2000000000) or those needing extensions
    if 'Extension_Needed' in df_all.columns:
        df = df_all[(df_all['TARGET_CONCEPT_ID'] > 2000000000) |
                    (df_all['Extension_Needed'] == 'Yes') |
                    (df_all['TARGET_VOCABULARY_ID'] == 'AIREADI-Vision')]
    else:
        df = df_all[df_all['TARGET_CONCEPT_ID'] > 2000000000]
    
    # Process each output file specification
    for output_spec in outputs:
        result_df = process_output_file(df, output_spec, tag, crm_df)
        result_df['source'] = tag
        result_dfs[output_spec['name']] = result_df
    
    return result_dfs


def process_output_file(df: pd.DataFrame, output_spec: Dict[str, Any], tag: str, crm_df: pd.DataFrame) -> pd.DataFrame:
    """
    Process a single output file specification for a given source.
    
    Args:
        df: Source dataframe
        output_spec: Output file specification
        tag: Source tag (MOCA or RedCap)
        crm_df: DataFrame with existing concept relationships
        
    Returns:
        Processed dataframe ready for output
    """
    columns = output_spec['columns']
    result_data = {}
    
    # Create mapping dictionary from crm_df
    cid2_mapping = {str(row['concept_id_1']): str(row['concept_id_2']) for _, row in crm_df.iterrows()}
    
    # For concept_relationship.csv, we need to handle additional columns
    if output_spec['name'] == 'concept_relationship.csv':
        # Create a mapping from concept_id_1 to the additional columns we need
        crm_mapping = {str(row['concept_id_1']): row for _, row in crm_df.iterrows()}
    
    for col_name, source_def in columns.items():
        # Special handling for concept_id_2 in concept_relationship.csv
        if col_name == 'concept_id_2' and output_spec['name'] == 'concept_relationship.csv':
            if tag == 'MOCA':
                # For MOCA: use mapping or default to 606671
                result_data['concept_id_2'] = df['TARGET_CONCEPT_ID'].apply(
                    lambda x: cid2_mapping.get(str(x), source_def.get('defaultMOCA', ''))
                )
            else:
                # For RedCap: use mapping or leave blank
                result_data['concept_id_2'] = df['TARGET_CONCEPT_ID'].apply(
                    lambda x: cid2_mapping.get(str(x), '')
                )
        elif tag in source_def or 'both' in source_def:
            # Use the source column from the dataframe
            source_col = source_def.get(tag, source_def.get('both'))
            if source_col in df.columns:
                result_data[col_name] = df[source_col].values
            else:
                print(f"Warning: Column '{source_col}' not found in {tag} data")
                result_data[col_name] = [source_def.get('default', '')] * len(df)
        else:
            # Use default value
            default_value = source_def.get(f'default{tag}', source_def.get('default', ''))
            result_data[col_name] = [default_value] * len(df)
    
    # Create and format the result dataframe
    result_df = pd.DataFrame(result_data)
    
    # Ensure integer types for concept IDs
    if 'concept_id' in result_df.columns:
        result_df['concept_id'] = result_df['concept_id'].astype(int)
    if 'concept_id_1' in result_df.columns:
        result_df['concept_id_1'] = result_df['concept_id_1'].astype(int)
    
    # For concept_relationship.csv, fill additional columns from OMOP database and crm_df
    if output_spec['name'] == 'concept_relationship.csv':
        # Get unique concept_id_2 values to query
        unique_concept_ids = result_df['concept_id_2'].unique().tolist()
        
        # Query OMOP database for concept details
        omop_concepts = get_omop_concepts(unique_concept_ids)
        
        # Fill columns from OMOP database
        result_df['temp name'] = result_df['concept_id_2'].apply(
            lambda x: omop_concepts.get(str(x), {}).get('concept_name', '')
        )
        result_df['temp domain'] = result_df['concept_id_2'].apply(
            lambda x: omop_concepts.get(str(x), {}).get('domain_id', '')
        )
        result_df['vocabulary_id_2'] = result_df['concept_id_2'].apply(
            lambda x: omop_concepts.get(str(x), {}).get('vocabulary_id', '')
        )
        result_df['temp class'] = result_df['concept_id_2'].apply(
            lambda x: omop_concepts.get(str(x), {}).get('concept_class_id', '')
        )
        result_df['concept_code_2'] = result_df['concept_id_2'].apply(
            lambda x: omop_concepts.get(str(x), {}).get('concept_code', '')
        )
        result_df['temp standard'] = result_df['concept_id_2'].apply(
            lambda x: omop_concepts.get(str(x), {}).get('standard_concept', '')
        )
        
        # Fill columns from crm_df
        for col in ['confidence', 'predicate_id', 'mapping_source', 'mapping_justification', 'mapping_tool']:
            if col in crm_df.columns:
                result_df[col] = result_df['concept_id_1'].apply(
                    lambda x: crm_mapping.get(str(x), {}).get(col, '') if str(x) in crm_mapping else ''
                )
    
    return result_df


def save_outputs(output_dfs: Dict[str, Dict[str, pd.DataFrame]]) -> None:
    """
    Save all output dataframes to CSV files.
    Creates both individual source files and combined files.
    
    Args:
        output_dfs: Nested dictionary of dataframes by source and filename
    """
    combined_dfs = {}
    
    # Save individual source files and collect for combined output
    for tag, dfs in output_dfs.items():
        for fname, df in dfs.items():
            # Save individual source file
            filename = f'output/{tag}_{fname}'
            df.to_csv(filename, index=False)
            print(f"Saved {filename} with {len(df)} rows")
            
            # Collect for combined file
            if fname not in combined_dfs:
                combined_dfs[fname] = []
            combined_dfs[fname].append(df)
    
    # Save combined files
    for fname, dfs in combined_dfs.items():
        df = pd.concat(dfs, ignore_index=True)
        filename = f'output/{fname}'
        df.to_csv(filename, index=False)
        print(f"Saved {filename} with {len(df)} rows")


def main() -> None:
    """
    Main function to orchestrate the concept template generation process.
    """
    try:
        # Initialize Google Sheets client
        gc = gspread.service_account()
        
        # Load existing concept mappings
        print("Loading existing concept mappings...")
        crm_df = load_concept_mappings(gc)
        print(f"Loaded {len(crm_df)} concept mappings")
        
        # Process each source
        output_dfs = {}
        for source in mapping_sources:
            if not source['process']:
                continue
            
            print(f"\nProcessing {source['tag']} data...")
            output_dfs[source['tag']] = process_source_data(gc, source, crm_df)
        
        # Save all outputs
        print("\nSaving output files...")
        save_outputs(output_dfs)
        
        print("\nProcessing complete!")
        
    except Exception as e:
        print(f"Error during processing: {e}")
        raise


if __name__ == "__main__":
    main()