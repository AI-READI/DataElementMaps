#!/usr/bin/env python3
"""
Validation Script for OMOP Concept Templates

This script compares the generated CSV files against the manually created worksheets
to validate the accuracy of the autogen.py output.

The script:
1. Loads data from Google Sheets (manual worksheets) and CSV files (generated)
2. Matches rows by concept_id/concept_id_1
3. Compares all columns with tolerance for whitespace, case, and null differences
4. Generates both summary and detailed reports in markdown format

Author: [Your name]
Date: 2025
"""

import gspread
from gspread_dataframe import get_as_dataframe
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
import os
import json
from datetime import datetime

# Import configuration from autogen.py
try:
    from autogen import spreadsheet_config
except ImportError:
    # Fallback configuration if import fails
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
            }
        }
    }

# Configuration for validation targets - using imported spreadsheet config
validation_targets = [
    {
        'name': 'concept',
        'spreadsheet_name': spreadsheet_config['spreadsheet_name'],
        'manual_worksheet_name': 'concept_manual',
        'generated_worksheet_name': 'concept_generated',
        'id_column': 'concept_id',
        'manual_worksheet_url': spreadsheet_config['worksheets']['concept_manual']['url'],
    },
    {
        'name': 'concept_relationship', 
        'spreadsheet_name': spreadsheet_config['spreadsheet_name'],
        'manual_worksheet_name': 'concept_relationship_manual',
        'generated_worksheet_name': 'concept_relationship_generated',
        'id_column': 'concept_id_1',
        'manual_worksheet_url': spreadsheet_config['worksheets']['concept_relationship_manual']['url'],
    }
]


def normalize_value(value: Any) -> str:
    """
    Normalize a value for comparison by handling whitespace, case, and null differences.
    Also handles int/float conversion issues from gspread_dataframe.
    
    Args:
        value: The value to normalize
        
    Returns:
        Normalized string value
    """
    if pd.isna(value) or value is None:
        return ""
    
    # Convert to string and normalize
    str_value = str(value).strip().lower()
    
    # Handle common null representations
    if str_value in ['nan', 'none', 'null', '']:
        return ""
    
    # Handle int/float conversion issues (e.g., "123.0" -> "123")
    if '.' in str_value and str_value.replace('.', '').replace('-', '').isdigit():
        try:
            float_val = float(str_value)
            if float_val.is_integer():
                str_value = str(int(float_val))
        except ValueError:
            pass
    
    return str_value


def analyze_difference_type(manual_val: str, generated_val: str, manual_normalized: str, generated_normalized: str) -> dict:
    """
    Analyze the type of difference between two values to provide explanations.
    
    Args:
        manual_val: Original manual value
        generated_val: Original generated value
        manual_normalized: Normalized manual value
        generated_normalized: Normalized generated value
        
    Returns:
        Dictionary with difference analysis
    """
    analysis = {
        'type': 'content',  # default
        'explanation': '',
        'severity': 'medium',  # low, medium, high
        'should_ignore': False
    }
    
    # Check if it's only whitespace differences (including internal whitespace)
    manual_no_spaces = ''.join(manual_val.split()) if manual_val else ''
    generated_no_spaces = ''.join(generated_val.split()) if generated_val else ''
    
    if manual_no_spaces == generated_no_spaces and manual_no_spaces != '':
        analysis['type'] = 'whitespace'
        analysis['explanation'] = 'Only whitespace differences (spaces, tabs, or line breaks)'
        analysis['severity'] = 'low'
        analysis['should_ignore'] = False  # Don't ignore, but categorize as whitespace
        return analysis
    
    # Check if it's only case differences
    if manual_val.lower() == generated_val.lower() and manual_val != '' and generated_val != '':
        analysis['type'] = 'case'
        analysis['explanation'] = 'Only case differences (upper/lower case)'
        analysis['severity'] = 'low'
        return analysis
    
    # Check if one is blank
    if manual_normalized == '' and generated_normalized != '':
        analysis['type'] = 'missing_manual'
        analysis['explanation'] = 'Value missing in manual sheet'
        analysis['severity'] = 'medium'
        return analysis
    elif generated_normalized == '' and manual_normalized != '':
        analysis['type'] = 'missing_generated'
        analysis['explanation'] = 'Value missing in generated file'
        analysis['severity'] = 'medium'
        return analysis
    
    # Check if it's a minor formatting difference (like "123.0" vs "123")
    if manual_normalized != generated_normalized:
        try:
            manual_float = float(manual_val) if manual_val else None
            generated_float = float(generated_val) if generated_val else None
            if manual_float == generated_float:
                analysis['type'] = 'formatting'
                analysis['explanation'] = 'Number formatting difference (e.g., "123.0" vs "123")'
                analysis['severity'] = 'low'
                return analysis
        except (ValueError, TypeError):
            pass
    
    # Default to content difference
    analysis['type'] = 'content'
    analysis['explanation'] = 'Content difference requiring review'
    analysis['severity'] = 'high'
    return analysis


def load_worksheet_data(gc: gspread.Client, spreadsheet_name: str, worksheet_name: str) -> Tuple[pd.DataFrame, int]:
    """
    Load data from a Google Sheets worksheet.
    
    Args:
        gc: Authenticated Google Sheets client
        spreadsheet_name: Name of the spreadsheet
        worksheet_name: Name of the worksheet
        
    Returns:
        Tuple of (DataFrame with worksheet data, number of rows skipped from top)
    """
    try:
        spreadsheet = gc.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        df = get_as_dataframe(worksheet)
        
        # Clean the dataframe similar to autogen.py
        # Dynamically detect where data starts, similar to clean_dataframe in autogen.py
        start_idx = 0
        id_column = 'concept_id_1' if 'concept_id_1' in df.columns else 'concept_id'
        if pd.isna(pd.to_numeric(df.iloc[0][id_column], errors='coerce')):
            start_idx = 1
        end_idx = len(df)
        
        # Find the last row with meaningful data (using the same logic as autogen.py)
        for idx in range(len(df) - 1, -1, -1):
            if pd.notna(df.iloc[idx][id_column]) and str(df.iloc[idx][id_column]).strip() != '':
                end_idx = idx + 1
                break
        
        df = df.iloc[start_idx:end_idx].fillna('')
        
        # Reset index so that idx starts from 0 for the first data row
        df = df.reset_index(drop=True)
        
        # Ensure concept IDs are integers to fix float/int issues
        if id_column in df.columns:
            df[id_column] = pd.to_numeric(df[id_column], errors='coerce').fillna(0).astype(int)
        if 'concept_id_2' in df.columns:
            df['concept_id_2'] = pd.to_numeric(df['concept_id_2'], errors='coerce').fillna(0).astype('Int64')  # nullable integer
        
        return df, start_idx
        
    except Exception as e:
        print(f"Error loading worksheet {worksheet_name}: {e}")
        return pd.DataFrame(), 0


def load_generated_worksheet_data(gc: gspread.Client, spreadsheet_name: str, worksheet_name: str) -> Tuple[pd.DataFrame, int]:
    """
    Load data from a generated Google Sheets worksheet.
    
    Args:
        gc: Authenticated Google Sheets client
        spreadsheet_name: Name of the spreadsheet
        worksheet_name: Name of the worksheet
        
    Returns:
        Tuple of (DataFrame with worksheet data, number of rows skipped from top)
    """
    try:
        spreadsheet = gc.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        df = get_as_dataframe(worksheet)
        
        # Clean the dataframe similar to manual worksheets  
        # Dynamically detect where data starts
        start_idx = 0
        id_column = 'concept_id_1' if 'concept_id_1' in df.columns else 'concept_id'
        if pd.isna(pd.to_numeric(df.iloc[0][id_column], errors='coerce')):
            start_idx = 1
        end_idx = len(df)
        
        # Find the last row with meaningful data
        for idx in range(len(df) - 1, -1, -1):
            if pd.notna(df.iloc[idx][id_column]) and str(df.iloc[idx][id_column]).strip() != '':
                end_idx = idx + 1
                break
        
        df = df.iloc[start_idx:end_idx].fillna('')
        
        # Reset index so that idx starts from 0 for the first data row
        df = df.reset_index(drop=True)
        
        # Ensure concept IDs are integers to fix float/int issues
        if id_column in df.columns:
            df[id_column] = pd.to_numeric(df[id_column], errors='coerce').fillna(0).astype(int)
        if 'concept_id_2' in df.columns:
            df['concept_id_2'] = pd.to_numeric(df['concept_id_2'], errors='coerce').fillna(0).astype('Int64')  # nullable integer
        
        return df, start_idx
        
    except Exception as e:
        print(f"Error loading generated worksheet {worksheet_name}: {e}")
        return pd.DataFrame(), 0


def load_tracking_info() -> Dict[str, Any]:
    """
    Load tracking information from the JSON file created by autogen.py.
    
    Returns:
        Dictionary with URL lookup and tracking data
    """
    try:
        with open('output/tracking_info.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Could not load tracking info: {e}")
        return {'url_lookup': {}, 'concepts': {}}


def compare_dataframes(df_manual: pd.DataFrame, df_generated: pd.DataFrame, 
                      id_column: str, name: str, target_info: Dict[str, Any] = None, 
                      manual_rows_skipped: int = 0) -> Dict[str, Any]:
    """
    Compare two dataframes and generate detailed comparison results.
    
    Args:
        df_manual: Manual worksheet data
        df_generated: Generated CSV data
        id_column: Column name to use for matching rows
        name: Name of the comparison (for reporting)
        
    Returns:
        Dictionary with comparison results
    """
    results = {
        'name': name,
        'manual_rows': len(df_manual),
        'generated_rows': len(df_generated),
        'matched_rows': 0,
        'unmatched_manual': [],
        'unmatched_generated': [],
        'column_differences': {},
        'errors': [],  # For critical ID differences
        'discrepancies': [],  # For other differences
        'manual_df': df_manual,  # Store for link generation
        'generated_df': df_generated,  # Store for link generation
        'target_info': target_info,  # Store target info for URL generation
        'manual_rows_skipped': manual_rows_skipped  # Store for row number calculation
    }
    
    if df_manual.empty or df_generated.empty:
        results['error'] = f"One or both dataframes are empty (manual: {len(df_manual)}, generated: {len(df_generated)})"
        return results
    
    # Ensure ID columns are integers first, then convert to string for consistent matching
    df_manual[id_column] = pd.to_numeric(df_manual[id_column], errors='coerce').fillna(0).astype(int).astype(str)
    df_generated[id_column] = pd.to_numeric(df_generated[id_column], errors='coerce').fillna(0).astype(int).astype(str)
    
    # Create dictionaries for easy lookup
    manual_dict = {str(row[id_column]): row for _, row in df_manual.iterrows()}
    generated_dict = {str(row[id_column]): row for _, row in df_generated.iterrows()}
    
    # Find common columns (excluding columns to ignore)
    ignored_columns = {'source', 'SRC_CODE', 'Notes'}
    manual_columns = set(df_manual.columns) - ignored_columns
    generated_columns = set(df_generated.columns) - ignored_columns
    common_columns = list(manual_columns.intersection(generated_columns))
    
    # Track column differences
    results['manual_only_columns'] = list(manual_columns - generated_columns)
    results['generated_only_columns'] = list(generated_columns - manual_columns)
    
    # Find matching and non-matching rows
    manual_ids = set(manual_dict.keys())
    generated_ids = set(generated_dict.keys())
    
    common_ids = manual_ids.intersection(generated_ids)
    results['matched_rows'] = len(common_ids)
    
    # Store unmatched with additional info for better reporting
    results['unmatched_manual'] = []
    for row_id in manual_ids - generated_ids:
        row = manual_dict[row_id]
        concept_name = row.get('concept_name', '')
        # Find the actual row number in the dataframe
        row_num = None
        for idx, df_row in df_manual.iterrows():
            if str(df_row[id_column]) == str(row_id):
                # With aligned DataFrames, row numbers match directly
                # Google Sheets: Row 1=Header, Row 2=Subheader, Row 3+=Data
                # After reset_index(), idx 0 = first data row in Google Sheets
                # start_idx tells us how many rows we skipped, so actual row = idx + start_idx + 3
                # But if user says it should be 167 not 168, we need idx + start_idx + 2
                row_num = idx + 2 + manual_rows_skipped
                break
        results['unmatched_manual'].append({
            'id': row_id,
            'concept_name': concept_name,
            'source': 'manual',
            'row_num': row_num
        })
    
    results['unmatched_generated'] = []
    for row_id in generated_ids - manual_ids:
        row = generated_dict[row_id]
        concept_name = row.get('concept_name', '')
        # Find the actual row number in the dataframe
        row_num = None
        for idx, df_row in df_generated.iterrows():
            if str(df_row[id_column]) == str(row_id):
                # With aligned DataFrames, use same calculation as manual
                # Since DataFrames are aligned, they have same row structure  
                row_num = idx + 2 + manual_rows_skipped
                break
        results['unmatched_generated'].append({
            'id': row_id,
            'concept_name': concept_name,
            'source': 'generated',
            'row_num': row_num
        })
    
    # Define critical ID columns that should be treated as errors
    critical_id_columns = {'concept_id', 'concept_id_1', 'concept_id_2'}
    
    # Compare matching rows
    for row_id in common_ids:
        manual_row = manual_dict[row_id]
        generated_row = generated_dict[row_id]
        
        error_diffs = {}  # For critical ID differences
        discrepancy_diffs = {}  # For other differences
        
        for col in common_columns:
            manual_val = normalize_value(manual_row.get(col, ''))
            generated_val = normalize_value(generated_row.get(col, ''))
            
            if manual_val != generated_val:
                manual_original = str(manual_row.get(col, ''))
                generated_original = str(generated_row.get(col, ''))
                
                # Analyze the type of difference
                diff_analysis = analyze_difference_type(manual_original, generated_original, manual_val, generated_val)
                
                # Skip whitespace-only differences if configured to ignore them
                if diff_analysis['should_ignore']:
                    continue
                
                diff_info = {
                    'manual': manual_original,
                    'generated': generated_original,
                    'manual_normalized': manual_val,
                    'generated_normalized': generated_val,
                    'analysis': diff_analysis
                }
                
                if col in critical_id_columns:
                    error_diffs[col] = diff_info
                else:
                    discrepancy_diffs[col] = diff_info
        
        # Add to appropriate category
        if error_diffs:
            results['errors'].append({
                'id': row_id,
                'differences': error_diffs
            })
        
        if discrepancy_diffs:
            # Add concept_name for better reporting
            concept_name_manual = manual_row.get('concept_name', '')
            concept_name_generated = generated_row.get('concept_name', '')
            
            results['discrepancies'].append({
                'id': row_id,
                'concept_name_manual': concept_name_manual,
                'concept_name_generated': concept_name_generated,
                'differences': discrepancy_diffs
            })
    
    # Calculate column-level statistics
    for col in common_columns:
        matching = 0
        total = len(common_ids)
        
        for row_id in common_ids:
            manual_val = normalize_value(manual_dict[row_id].get(col, ''))
            generated_val = normalize_value(generated_dict[row_id].get(col, ''))
            
            if manual_val == generated_val:
                matching += 1
        
        results['column_differences'][col] = {
            'matching': matching,
            'total': total,
            'match_rate': matching / total if total > 0 else 0
        }
    
    return results


def generate_markdown_report(all_results: List[Dict[str, Any]]) -> str:
    """
    Generate a markdown report from comparison results.
    
    Args:
        all_results: List of comparison results for each target
        
    Returns:
        Markdown formatted report string
    """
    report = f"""# Validation Report

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Data Sources

This report compares generated Google Sheets against manual Google Sheets:

- **Manual Sheets**: [{spreadsheet_config['spreadsheet_name']}]({spreadsheet_config['base_url']})
  - concept_manual worksheet
  - concept_relationship_manual worksheet
- **Generated Sheets**: [{spreadsheet_config['spreadsheet_name']}]({spreadsheet_config['base_url']})
  - concept_generated worksheet (from autogen.py)
  - concept_relationship_generated worksheet (from autogen.py)

## Summary

"""
    
    # Summary table
    report += "| Target | Manual Rows | Generated Rows | Matched Rows | Errors | Discrepancies |\n"
    report += "|--------|-------------|----------------|--------------|--------|---------------|\n"
    
    for result in all_results:
        if 'error' in result:
            report += f"| {result['name']} | ERROR | ERROR | ERROR | ERROR | {result['error']} |\n"
        else:
            error_count = len(result.get('errors', []))
            discrepancy_count = len(result.get('discrepancies', []))
            report += f"| {result['name']} | {result['manual_rows']} | {result['generated_rows']} | {result['matched_rows']} | {error_count} | {discrepancy_count} |\n"
    
    # Detailed results for each target
    for result in all_results:
        if 'error' in result:
            report += f"\n## {result['name'].title()} Validation\n\n**ERROR:** {result['error']}\n"
            continue
            
        report += f"\n## {result['name'].title()} Validation\n\n"
        
        # Row matching summary
        report += f"- **Manual rows:** {result['manual_rows']}\n"
        report += f"- **Generated rows:** {result['generated_rows']}\n"
        report += f"- **Matched rows:** {result['matched_rows']}\n"
        report += f"- **Unmatched manual rows:** {len(result['unmatched_manual'])}\n"
        report += f"- **Unmatched generated rows:** {len(result['unmatched_generated'])}\n\n"
        
        # Note: standard_concept differences are now included in blank counts
        
        # Move column match rates to discrepancies section
        
        # Unmatched concepts details with proper worksheet URLs
        if result['unmatched_manual']:
            report += f"### Unmatched Manual Concepts ({len(result['unmatched_manual'])})\n\n"
            report += "| Concept ID | Concept Name |\n"
            report += "|------------|--------------|\n"
            
            # Sort unmatched manual concepts alphabetically by concept name
            sorted_unmatched_manual = sorted(result['unmatched_manual'], key=lambda x: x['concept_name'])
            
            for row_info in sorted_unmatched_manual:
                concept_id = row_info['id']
                concept_name = row_info['concept_name']
                
                # Create proper Google Sheets URL with range
                if result.get('target_info') and result['target_info'].get('manual_worksheet_url') and row_info.get('row_num'):
                    base_url = result['target_info']['manual_worksheet_url']
                    row_num = row_info['row_num']
                    url_with_range = f"{base_url}&range=A{row_num}"
                    concept_id_link = f"[{concept_id}]({url_with_range})"
                else:
                    concept_id_link = concept_id
                    
                report += f"| {concept_id_link} | {concept_name} |\n"
            report += "\n"
        
        if result['unmatched_generated']:
            report += f"### Unmatched Generated Concepts ({len(result['unmatched_generated'])})\n\n"
            report += "| Concept ID | Concept Name |\n"
            report += "|------------|--------------|\n"
            
            # Sort unmatched generated concepts alphabetically by concept name
            sorted_unmatched_generated = sorted(result['unmatched_generated'], key=lambda x: x['concept_name'])
            
            for row_info in sorted_unmatched_generated:
                concept_id = row_info['id']
                concept_name = row_info['concept_name']
                
                # Create link to generated sheet using tracking info
                concept_id_link = concept_id
                if result.get('target_info') and result['target_info'].get('tracking_info') and row_info.get('row_num'):
                    tracking_info = result['target_info']['tracking_info']
                    url_lookup = tracking_info.get('url_lookup', {})
                    generated_sheet_name = result['target_info']['generated_worksheet_name']
                    
                    if generated_sheet_name in url_lookup:
                        base_url = url_lookup[generated_sheet_name]
                        row_num = row_info['row_num']
                        url_with_range = f"{base_url}&range=A{row_num}"
                        concept_id_link = f"[{concept_id}]({url_with_range})"
                
                report += f"| {concept_id_link} | {concept_name} |\n"
            report += "\n"
        
        # Errors section (critical ID differences)
        if result.get('errors'):
            report += f"### Errors ({len(result['errors'])} rows with critical ID differences)\n\n"
            report += "⚠️ **These are critical errors that need immediate attention!**\n\n"
            
            for row_diff in result['errors']:
                report += f"#### Row ID: {row_diff['id']}\n\n"
                report += "| Column | Manual | Generated |\n"
                report += "|--------|--------|----------|\n"
                
                for col, diff in row_diff['differences'].items():
                    manual_val = diff['manual']
                    generated_val = diff['generated']
                    report += f"| {col} | {manual_val} | {generated_val} |\n"
                report += "\n"
        
        # Discrepancies section (other differences) - single table format
        if result.get('discrepancies'):
            report += f"### Discrepancies ({len(result['discrepancies'])} rows with other differences)\n\n"

            # Add column match rates here
            if result['column_differences']:
                report += "#### Column Match Rates\n\n"
                report += "| Column | Matching | Total | Match Rate |\n"
                report += "|--------|----------|-------|------------|\n"
                
                # Sort columns by match rate (ascending, so worst matches appear first)
                sorted_columns = sorted(result['column_differences'].items(), key=lambda x: x[1]['match_rate'])
                
                for col, stats in sorted_columns:
                    match_rate = stats['match_rate'] * 100
                    report += f"| {col} | {stats['matching']} | {stats['total']} | {match_rate:.1f}% |\n"
                report += "\n"
            
            # Group discrepancies by type
            report += "#### Discrepancy Summary\n\n"
            report += "- 🔴 Manual values link to specific cells in manual Google Sheets\n"
            report += "- 🔵 Generated values link to specific cells in generated Google Sheets\n"
            report += "- Explanations in parentheses describe the type of difference\n\n"

            # Categorize all discrepancies
            whitespace_case_diffs = []
            blank_diffs = []
            substantive_diffs = []
            column_blank_counts = {}
            
            for row_diff in result['discrepancies']:
                for col, diff in row_diff['differences'].items():
                    # Track blank counts
                    if col not in column_blank_counts:
                        column_blank_counts[col] = {'manual_blanks': 0, 'generated_blanks': 0, 'total': 0}
                    column_blank_counts[col]['total'] += 1
                    
                    diff_type = diff.get('analysis', {}).get('type', 'content')
                    
                    if diff_type in ['whitespace', 'case', 'formatting']:
                        whitespace_case_diffs.append((row_diff, col, diff))
                    elif diff_type in ['missing_manual', 'missing_generated']:
                        blank_diffs.append((row_diff, col, diff))
                        if diff['manual_normalized'] == '':
                            column_blank_counts[col]['manual_blanks'] += 1
                        if diff['generated_normalized'] == '':
                            column_blank_counts[col]['generated_blanks'] += 1
                    else:
                        substantive_diffs.append((row_diff, col, diff))
            
            # Show blank summaries for all columns with blanks
            blank_summary_columns = []
            for col, stats in column_blank_counts.items():
                if stats['manual_blanks'] > 0 or stats['generated_blanks'] > 0:
                    blank_summary_columns.append(col)
                    report += f"**{col}**: {stats['manual_blanks']} manual blanks, {stats['generated_blanks']} generated blanks (out of {stats['total']} total differences)\n\n"
            
            # Show whitespace/case summary
            if whitespace_case_diffs:
                report += f"**Whitespace/Case differences**: {len(whitespace_case_diffs)} instances across {len(set(item[1] for item in whitespace_case_diffs))} columns\n"
                # Show 2-3 examples
                for i, (row_diff, col, diff) in enumerate(whitespace_case_diffs[:3]):
                    concept_name = row_diff['concept_name_manual']
                    concept_id = row_diff['id']
                    manual_val = diff['manual'] if diff['manual'] else 'blank'
                    generated_val = diff['generated'] if diff['generated'] else 'blank'
                    explanation = diff.get('analysis', {}).get('explanation', '')
                    report += f"- {concept_name} ({concept_id}) - {col}: \"{manual_val}\" vs \"{generated_val}\" ({explanation})\n"
                if len(whitespace_case_diffs) > 3:
                    report += f"- ... and {len(whitespace_case_diffs) - 3} more\n"
                report += "\n"
            
            if blank_summary_columns:
                report += "\n"
            
            # Show detailed table only for substantive differences
            detailed_columns = set(item[1] for item in substantive_diffs)
            
            if detailed_columns:
                report += f"#### Substantive Content Differences ({len(substantive_diffs)} instances)\n\n"
                
                # Helper function to get column letter from column name
                def get_column_letter(col_name, df):
                    try:
                        col_index = list(df.columns).index(col_name)
                        # Convert to Excel column letter (A=0, B=1, etc.)
                        if col_index < 26:
                            return chr(ord('A') + col_index)
                        else:
                            return chr(ord('A') + col_index // 26 - 1) + chr(ord('A') + col_index % 26)
                    except ValueError:
                        return 'A'  # fallback
                
                # Group substantive differences by concept
                substantive_by_concept = {}
                for row_diff, col, diff in substantive_diffs:
                    concept_id = row_diff['id']
                    if concept_id not in substantive_by_concept:
                        substantive_by_concept[concept_id] = {
                            'row_diff': row_diff,
                            'differences': []
                        }
                    substantive_by_concept[concept_id]['differences'].append((col, diff))
                
                # Sort concepts by name
                sorted_concepts = sorted(substantive_by_concept.items(), key=lambda x: x[1]['row_diff']['concept_name_manual'])
                
                # Group by concept using nested lists
                for concept_id, concept_data in sorted_concepts:
                    row_diff = concept_data['row_diff']
                    concept_name_manual = row_diff['concept_name_manual']
                    
                    # Get row numbers for linking
                    manual_row_num = None
                    generated_row_num = None
                    
                    if result.get('target_info'):
                        id_column = result['target_info']['id_column']
                        
                        # Find row number in manual dataframe
                        for idx, df_row in result['manual_df'].iterrows():
                            if str(df_row[id_column]) == str(concept_id):
                                # Calculate actual Google Sheets row number 
                                # idx is 0-based in cleaned dataframe
                                # Google Sheets structure: Row 1=Header, Row 2=Subheader, Row 3+=Data
                                # After reset_index(), idx 0 = first data row
                                # Adjusted formula to match expected row numbers
                                manual_row_num = idx + 2 + result['manual_rows_skipped']
                                break
                        
                        # Find row number in generated dataframe  
                        for idx, df_row in result['generated_df'].iterrows():
                            if str(df_row[id_column]) == str(concept_id):
                                # With aligned DataFrames, manual and generated rows should be at same positions
                                generated_row_num = idx + 2 + result['manual_rows_skipped']  # Same calculation as manual
                                break
                    
                    # Show concept header with nested differences
                    concept_details = []
                    
                    # Sort columns within each concept
                    sorted_columns_for_concept = sorted(concept_data['differences'])
                    
                    for col, diff in sorted_columns_for_concept:
                        # Create linked values with proper column references
                        manual_val = diff['manual'] if diff['manual'] else 'blank'
                        generated_val = diff['generated'] if diff['generated'] else 'blank'
                        
                        # Create manual link with correct column
                        manual_val_link = manual_val
                        if result.get('target_info') and result['target_info'].get('manual_worksheet_url') and manual_row_num:
                            col_letter = get_column_letter(col, result['manual_df'])
                            base_url = result['target_info']['manual_worksheet_url']
                            manual_url = f"{base_url}&range={col_letter}{manual_row_num}"
                            manual_val_link = f"[{manual_val}]({manual_url})"
                        
                        # Create generated link with sheet reference
                        generated_val_link = generated_val
                        if generated_row_num and result.get('target_info') and result['target_info'].get('tracking_info'):
                            tracking_info = result['target_info']['tracking_info']
                            url_lookup = tracking_info.get('url_lookup', {})
                            generated_sheet_name = result['target_info']['generated_worksheet_name']
                            
                            if generated_sheet_name in url_lookup:
                                col_letter = get_column_letter(col, result['generated_df'])
                                base_url = url_lookup[generated_sheet_name]
                                generated_url = f"{base_url}&range={col_letter}{generated_row_num}"
                                generated_val_link = f"[{generated_val}]({generated_url})"
                        
                        # Get explanation if available
                        explanation = diff.get('analysis', {}).get('explanation', '')
                        
                        # Add to concept details with explanation
                        detail_line = f"  - {col}: 🔴 {manual_val_link} vs 🔵 {generated_val_link}"
                        if explanation:
                            detail_line += f" ({explanation})"
                        concept_details.append(detail_line)
                    
                    # Show concept with details
                    report += f"- **{concept_name_manual}** ({concept_id})\n"
                    for detail in concept_details:
                        report += f"{detail}\n"
    
    return report


def main():
    """
    Main function to run the validation process.
    """
    try:
        # Initialize Google Sheets client
        gc = gspread.service_account()
        
        all_results = []
        
        print("Starting validation process...")
        
        # Load tracking information
        tracking_info = load_tracking_info()
        
        for target in validation_targets:
            print(f"\nValidating {target['name']}...")
            
            # Load manual worksheet data
            print(f"  Loading manual data from {target['manual_worksheet_name']}...")
            df_manual, manual_rows_skipped = load_worksheet_data(gc, target['spreadsheet_name'], target['manual_worksheet_name'])
            
            # Load generated worksheet data
            print(f"  Loading generated data from {target['generated_worksheet_name']}...")
            df_generated, generated_rows_skipped = load_generated_worksheet_data(gc, target['spreadsheet_name'], target['generated_worksheet_name'])
            
            # Add tracking info to target config
            target_with_tracking = target.copy()
            target_with_tracking['tracking_info'] = tracking_info
            
            # Compare the data
            print("  Comparing data...")
            results = compare_dataframes(df_manual, df_generated, target['id_column'], target['name'], target_with_tracking, manual_rows_skipped)
            results['generated_rows_skipped'] = generated_rows_skipped
            all_results.append(results)
            
            if 'error' not in results:
                error_count = len(results.get('errors', []))
                discrepancy_count = len(results.get('discrepancies', []))
                print(f"  Results: {results['matched_rows']} matched rows, {error_count} errors, {discrepancy_count} discrepancies")
        
        # Generate and save report
        print("\nGenerating validation report...")
        report = generate_markdown_report(all_results)
        
        # Save timestamped report
        timestamped_report_path = f"old_validation_reports/validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(timestamped_report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save generic report (for git tracking)
        generic_report_path = "validation_report.md"
        with open(generic_report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Validation report saved to: {timestamped_report_path}")
        print(f"Generic validation report saved to: {generic_report_path}")
        
        # Also print summary to console
        print("\n" + "="*50)
        print("VALIDATION SUMMARY")
        print("="*50)
        
        for result in all_results:
            if 'error' in result:
                print(f"{result['name']}: ERROR - {result['error']}")
            else:
                error_count = len(result.get('errors', []))
                discrepancy_count = len(result.get('discrepancies', []))
                unmatched_manual = len(result.get('unmatched_manual', []))
                unmatched_generated = len(result.get('unmatched_generated', []))
                match_rate = result['matched_rows'] / max(result['manual_rows'], result['generated_rows']) * 100
                print(f"{result['name']}: {match_rate:.1f}% match rate, {error_count} errors, {discrepancy_count} discrepancies, {unmatched_manual} unmatched manual concepts, {unmatched_generated} unmatched generated concepts")
        
    except Exception as e:
        print(f"Error during validation: {e}")
        raise


if __name__ == "__main__":
    main()