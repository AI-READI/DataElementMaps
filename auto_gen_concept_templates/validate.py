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
        'id_column': 'concept_id'
    },
    {
        'name': 'concept_relationship', 
        'spreadsheet_name': 'template_4_adding_vocabulary-2',
        'worksheet_name': 'concept_relationship_manual',
        'csv_path': 'output/concept_relationship.csv',
        'id_column': 'concept_id_1'
    }
]


def normalize_value(value: Any) -> str:
    """
    Normalize a value for comparison by handling whitespace, case, and null differences.
    
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
        # Find first and last valid rows
        start_idx = 0
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
                      id_column: str, name: str) -> Dict[str, Any]:
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
        'row_differences': []
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
    
    # Find common columns (excluding 'source' column that's only in generated data)
    manual_columns = set(df_manual.columns)
    generated_columns = set(df_generated.columns) - {'source'}  # Exclude source column
    common_columns = list(manual_columns.intersection(generated_columns))
    
    # Track column differences
    results['manual_only_columns'] = list(manual_columns - generated_columns)
    results['generated_only_columns'] = list(generated_columns - manual_columns - {'source'})
    
    # Find matching and non-matching rows
    manual_ids = set(manual_dict.keys())
    generated_ids = set(generated_dict.keys())
    
    common_ids = manual_ids.intersection(generated_ids)
    results['matched_rows'] = len(common_ids)
    results['unmatched_manual'] = list(manual_ids - generated_ids)
    results['unmatched_generated'] = list(generated_ids - manual_ids)
    
    # Compare matching rows
    for row_id in common_ids:
        manual_row = manual_dict[row_id]
        generated_row = generated_dict[row_id]
        
        row_diffs = {}
        for col in common_columns:
            manual_val = normalize_value(manual_row.get(col, ''))
            generated_val = normalize_value(generated_row.get(col, ''))
            
            if manual_val != generated_val:
                row_diffs[col] = {
                    'manual': str(manual_row.get(col, '')),
                    'generated': str(generated_row.get(col, '')),
                    'manual_normalized': manual_val,
                    'generated_normalized': generated_val
                }
        
        if row_diffs:
            results['row_differences'].append({
                'id': row_id,
                'differences': row_diffs
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
    report += "| Target | Manual Rows | Generated Rows | Matched Rows | Match Rate |\n"
    report += "|--------|-------------|----------------|--------------|------------|\n"
    
    for result in all_results:
        if 'error' in result:
            report += f"| {result['name']} | ERROR | ERROR | ERROR | {result['error']} |\n"
        else:
            match_rate = result['matched_rows'] / max(result['manual_rows'], result['generated_rows']) * 100
            report += f"| {result['name']} | {result['manual_rows']} | {result['generated_rows']} | {result['matched_rows']} | {match_rate:.1f}% |\n"
    
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
        
        # Column differences summary
        if result['column_differences']:
            report += "### Column Match Rates\n\n"
            report += "| Column | Matching | Total | Match Rate |\n"
            report += "|--------|----------|-------|------------|\n"
            
            for col, stats in result['column_differences'].items():
                match_rate = stats['match_rate'] * 100
                report += f"| {col} | {stats['matching']} | {stats['total']} | {match_rate:.1f}% |\n"
            report += "\n"
        
        # Unmatched rows details
        if result['unmatched_manual']:
            report += f"### Unmatched Manual Rows ({len(result['unmatched_manual'])})\n\n"
            for row_id in result['unmatched_manual']:
                report += f"- {row_id}\n"
            report += "\n"
        
        if result['unmatched_generated']:
            report += f"### Unmatched Generated Rows ({len(result['unmatched_generated'])})\n\n"
            for row_id in result['unmatched_generated']:
                report += f"- {row_id}\n"
            report += "\n"
        
        # Row differences details
        if result['row_differences']:
            report += f"### Row-by-Row Differences ({len(result['row_differences'])} rows with differences)\n\n"
            
            for row_diff in result['row_differences'][:5]:  # Limit to first 5 for readability
                report += f"#### Row ID: {row_diff['id']}\n\n"
                report += "| Column | Manual | Generated |\n"
                report += "|--------|--------|----------|\n"
                
                for col, diff in row_diff['differences'].items():
                    manual_val = diff['manual'][:50] + ('...' if len(diff['manual']) > 50 else '')
                    generated_val = diff['generated'][:50] + ('...' if len(diff['generated']) > 50 else '')
                    report += f"| {col} | {manual_val} | {generated_val} |\n"
                report += "\n"
            
            if len(result['row_differences']) > 5:
                report += f"*... and {len(result['row_differences']) - 5} more rows with differences*\n\n"
    
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
            results = compare_dataframes(df_manual, df_generated, target['id_column'], target['name'])
            all_results.append(results)
            
            if 'error' not in results:
                print(f"  Results: {results['matched_rows']} matched rows, {len(results['row_differences'])} with differences")
        
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
                total_diffs = len(result['row_differences'])
                match_rate = result['matched_rows'] / max(result['manual_rows'], result['generated_rows']) * 100
                print(f"{result['name']}: {match_rate:.1f}% match rate, {total_diffs} rows with differences")
        
    except Exception as e:
        print(f"Error during validation: {e}")
        raise


if __name__ == "__main__":
    main()