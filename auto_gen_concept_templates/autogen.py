import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import pandas as pd

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
concept_rel_man_old = {
        'spreadsheet_name': 'template_4_adding_vocabulary-2',
        'worksheet_name': 'concept_relationship_manual',
        'location': 'https://docs.google.com/spreadsheets/d/1IDjSfI9Kbr9VGeL9hTxO4ic6xBEMNs88b1f8DHPgKPY/edit?gid=933853125#gid=933853125',
}
outputs = [
    {
        'name': 'concept_manual.csv',
        'columns': {
            'concept_name':     {'both': 'TARGET_CONCEPT_NAME'},
            'SRC_CODE':         {'both': 'SRC_CODE', },
            'concept_id':       {'both': 'TARGET_CONCEPT_ID', },
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
        'name': 'concept_relationship_manual.csv',
        'columns': {
            'concept_name': {'both': 'TARGET_CONCEPT_NAME'},
            'concept_id_1': {'both': 'TARGET_CONCEPT_ID'},
            'SRC_CODE': {'both': 'SRC_CODE', },
            'vocabulary_id_1': {'both': 'TARGET_VOCABULARY_ID'},
            'relationship_id': {'default': ''},
            'concept_id_2': {'defaultMOCA': '606671'},
            #   leave concept_id_2 blank for redcap
            #   same with all below
            'temp name': {'defaultMOCA': 'Montreal Cognitive Assessment version 8.1'},
            'temp domain': {'defaultMOCA': 'Measurement'},
            'vocabulary_id_2': {'defaultMOCA': 'SNOMED'},
            'temp class': {'defaultMOCA': 'Staging / Scales'},
            'concept_code_2': {'defaultMOCA': '1148423001'},
            'temp standard': {'defaultMOCA': 'S'},
            'relationship_valid_start_date': {'default': ''},
            'relationship_valid_end_date': {'default': ''},
            'invalid_reason': {'default': ''},
            'confidence': {'defaultMOCA': '1'},
            'predicate_id': {'defaultMOCA': 'skos:broadMatch'},
            'mapping_source': {'defaultMOCA': 'ManualMapping'},
            'mapping_justification': {'defaultMOCA': 'ManualMappingCuration'},
            'mapping_tool': {'default': ''},
            'Notes': {'default': ''},
        }
    },
]

def main():
    output_dfs = {}
    gc = gspread.service_account()

    crm_old_spreadsheet = gc.open(concept_rel_man_old['spreadsheet_name'])
    crm_old_worksheet = crm_old_spreadsheet.worksheet(concept_rel_man_old['worksheet_name'])
    crm_df = get_as_dataframe(crm_old_worksheet)
    crm_df = crm_df.iloc[1:415] # THIS WILL BREAK IF WORKSHEET CHANGES, BUT IS NECESSARY FOR GETTING RID OF
                                #   SUBTITLE ROW AND BLANK ROWS AT BOTTOM
    crm_df = crm_df.fillna('')
    # check_primary_keys(crm_df)
    cid2 = {str(row['concept_id_1']): row['concept_id_2'] for index, row in crm_df.iterrows()}

    for source in mapping_sources:
        if not source['process']:
            continue

        tag = source['tag']
        output_dfs[tag] = {}

        spreadsheet = gc.open(source['spreadsheet_name'])
        mapping = spreadsheet.worksheet(source['worksheet_name'])
        df_all = get_as_dataframe(mapping)
        df_all['TARGET_CONCEPT_ID'] = pd.to_numeric(df_all['TARGET_CONCEPT_ID'], errors='coerce').fillna(0).astype(int)
        if 'Extension_Needed' in df_all.columns:
            df = df_all[(df_all['TARGET_CONCEPT_ID'] > 2000000000) |
                        (df_all['Extension_Needed'] == 'Yes') |
                        (df_all['TARGET_VOCABULARY_ID'] == 'AIREADI-Vision') ]
        else:
            df = df_all[df_all['TARGET_CONCEPT_ID'] > 2000000000]

        for ofile in outputs:
            columns = ofile['columns']
            result_data = {}

            # Process each column in the output specification
            for col_name, source_def in columns.items():
                if col_name == 'concept_id_2' and  ofile['name'] == 'concept_relationship_manual.csv':
                    if tag == 'MOCA':
                        result_data['concept_id_2'] = df['TARGET_CONCEPT_ID'].apply(lambda x: cid2.get(str(x), source_def['defaultMOCA']))
                    else:
                        result_data['concept_id_2'] = df['TARGET_CONCEPT_ID'].apply(lambda x: cid2.get(str(x), ''))
                elif tag in source_def or 'both' in source_def:
                    # Use the source column from the dataframe
                    source_col = source_def[tag] if tag in source_def else source_def['both']
                    if source_col in df.columns:
                        result_data[col_name] = df[source_col].values
                    else:
                        print(f"Warning: Column '{source_col}' not found in source data")
                        result_data[col_name] = [source_def.get('default', '')] * len(df)
                else:
                    if f'default{tag}' in source_def:
                        default_value = source_def.get(f'default{tag}', '')
                    else:
                        default_value = source_def.get('default', '')
                    # Use default value for all rows
                    result_data[col_name] = [default_value] * len(df)

            # Create DataFrame from the result data
            result_df = pd.DataFrame(result_data)
            if 'concept_id' in result_df.columns:
                result_df['concept_id'] = result_df['concept_id'].astype(int)
            if 'concept_id_1' in result_df.columns:
                result_df['concept_id_1'] = result_df['concept_id_1'].astype(int)

            result_df['source'] = tag

            output_dfs[tag][ofile['name']] = result_df

    combined_dfs = {}
    for tag, dfs in output_dfs.items():
        for fname, df in dfs.items():
            combined_dfs[fname] = combined_dfs.get(fname, [])
            combined_dfs[fname].append(df)
            filename = f'output/{tag}_{fname}'
            df.to_csv(filename, index=False)
            print(f"Saved {filename} with {len(df)} rows")

        # Save to CSVs
    for fname, dfs in combined_dfs.items():
        df = pd.concat(dfs, ignore_index=True)
        filename = f'output/{fname}'
        df.to_csv(filename, index=False)
        print(f"Saved {filename} with {len(df)} rows")

    pass


# Check if columns can serve as primary keys
# A primary key must have unique values and no nulls

def check_primary_key(df, column_name):
    """
    Check if a column can serve as a primary key
    Returns a dictionary with validation results
    """
    total_rows = len(df)
    unique_count = df[column_name].nunique()
    null_count = df[column_name].isnull().sum()

    is_unique = unique_count == total_rows
    has_no_nulls = null_count == 0
    can_be_primary_key = is_unique and has_no_nulls

    return {
        'column': column_name,
        'total_rows': total_rows,
        'unique_values': unique_count,
        'null_values': null_count,
        'is_unique': is_unique,
        'has_no_nulls': has_no_nulls,
        'can_be_primary_key': can_be_primary_key
    }


def check_composite_primary_key(df, columns):
    """
    Check if a combination of columns can serve as a composite primary key
    """
    total_rows = len(df)
    # Create a tuple of the column values for uniqueness check
    combined_values = df[columns].apply(tuple, axis=1)
    unique_count = combined_values.nunique()

    # Check for nulls in any of the columns
    null_count = df[columns].isnull().any(axis=1).sum()

    is_unique = unique_count == total_rows
    has_no_nulls = null_count == 0
    can_be_primary_key = is_unique and has_no_nulls

    return {
        'columns': columns,
        'total_rows': total_rows,
        'unique_combinations': unique_count,
        'rows_with_nulls': null_count,
        'is_unique': is_unique,
        'has_no_nulls': has_no_nulls,
        'can_be_primary_key': can_be_primary_key
    }


def check_primary_keys(df):
    print("=== PRIMARY KEY VALIDATION ===\n")

    # Check concept_id_1 as primary key
    print("1. Checking concept_id_1 as primary key:")
    result1 = check_primary_key(df, 'concept_id_1')
    for key, value in result1.items():
        print(f"   {key}: {value}")

    print(f"\n✓ concept_id_1 CAN be primary key: {result1['can_be_primary_key']}\n")

    # Check [concept_name, SRC_CODE] as composite primary key
    print("2. Checking [concept_name, SRC_CODE] as composite primary key:")
    result2 = check_composite_primary_key(df, ['concept_name', 'SRC_CODE'])
    for key, value in result2.items():
        print(f"   {key}: {value}")

    print(f"\n✓ [concept_name, SRC_CODE] CAN be primary key: {result2['can_be_primary_key']}\n")

    # Additional analysis: Check for duplicates if not unique
    if not result1['is_unique']:
        print("3. Duplicate analysis for concept_id_1:")
        duplicates = df[df.duplicated('concept_id_1', keep=False)]['concept_id_1'].value_counts()
        print(f"   Number of duplicate values: {len(duplicates)}")
        if len(duplicates) > 0:
            print(f"   Most frequent duplicate: {duplicates.index[0]} (appears {duplicates.iloc[0]} times)")
        else:
            print("   No duplicates found (this shouldn't happen if is_unique=False)")

    if not result2['is_unique']:
        print("4. Duplicate analysis for [concept_name, SRC_CODE]:")
        duplicates = df[df.duplicated(['concept_name', 'SRC_CODE'], keep=False)]
        duplicate_counts = duplicates.groupby(['concept_name', 'SRC_CODE']).size().sort_values(ascending=False)
        print(f"   Number of duplicate combinations: {len(duplicate_counts)}")
        if len(duplicate_counts) > 0:
            top_duplicate = duplicate_counts.index[0]
            print(f"   Most frequent duplicate: {top_duplicate} (appears {duplicate_counts.iloc[0]} times)")
        else:
            print("   No duplicates found (this shouldn't happen if is_unique=False)")

    print("\n=== SUMMARY ===")
    print(f"concept_id_1 as primary key: {'✓ VALID' if result1['can_be_primary_key'] else '✗ INVALID'}")
    print(f"[concept_name, SRC_CODE] as primary key: {'✓ VALID' if result2['can_be_primary_key'] else '✗ INVALID'}")

if __name__ == "__main__":
    main()
