"""Build imported_field_concept_lookup.csv: one row per mapped question on the REDCap `imported` form
(imported labs, MoCA, interview age and education), keyed by the REDCap field name.

Use it in the ETL to join imported records on the field name (`field_id`) and take the OMOP concept from
`target_concept_id`. Since v1.8.8 the map's SRC_CODE of the imported labs is the field name (so `src_code`
equals `field_id`); the LOINC code of each lab is in `target_concept_code`.

Usage (from the repository root):
    python redCapDataDictionaryWithExtension/value-set-mapping-common/scripts/build_imported_field_concept_lookup.py .
Re-run after every change to the concept map. The concept map itself is only read, never changed.
"""
import csv
import sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
D = f"{repo}/redCapDataDictionaryWithExtension/value-set-mapping-common"
r = list(csv.reader(open(f"{D}/_ai_readi_redcap_value_set_mapping_common.csv", newline="", encoding="utf-8-sig")))
C = {c: i for i, c in enumerate(r[0])}
g = lambda x, k: x[C[k]].strip()

# measurement fields whose unit field does not follow <field>_u (same exception as the unit lookup)
UNIT_FIELD = {"import_ldl_cholesterol_calculation": "import_ldl_cholesterol_u"}
NOTE = {"import_ldl_cholesterol_calculation": "Unit row is import_ldl_cholesterol_u (different name)",
        "test_upload_date": "Date of the imported record (MoCA date); no value concept"}

questions, units = [], {}
for n, x in enumerate(r[1:], 2):
    if g(x, "Map_to_OMOP") != "Yes" or g(x, "FORM_NAME") != "imported":
        continue
    t = g(x, "temp_Question_or_Answer")
    field = g(x, "FIELD_ID") or g(x, "SRC_CODE")
    if t == "Question" and g(x, "TARGET_CONCEPT_ID") not in ("", "0"):
        questions.append((n, field, x))
    elif t == "Unit" and g(x, "FIELD_ID"):
        units.setdefault(g(x, "FIELD_ID"), (n, x))

cols = ["field_id", "field_label", "src_code", "target_concept_id", "target_concept_name", "target_domain_id",
        "target_vocabulary_id", "target_concept_code", "unit_concept_id", "unit_concept_name", "unit_source_value",
        "map_line", "map_line_unit", "note"]
out, seen = [], set()
for n, field, x in questions:
    assert field not in seen, f"two question rows for {field}"
    seen.add(field)
    # imported labs keep the short REDCap label in SRC_CODE_ID (SRC_CD_DESCRIPTION is the LOINC name)
    label = g(x, "SRC_CODE_ID") if field.startswith("import_") and g(x, "SRC_CODE_ID") else g(x, "SRC_CD_DESCRIPTION")
    un, ux = units.get(UNIT_FIELD.get(field, field + "_u"), (None, None))
    out.append([field, label, g(x, "SRC_CODE"), g(x, "TARGET_CONCEPT_ID"), g(x, "TARGET_CONCEPT_NAME"),
                g(x, "TARGET_DOMAIN_ID"), g(x, "TARGET_VOCABULARY_ID"), g(x, "TARGET_CONCEPT_CODE"),
                g(ux, "TARGET_CONCEPT_ID") if ux else "", g(ux, "TARGET_CONCEPT_NAME") if ux else "",
                g(ux, "SRC_CODE") if ux else "", n, un or "", NOTE.get(field, "")])

out.sort(key=lambda row: (0 if row[0].startswith("import_") else 1, row[11]))
with open(f"{D}/scripts/imported_field_concept_lookup.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(cols)
    w.writerows(out)
print(len(out), "rows:", sum(1 for o in out if o[0].startswith("import_")), "imported labs,",
      sum(1 for o in out if not o[0].startswith("import_")), "other imported fields")
