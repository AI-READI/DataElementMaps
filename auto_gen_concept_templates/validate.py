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
from datetime import datetime

# Configuration for validation targets
validation_targets = [
    {
        'name': 'concept',
        'spreadsheet_name': 'template_4_adding_vocabulary-2',
        'worksheet_name': 'concept_manual',
        'csv_path': 'output/concept.csv',
        'id_column': 'concept_id',
        'worksheet_url': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=535320917#gid=535320917',
    },
    {
        'name': 'concept_relationship', 
        'spreadsheet_name': 'template_4_adding_vocabulary-2',
        'worksheet_name': 'concept_relationship_manual',
        'csv_path': 'output/concept_relationship.csv',
        'id_column': 'concept_id_1',
        'worksheet_url': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125',
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


def load_worksheet_data(gc: gspread.Client, spreadsheet_name: str, worksheet_name: str) -> pd.DataFrame:
    """
    Load data from a Google Sheets worksheet.
    
    Args:
        gc: Authenticated Google Sheets client
        spreadsheet_name: Name of the spreadsheet
        worksheet_name: Name of the worksheet
        
    Returns:
        DataFrame with worksheet data
    """
    try:
        spreadsheet = gc.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        df = get_as_dataframe(worksheet)
        
        # Clean the dataframe similar to autogen.py
        # Skip row 2 (index 1) which contains column descriptions
        # Find first and last valid rows, but start from index 2 (row 3)
        start_idx = 2  # Skip header (0) and descriptions (1)
        end_idx = len(df)
        
        # Find the last row with meaningful data
        for idx in range(len(df) - 1, -1, -1):
            if not df.iloc[idx].isna().all():
                end_idx = idx + 1
                break
        
        df = df.iloc[start_idx:end_idx].fillna('')
        return df
        
    except Exception as e:
        print(f"Error loading worksheet {worksheet_name}: {e}")
        return pd.DataFrame()


def load_csv_data(csv_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        DataFrame with CSV data
    """
    try:
        if not os.path.exists(csv_path):
            print(f"CSV file not found: {csv_path}")
            return pd.DataFrame()
        
        df = pd.read_csv(csv_path).fillna('')
        return df
        
    except Exception as e:
        print(f"Error loading CSV {csv_path}: {e}")
        return pd.DataFrame()


def compare_dataframes(df_manual: pd.DataFrame, df_generated: pd.DataFrame, 
                      id_column: str, name: str, target_info: Dict[str, Any] = None) -> Dict[str, Any]:
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
        'target_info': target_info  # Store target info for URL generation
    }
    
    if df_manual.empty or df_generated.empty:
        results['error'] = f"One or both dataframes are empty (manual: {len(df_manual)}, generated: {len(df_generated)})"
        return results
    
    # Convert ID columns to string for consistent matching
    df_manual[id_column] = df_manual[id_column].astype(str)
    df_generated[id_column] = df_generated[id_column].astype(str)
    
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
        # Find the actual row number in the dataframe (add 3 for header, descriptions, + 1-indexed)
        row_num = None
        for idx, df_row in df_manual.iterrows():
            if str(df_row[id_column]) == str(row_id):
                row_num = idx + 3  # +3 for header, descriptions, and 1-indexed
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
        # Find the actual row number in the dataframe (add 2 for header + 1-indexed for CSV)
        row_num = None
        for idx, df_row in df_generated.iterrows():
            if str(df_row[id_column]) == str(row_id):
                row_num = idx + 2  # +2 for header and 1-indexed for CSV
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
                diff_info = {
                    'manual': str(manual_row.get(col, '')),
                    'generated': str(generated_row.get(col, '')),
                    'manual_normalized': manual_val,
                    'generated_normalized': generated_val
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
            
            for row_info in result['unmatched_manual']:
                concept_id = row_info['id']
                concept_name = row_info['concept_name']
                
                # Create proper Google Sheets URL with range
                if result.get('target_info') and result['target_info'].get('worksheet_url') and row_info.get('row_num'):
                    base_url = result['target_info']['worksheet_url']
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
            
            for row_info in result['unmatched_generated']:
                concept_id = row_info['id']
                concept_name = row_info['concept_name']
                
                # Create relative link to CSV file
                csv_filename = f"output/{result['name']}.csv"
                concept_id_link = f"[{concept_id}]({csv_filename})"
                
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
                
                for col, stats in result['column_differences'].items():
                    match_rate = stats['match_rate'] * 100
                    report += f"| {col} | {stats['matching']} | {stats['total']} | {match_rate:.1f}% |\n"
                report += "\n"
            
            # Single comprehensive table for all discrepancies
            report += "#### All Discrepancies\n\n"
            
            # First, collect column stats to determine which ones have >5 blanks
            column_blank_counts = {}
            for row_diff in result['discrepancies']:
                for col, diff in row_diff['differences'].items():
                    if col not in column_blank_counts:
                        column_blank_counts[col] = {'manual_blanks': 0, 'generated_blanks': 0, 'total': 0}
                    column_blank_counts[col]['total'] += 1
                    if diff['manual_normalized'] == '':
                        column_blank_counts[col]['manual_blanks'] += 1
                    if diff['generated_normalized'] == '':
                        column_blank_counts[col]['generated_blanks'] += 1
            
            # Show counts for columns with >5 blanks
            high_blank_columns = []
            for col, stats in column_blank_counts.items():
                if stats['manual_blanks'] > 5 or stats['generated_blanks'] > 5:
                    high_blank_columns.append(col)
                    report += f"**{col}**: {stats['manual_blanks']} manual blanks, {stats['generated_blanks']} generated blanks (out of {stats['total']} total differences)\n\n"
            
            if high_blank_columns:
                report += "\n"
            
            # Show detailed table for columns without excessive blanks
            detailed_columns = [col for col in column_blank_counts.keys() if col not in high_blank_columns]
            
            if detailed_columns:
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
                
                # Group by concept using nested lists
                for row_diff in result['discrepancies']:
                    concept_id = row_diff['id']
                    concept_name_manual = row_diff['concept_name_manual']
                    
                    # Get row numbers for linking
                    manual_row_num = None
                    generated_row_num = None
                    
                    if result.get('target_info'):
                        id_column = result['target_info']['id_column']
                        
                        # Find row number in manual dataframe
                        for idx, df_row in result['manual_df'].iterrows():
                            if str(df_row[id_column]) == str(concept_id):
                                manual_row_num = idx + 3  # +3 for header, descriptions, and 1-indexed
                                break
                        
                        # Find row number in generated dataframe  
                        for idx, df_row in result['generated_df'].iterrows():
                            if str(df_row[id_column]) == str(concept_id):
                                generated_row_num = idx + 2  # +2 for header and 1-indexed
                                break
                    
                    # Show concept header with nested differences
                    concept_has_details = False
                    concept_details = []
                    
                    for col, diff in row_diff['differences'].items():
                        if col in detailed_columns:  # Only show detailed entries for non-high-blank columns
                            concept_has_details = True
                            
                            # Create linked values with proper column references
                            manual_val = diff['manual'] if diff['manual'] else 'blank'
                            generated_val = diff['generated'] if diff['generated'] else 'blank'
                            
                            # Create manual link with correct column
                            manual_val_link = manual_val
                            if result.get('target_info') and result['target_info'].get('worksheet_url') and manual_row_num:
                                col_letter = get_column_letter(col, result['manual_df'])
                                base_url = result['target_info']['worksheet_url']
                                manual_url = f"{base_url}&range={col_letter}{manual_row_num}"
                                manual_val_link = f"[{manual_val}]({manual_url})"
                            
                            # Create generated link with line number
                            generated_val_link = generated_val
                            if generated_row_num:
                                csv_path = f"output/{result['name']}.csv"
                                generated_url = f"{csv_path}#L{generated_row_num}"
                                generated_val_link = f"[{generated_val}]({generated_url})"
                            
                            # Add to concept details
                            concept_details.append(f"  - **{col}**: 🔴 {manual_val_link} vs 🔵 {generated_val_link}")
                    
                    # Only show concept if it has details
                    if concept_has_details:
                        report += f"- **{concept_id}**: {concept_name_manual}\n"
                        for detail in concept_details:
                            report += f"{detail}\n"
                        report += "\n"
    
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
        
        for target in validation_targets:
            print(f"\nValidating {target['name']}...")
            
            # Load manual worksheet data
            print(f"  Loading manual data from {target['worksheet_name']}...")
            df_manual = load_worksheet_data(gc, target['spreadsheet_name'], target['worksheet_name'])
            
            # Load generated CSV data
            print(f"  Loading generated data from {target['csv_path']}...")
            df_generated = load_csv_data(target['csv_path'])
            
            # Compare the data
            print("  Comparing data...")
            results = compare_dataframes(df_manual, df_generated, target['id_column'], target['name'], target)
            all_results.append(results)
            
            if 'error' not in results:
                error_count = len(results.get('errors', []))
                discrepancy_count = len(results.get('discrepancies', []))
                print(f"  Results: {results['matched_rows']} matched rows, {error_count} errors, {discrepancy_count} discrepancies")
        
        # Generate and save report
        print("\nGenerating validation report...")
        report = generate_markdown_report(all_results)
        
        # Save report to file
        report_path = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Validation report saved to: {report_path}")
        
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