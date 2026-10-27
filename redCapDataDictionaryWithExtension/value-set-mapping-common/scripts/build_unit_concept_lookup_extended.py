"""Build unit_concept_lookup_extended.csv: one row per field key of unit_concept_lookup.csv, with the measurement
(lab) concept from the field's question row and the unit concept from its unit row.
Usage (from the repository root): python redCapDataDictionaryWithExtension/value-set-mapping-common/scripts/build_unit_concept_lookup_extended.py .
Re-run after every change to the concept map or to unit_concept_lookup.csv."""
import csv, sys
repo = sys.argv[1]
D = f'{repo}/redCapDataDictionaryWithExtension/value-set-mapping-common'
r = list(csv.reader(open(f'{D}/_ai_readi_redcap_value_set_mapping_common.csv', newline='', encoding='utf-8')))
C = {c: i for i, c in enumerate(r[0])}
g = lambda x, k: x[C[k]].strip()
q, u = {}, {}
for n, x in enumerate(r[1:], 2):
    if g(x, 'Map_to_OMOP') != 'Yes': continue
    t = g(x, 'temp_Question_or_Answer')
    if t == 'Question': q.setdefault(g(x, 'FIELD_ID') or g(x, 'SRC_CODE'), (n, x))
    elif t == 'Unit' and g(x, 'FIELD_ID'): u.setdefault(g(x, 'FIELD_ID'), (n, x))
# measurement fields whose unit field does not follow <field>_u
UNIT_FIELD = {'import_ldl_cholesterol_calculation': 'import_ldl_cholesterol_u'}
# lookup keys built from a unit field whose measurement field has another name
LAB_FIELD = {'import_ldl_cholesterol': 'import_ldl_cholesterol_calculation'}
NOTE = {'import_ldl_cholesterol': 'Key from unit field import_ldl_cholesterol_u; the measurement field is import_ldl_cholesterol_calculation',
        'import_ldl_cholesterol_calculation': 'Unit field is import_ldl_cholesterol_u (different name)'}
lk = [x for x in csv.DictReader(open(f'{D}/scripts/unit_concept_lookup.csv', encoding='utf-8')) if x['key_type'] == 'field']
cols = ['lookup_key', 'form_name', 'lab_name', 'lab_concept_id', 'lab_concept_name', 'lab_vocabulary_id', 'lab_concept_code',
        'unit_concept_id', 'unit_concept_name', 'unit_source_value', 'map_line_lab', 'map_line_unit', 'note']
out = []
for k in lk:
    key = k['lookup_key']
    qn, qx = q[LAB_FIELD.get(key, key)]
    un, ux = u[UNIT_FIELD.get(key, key + '_u')]
    assert g(ux, 'TARGET_CONCEPT_ID') == k['unit_concept_id'] and g(ux, 'SRC_CODE') == k['unit_source_value'], key
    assert g(qx, 'TARGET_DOMAIN_ID') == 'Measurement', key
    # lab name: imported labs keep the short REDCap label in SRC_CODE_ID (SRC_CD_DESCRIPTION is the LOINC name)
    name = g(qx, 'SRC_CODE_ID') if g(qx, 'FIELD_ID') and g(qx, 'SRC_CODE_ID') else g(qx, 'SRC_CD_DESCRIPTION')
    out.append([key, g(qx, 'FORM_NAME'), name, g(qx, 'TARGET_CONCEPT_ID'), g(qx, 'TARGET_CONCEPT_NAME'),
                g(qx, 'TARGET_VOCABULARY_ID'), g(qx, 'TARGET_CONCEPT_CODE'), k['unit_concept_id'], g(ux, 'TARGET_CONCEPT_NAME'),
                k['unit_source_value'], qn, un, NOTE.get(key, '')])
with open(f'{D}/scripts/unit_concept_lookup_extended.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n'); w.writerow(cols); w.writerows(out)
print(len(out), 'rows')
