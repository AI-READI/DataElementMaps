"""Build imported_field_concept_lookup.csv: one row per mapped question on the REDCap `imported` form
(imported labs, MoCA, interview age and education), keyed by the REDCap field name.

Use it in the ETL to join imported records on the field name (`field_id`) and take the OMOP concept from
`target_concept_id`. Since v1.8.8 the map's SRC_CODE of the imported labs is the field name (so `src_code`
equals `field_id`); the LOINC code of each lab is in `target_concept_code`.

Usage (from the repository root):
    python redCapDataDictionaryWithExtension/value-set-mapping-common/scripts/build_imported_field_concept_lookup.py .
Re-run after every change to the concept map. The concept map itself is only read, never changed.

Reference ranges (v1.8.8): `range_low_field` / `range_high_field` name the REDCap export columns that hold the
participant's reference range for the lab (`<lab>_min` / `<lab>_max`; values may carry <, <=, >, >=), for
MEASUREMENT.range_low / range_high. `range_low_field_alt` / `range_high_field_alt` name the second range columns
(`<lab>_min2` / `<lab>_max2`), whose meaning is not yet documented; do not load them. A column is listed when it is
a FIELD_ID in the concept map or a column of the REDCap export header file in redcap-data-dictionary/.
"""
import csv
import glob
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

# reference-range columns: FIELD_IDs of the map plus the columns of the newest export header in the repo
range_cols = {g(x, "FIELD_ID") for x in r[1:]} | {g(x, "SRC_CODE") for x in r[1:]}
headers = sorted(glob.glob(f"{repo}/redCapDataDictionaryWithExtension/redcap-data-dictionary/redcap_export_header_*.csv"))
if headers:
    range_cols |= {c.strip() for c in next(csv.reader(open(headers[-1], newline="", encoding="utf-8-sig")))}


def rng(field, suffix):
    base = field[:-len("_calculation")] if field.endswith("_calculation") else field
    return base + suffix if field.startswith("import_") and base + suffix in range_cols else ""


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
        "map_line", "map_line_unit", "note",
        "range_low_field", "range_high_field", "range_low_field_alt", "range_high_field_alt"]
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
                g(ux, "SRC_CODE") if ux else "", n, un or "", NOTE.get(field, ""),
                rng(field, "_min"), rng(field, "_max"), rng(field, "_min2"), rng(field, "_max2")])

out.sort(key=lambda row: (0 if row[0].startswith("import_") else 1, row[11]))
with open(f"{D}/scripts/imported_field_concept_lookup.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(cols)
    w.writerows(out)
print(sum(1 for o in out if o[14] or o[15]), "rows with a reference range,",
      sum(1 for o in out for v in o[14:18] if v), "range columns")
print(len(out), "rows:", sum(1 for o in out if o[0].startswith("import_")), "imported labs,",
      sum(1 for o in out if not o[0].startswith("import_")), "other imported fields")
