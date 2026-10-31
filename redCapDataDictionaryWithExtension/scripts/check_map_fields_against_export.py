"""Check the concept map's REDCap field names against a REDCap export header.

Usage (from the repository root):
    python redCapDataDictionaryWithExtension/scripts/check_map_fields_against_export.py \\
        redCapDataDictionaryWithExtension/redcap-data-dictionary/redcap_export_header_2026-10-29.csv [mapping.csv]

The header file holds only the first row of a REDCap export (field names, no data). Keep data rows out of
the repository. The mapping file defaults to value-set-mapping-common/_ai_readi_redcap_value_set_mapping_common.csv.

REDCap writes one column per field, and one column per option of a checkbox field: <field>___<code>.
The map names a field in FIELD_ID (answer, unit and imported rows) or SRC_CODE (question rows without FIELD_ID).

Reports
  1. Mapped fields (Map_to_OMOP = Yes) with no export column. Expected for fields left out of the export
     (protected fields in a public export, repeating instruments exported separately); a misspelled field
     name also shows here. Grouped by Protected_or_open-source.
  2. Export columns the map does not name at all (not even as Map_to_OMOP = No).
  3. Checkbox answer rows whose <FIELD_ID>___<SRC_CODE> is not an export column, and export checkbox
     columns with no answer row in the map.
Unit rows name their REDCap unit field (report 2), but a unit row with no export column is not reported:
most unit rows describe a fixed unit with no REDCap field.
Standard library only.
"""
import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAP = ROOT / "redCapDataDictionaryWithExtension/value-set-mapping-common/_ai_readi_redcap_value_set_mapping_common.csv"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    header_path = Path(sys.argv[1])
    map_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_MAP
    with open(header_path, newline="", encoding="utf-8-sig") as f:
        export = [h.strip() for h in next(csv.reader(f)) if h.strip()]
    cols = set(export)
    dup = [h for h, n in collections.Counter(export).items() if n > 1]
    with open(map_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    g = lambda r, k: (r.get(k) or "").strip()

    questions = {}                                # field -> (line, type, mapped, protection)
    answers = collections.defaultdict(list)       # checkbox field -> [(line, code)]
    units = set()                                 # FIELD_ID of unit rows (REDCap unit fields such as import_glucose_u)
    for n, r in enumerate(rows, 2):
        t = g(r, "temp_Question_or_Answer")
        if t == "Question":
            f = g(r, "FIELD_ID") or g(r, "SRC_CODE")
            q = questions.get(f)
            mapped = g(r, "Map_to_OMOP") == "Yes"
            if q is None or (mapped and not q[2]):
                questions[f] = (n, g(r, "FIELD_TYPE"), mapped, g(r, "Protected_or_open-source"))
        elif t == "Answer" and g(r, "FIELD_TYPE") == "checkbox":
            answers[g(r, "FIELD_ID")].append((n, g(r, "SRC_CODE")))
        elif t == "Unit" and g(r, "FIELD_ID"):
            units.add(g(r, "FIELD_ID"))

    def in_export(f, ftype):
        return any(c.startswith(f + "___") for c in cols) if ftype == "checkbox" else f in cols

    print(f"Export header: {header_path} ({len(export)} columns)")
    print(f"Concept map:   {map_path} ({len(rows)} rows, {len(questions)} fields)")
    if dup:
        print(f"Duplicate export columns: {', '.join(dup)}")

    # 1
    missing = collections.defaultdict(list)
    for f, (n, ftype, mapped, prot) in questions.items():
        if mapped and not in_export(f, ftype):
            missing[prot or "(blank)"].append(f"{f} ({n})")
    print(f"\n1. Mapped fields with no export column: {sum(map(len, missing.values()))}")
    for prot, fs in sorted(missing.items()):
        print(f"   {prot} ({len(fs)}): " + ", ".join(fs))

    # 2
    named = set(questions) | units | {f"{f}___{c}" for f, a in answers.items() for _, c in a}
    unnamed = [c for c in export
               if c not in named and not (c.split("___")[0] in questions and "___" in c)]
    print(f"\n2. Export columns not in the map: {len(unnamed)}")
    if unnamed:
        print("   " + ", ".join(unnamed))

    # 3
    bad = [f"{f}___{c} (line {n})" for f, a in answers.items() for n, c in a
           if f"{f}___{c}" not in cols and (f in questions and in_export(f, questions[f][1]) or f not in questions)]
    orphan = [c for c in export if "___" in c and c not in named]
    print(f"\n3a. Checkbox answer rows with no export column: {len(bad)}")
    if bad:
        print("   " + ", ".join(bad))
    print(f"3b. Export checkbox columns with no answer row in the map: {len(orphan)}")
    if orphan:
        print("   " + ", ".join(orphan))


if __name__ == "__main__":
    main()
