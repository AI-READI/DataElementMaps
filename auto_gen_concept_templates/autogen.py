import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
import pandas as pd

mapping_sources = [
    {
        'spreadsheet_name': 'AIREADI MOCA Data Dictionary and Mappings v0.3',
        'worksheet_name': 'MOCA Data Dictionary with Extensions',
        'process': True,
        'tag': 'MOCA',
    },
    {
        'spreadsheet_name': 'REDCap Data Dictionary and OMOP Mappings',
        'worksheet_name': '_master REDCap Data Dictionary with Extensions',
        'process': False,
        'tag': 'RedCap',
    },
]
outputs = [
    {
        'name': 'concept_manual.csv',
        'columns': {
            'concept_name':     {'MOCA': 'TARGET_CONCEPT_NAME'},
            'SRC_CODE':         {'default': ''},
            'concept_id':       {'MOCA': 'TARGET_CONCEPT_ID'},
            'vocabulary_id':    {'MOCA': 'TARGET_VOCABULARY_ID'},
            'domain_id':        {'MOCA': 'TARGET_DOMAIN_ID'},
            'v6_domain_id':     {'default': 'survey_conduct'},
            'concept_class_id': {'MOCA': 'TARGET_CONCEPT_CLASS_ID'},
            'standard_concept': {'MOCA': 'TARGET_STANDARD_CONCEPT'},
            'valid_start_date': {'default': '1/1/1970'},
            'valid_end_date':   {'default': ''},
            'invalid_reason':   {'default': ''},
        }
    },
    {
        'name': 'concept_relationship_manual.csv',
        'columns': {
            'concept_name': {'MOCA': 'TARGET_CONCEPT_NAME'},
            'concept_id_1': {'MOCA': 'TARGET_CONCEPT_ID'},
            'SRC_CODE': {'default': ''},
            'vocabulary_id_1': {'MOCA': 'TARGET_VOCABULARY_ID'},
            'relationship_id': {'default': ''},
            'concept_id_2': {'default': '606671'},
            'temp name': {'default': 'Montreal Cognitive Assessment version 8.1'},
            'temp domain': {'default': 'Measurement'},
            'vocabulary_id_2': {'default': 'SNOMED'},
            'temp class': {'default': 'Staging / Scales'},
            'concept_code_2': {'default': '1148423001'},
            'temp standard': {'default': 'S'},
            'relationship_valid_start_date': {'default': ''},
            'relationship_valid_end_date': {'default': ''},
            'invalid_reason': {'default': ''},
            'confidence': {'default': '1'},
            'predicate_id': {'default': 'skos:broadMatch'},
            'mapping_source': {'default': 'ManualMapping'},
            'mapping_justification': {'default': 'ManualMappingCuration'},
            'mapping_tool': {'default': ''},
            'Notes': {'default': ''},
        }
    },
]


def main():
    gc = gspread.service_account()

    for source in mapping_sources:
        if not source['process']:
            continue

        spreadsheet = gc.open(source['spreadsheet_name'])
        mapping = spreadsheet.worksheet(source['worksheet_name'])
        df_all = get_as_dataframe(mapping)
        df = df_all.copy()[df_all['TARGET_CONCEPT_ID'] > 2000000000]
        tag = source['tag']

        for ofile in outputs:
            columns = ofile['columns']
            result_data = {}

            # Process each column in the output specification
            for col_name, source_def in columns.items():
                if tag in source_def:
                    # Use the source column from the dataframe
                    source_col = source_def[tag]
                    if source_col in df.columns:
                        result_data[col_name] = df[source_col].values
                    else:
                        print(f"Warning: Column '{source_col}' not found in source data")
                        result_data[col_name] = [source_def.get('default', '')] * len(df)
                else:
                    # Use default value for all rows
                    default_value = source_def.get('default', '')
                    result_data[col_name] = [default_value] * len(df)

            # Create DataFrame from the result data
            result_df = pd.DataFrame(result_data)

            # Save to CSV
            filename = 'output/' + ofile['name']
            result_df.to_csv(filename, index=False)
            print(f"Saved {filename} with {len(result_df)} rows")

if __name__ == "__main__":
    main()
