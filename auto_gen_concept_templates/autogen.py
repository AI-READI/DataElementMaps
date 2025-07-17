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
                if tag in source_def or 'both' in source_def:
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

if __name__ == "__main__":
    main()
