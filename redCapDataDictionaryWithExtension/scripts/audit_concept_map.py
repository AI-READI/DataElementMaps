"""Release audit for the AI-READI concept map (run before every release).

Part A - structural checks (each should report 0 rows unless noted):
  A1  Custom target (2005200xxx) missing from concept_manual.csv, or name/domain differs
  A2  Same TARGET_CONCEPT_ID used with different name, domain, vocabulary or code
  A3  Non-custom target not flagged standard ('S')
  A4  Predicate/confidence: exactMatch with confidence < 1; target 0 with a predicate;
      non-zero target without a predicate
  A5  Duplicate (FORM_NAME, FIELD_ID, SRC_CODE, row type) keys
      (informational: Yes answers deliberately mapped to both a Condition/Observation
      concept and the Yes value are listed here)
  A6  Leading/trailing spaces or non-breaking spaces in key columns
  A7  Custom concept used as a Condition/answer target where a review is due
      (lists every custom Condition target; check whether a standard concept exists)
  A8  Answer rows whose FIELD_ID matches no question row (a field-name typo stops the
      ETL from linking the answers; e.g. pxne9_ and pxrd9 before v1.5)

Part B - review lists (read every row; nothing here is automatically wrong):
  B1  Answer rows whose source text differs from the target concept name
  B2  Question rows mapped to standard concepts (source text vs target name)

Part C - same row type, same predicate convention (informational):
  C1  "Other (please specify)" style rows and their predicates
  C2  Distinct predicate/confidence combinations with counts

Usage (from any folder):
    python redCapDataDictionaryWithExtension/scripts/audit_concept_map.py [mapping.csv] [--out report.md]

Databricks notebook (files in a Volume or a Git folder; no extra packages needed):
    %sh
    python /Workspace/<path>/audit_concept_map.py /Volumes/<catalog>/<schema>/<volume>/_ai_readi_redcap_value_set_mapping_common.csv \
        --concept-manual /Volumes/<catalog>/<schema>/<volume>/concept_manual.csv \
        --out /Volumes/<catalog>/<schema>/<volume>/audit_concept_map_report.md

Writes a Markdown report (default: audit_concept_map_report.md next to this script)
and prints a summary. Line numbers refer to the CSV file (header = line 1).
Vocabulary checks against the deployed OMOP vocabulary are in validate_concept_map_vocab.sql.
"""
import argparse
import collections
import csv
import re
import sys
from pathlib import Path

try:
    HERE = Path(__file__).resolve().parent
except NameError:  # pasted into a notebook cell: no __file__; pass paths to run_audit() instead
    HERE = Path.cwd()
ROOT = HERE.parent
DEFAULT_MAP = ROOT / "value-set-mapping-common" / "_ai_readi_redcap_value_set_mapping_common.csv"
CONCEPT_MANUAL = ROOT / "OHDSI-vocabulary-request" / "concept_manual.csv"
MAP_COLUMNS = ["Map_to_OMOP", "transferred_to_fairhub_REDCap_dataset", "Protected_or_open-source", "Extension_Needed",
               "FORM_NAME", "FIELD_TYPE", "FIELD_ID", "FIELD_ID_NUM", "temp_Question_or_Answer", "SRC_CODE",
               "SRC_CODE_ID", "SRC_CD_DESCRIPTION", "TARGET_CONCEPT_ID", "LOCAL_CONCEPT_ID", "TARGET_CONCEPT_NAME",
               "TARGET_DOMAIN_ID", "TARGET_VOCABULARY_ID", "TARGET_CONCEPT_CLASS_ID", "TARGET_CONCEPT_CODE",
               "TARGET_STANDARD_CONCEPT", "PREDICATE_ID", "CONFIDENCE", "MODIFIER", "value_as_concept_id",
               "qualifier_concept_id", "qualifier_source_value"]
KEY_COLS = ["FIELD_ID", "SRC_CODE", "TARGET_CONCEPT_ID", "TARGET_CONCEPT_NAME",
            "TARGET_DOMAIN_ID", "TARGET_VOCABULARY_ID", "TARGET_CONCEPT_CODE", "PREDICATE_ID", "CONFIDENCE"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def is_custom(cid):
    return cid.startswith("20052")


def mapped(cid):
    return cid not in ("", "0")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("mapping", nargs="?", default=str(DEFAULT_MAP))
    ap.add_argument("--concept-manual", default=str(CONCEPT_MANUAL),
                    help="path to concept_manual.csv (default: the copy in this repository)")
    ap.add_argument("--out", default=str(HERE / "audit_concept_map_report.md"))
    a, _ = ap.parse_known_args(argv)  # ignore extra arguments added by notebook runners

    with open(a.mapping, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for i, r in enumerate(rows):
        r["_ln"] = i + 2
    with open(a.concept_manual, encoding="utf-8-sig", newline="") as f:
        cm = {c["concept_id"].strip(): c for c in csv.DictReader(f)}
    return audit(rows, cm, a.out, Path(a.mapping).name)


def _text(v):
    """Table values to the text the CSV would hold (None -> '', 1.0 -> '1')."""
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def run_audit_table(table="hive_metastore.redcapsurveydb.ai_readi_redcap_value_set_mapping_common",
                    concept_manual=None, out=None):
    """Databricks entry point: audit the concept map loaded as a table.

    table          : the mapping table (every column as in the CSV)
    concept_manual : optional path to concept_manual.csv, or a table name holding it;
                     if omitted, check A1 (custom concepts vs concept_manual) is skipped
    out            : optional path for the Markdown report (e.g. a /Volumes/... path)

    A Spark table has no row order, so the 'Line' column is blank; rows are identified
    by FIELD_ID and SRC_CODE. Use the CSV entry points for line numbers.
    """
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.getOrCreate()
    # column names as in the CSV header, whatever case the table stores them in
    canon = {c.lower(): c for c in MAP_COLUMNS}
    rows = [{canon.get(k.lower(), k): _text(v) for k, v in r.asDict().items()} for r in spark.table(table).collect()]
    missing = [c for c in MAP_COLUMNS if c not in rows[0]] if rows else MAP_COLUMNS
    if missing:
        raise ValueError(f"{table} is missing columns: {missing}")
    for r in rows:
        r["_ln"] = ""
    cm = None
    if concept_manual:
        if concept_manual.lower().endswith(".csv"):
            with open(concept_manual, encoding="utf-8-sig", newline="") as f:
                cm = {c["concept_id"].strip(): c for c in csv.DictReader(f)}
        else:
            cm = {_text(r["concept_id"]).strip(): {k: _text(v) for k, v in r.asDict().items()}
                  for r in spark.table(concept_manual).collect()}
    return audit(rows, cm, out, table)


def audit(rows, cm, out, label):
    """Run all checks. rows: list of dicts (CSV columns as text, plus '_ln'); cm: concept_manual by id or None."""
    for r in rows:
        r["_raw"] = {k: v for k, v in r.items() if k != "_ln"}
        for k in list(r):
            if isinstance(r[k], str) and not k.startswith("_"):
                r[k] = r[k].strip()

    sections = []  # (title, header, rows, expect_zero)

    # A1
    a1 = []
    for r in rows if cm is not None else []:
        t = r["TARGET_CONCEPT_ID"]
        if is_custom(t):
            c = cm.get(t)
            if not c:
                a1.append((r["_ln"], r["FIELD_ID"], r["SRC_CODE"], t, "not in concept_manual.csv"))
            elif c["concept_name"].strip() != r["TARGET_CONCEPT_NAME"]:
                a1.append((r["_ln"], r["FIELD_ID"], r["SRC_CODE"], t, f"name: map '{r['TARGET_CONCEPT_NAME']}' vs manual '{c['concept_name'].strip()}'"))
            elif c["domain_id"].strip() != r["TARGET_DOMAIN_ID"]:
                a1.append((r["_ln"], r["FIELD_ID"], r["SRC_CODE"], t, f"domain: map {r['TARGET_DOMAIN_ID']} vs manual {c['domain_id'].strip()}"))
    sections.append(("A1 Custom targets vs concept_manual.csv" + ("" if cm is not None else " (skipped: no concept_manual given)"), ["Line", "FIELD_ID", "SRC_CODE", "Concept", "Problem"], a1, True))

    # A2
    g = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        if mapped(r["TARGET_CONCEPT_ID"]):
            sig = (r["TARGET_CONCEPT_NAME"], r["TARGET_DOMAIN_ID"], r["TARGET_VOCABULARY_ID"], r["TARGET_CONCEPT_CODE"])
            g[r["TARGET_CONCEPT_ID"]][sig].append(r["_ln"])
    a2 = []
    for cid, sigs in g.items():
        if len(sigs) > 1:
            for sig, lns in sigs.items():
                a2.append((cid, " / ".join(x or "(blank)" for x in sig), f"{len(lns)}: " + ", ".join(map(str, lns[:15])) + (" ..." if len(lns) > 15 else "")))
    sections.append(("A2 Same concept_id with different name/domain/vocabulary/code", ["Concept", "Name / domain / vocabulary / code", "Rows (lines)"], a2, True))

    # A3
    a3 = [(r["_ln"], r["FIELD_ID"], r["SRC_CODE"], r["TARGET_CONCEPT_ID"], r["TARGET_CONCEPT_NAME"], r["TARGET_STANDARD_CONCEPT"])
          for r in rows if mapped(r["TARGET_CONCEPT_ID"]) and not is_custom(r["TARGET_CONCEPT_ID"]) and r["TARGET_STANDARD_CONCEPT"] != "S"]
    sections.append(("A3 Non-custom target not flagged standard", ["Line", "FIELD_ID", "SRC_CODE", "Concept", "Name", "Standard"], a3, True))

    # A4
    a4 = []
    for r in rows:
        p, c, t = r["PREDICATE_ID"], r["CONFIDENCE"], r["TARGET_CONCEPT_ID"]
        if p == "skos:exactMatch" and c != "1":
            a4.append((r["_ln"], r["FIELD_ID"], r["SRC_CODE"], t, p, c, "exactMatch with confidence < 1"))
        if t == "0" and p:
            a4.append((r["_ln"], r["FIELD_ID"], r["SRC_CODE"], t, p, c, "target 0 with a predicate"))
        if mapped(t) and not p:
            a4.append((r["_ln"], r["FIELD_ID"], r["SRC_CODE"], t, p, c, "target without a predicate"))
    sections.append(("A4 Predicate / confidence rules", ["Line", "FIELD_ID", "SRC_CODE", "Concept", "Predicate", "Confidence", "Problem"], a4, True))

    # A5
    k = collections.defaultdict(list)
    for r in rows:
        k[(r["FORM_NAME"], r["FIELD_ID"], r["SRC_CODE"], r["temp_Question_or_Answer"])].append(r)
    a5 = []
    for key, rs in k.items():
        if len(rs) > 1:
            a5.append((" / ".join(key), ", ".join(str(r["_ln"]) for r in rs),
                       " | ".join(f"{r['TARGET_CONCEPT_ID']} {r['TARGET_CONCEPT_NAME'][:40]} ({r['TARGET_DOMAIN_ID']})" for r in rs)))
    sections.append(("A5 Duplicate keys (informational: Yes -> Condition/Observation + Yes value pairs are expected)",
                     ["Form / field / code / type", "Lines", "Targets"], a5, False))

    # A6
    a6 = []
    for r in rows:
        for col in KEY_COLS + ["SRC_CD_DESCRIPTION", "MODIFIER"]:
            v = r["_raw"].get(col, "") or ""
            if v != v.strip() or "\u00a0" in v:
                a6.append((r["_ln"], col, repr(v[:60])))
    sections.append(("A6 Leading/trailing or non-breaking spaces", ["Line", "Column", "Value"], a6, True))

    # A7
    a7 = [(r["_ln"], r["FIELD_ID"], r["SRC_CODE"], r["SRC_CD_DESCRIPTION"][:60], r["TARGET_CONCEPT_ID"], r["TARGET_CONCEPT_NAME"][:60])
          for r in rows if is_custom(r["TARGET_CONCEPT_ID"]) and r["TARGET_DOMAIN_ID"] == "Condition"]
    sections.append(("A7 Custom concepts used as Condition targets (check for a standard alternative)",
                     ["Line", "FIELD_ID", "SRC_CODE", "Source text", "Concept", "Name"], a7, False))

    # A8
    qcodes = {r["SRC_CODE"] for r in rows if r["temp_Question_or_Answer"] == "Question"}
    a8 = [(r["_ln"], r["FORM_NAME"], r["FIELD_ID"], r["SRC_CODE"], r["SRC_CD_DESCRIPTION"][:60], r["TARGET_CONCEPT_ID"])
          for r in rows if r["temp_Question_or_Answer"] == "Answer" and r["FIELD_ID"] not in qcodes]
    sections.append(("A8 Answers whose FIELD_ID matches no question row (field-name typos; administrative fields expected)",
                     ["Line", "Form", "FIELD_ID", "SRC_CODE", "Source text", "Concept"], a8, False))

    # B1
    b1 = [(r["_ln"], r["FIELD_ID"], r["SRC_CODE"], r["SRC_CD_DESCRIPTION"][:80], r["TARGET_CONCEPT_ID"], r["TARGET_CONCEPT_NAME"][:80],
           r["TARGET_DOMAIN_ID"], f"{r['PREDICATE_ID'].replace('skos:', '')} {r['CONFIDENCE']}")
          for r in rows if r["temp_Question_or_Answer"] == "Answer" and mapped(r["TARGET_CONCEPT_ID"])
          and not is_custom(r["TARGET_CONCEPT_ID"]) and norm(r["SRC_CD_DESCRIPTION"]) != norm(r["TARGET_CONCEPT_NAME"])]
    sections.append(("B1 Answers whose text differs from the target name (review each)",
                     ["Line", "FIELD_ID", "SRC_CODE", "Source text", "Concept", "Target name", "Domain", "Predicate"], b1, False))

    # B2
    b2 = [(r["_ln"], r["SRC_CODE"], r["SRC_CD_DESCRIPTION"][:100], r["TARGET_CONCEPT_ID"], r["TARGET_CONCEPT_NAME"][:80],
           r["TARGET_DOMAIN_ID"], f"{r['PREDICATE_ID'].replace('skos:', '')} {r['CONFIDENCE']}")
          for r in rows if r["temp_Question_or_Answer"] == "Question" and mapped(r["TARGET_CONCEPT_ID"]) and not is_custom(r["TARGET_CONCEPT_ID"])]
    sections.append(("B2 Questions mapped to standard concepts (review each)",
                     ["Line", "SRC_CODE", "Source text", "Concept", "Target name", "Domain", "Predicate"], b2, False))

    # C1
    c1 = [(r["_ln"], r["SRC_CODE"] if r["temp_Question_or_Answer"] == "Question" else f"{r['FIELD_ID']}={r['SRC_CODE']}",
           r["SRC_CD_DESCRIPTION"][:60], r["TARGET_CONCEPT_ID"], r["TARGET_CONCEPT_NAME"][:50], f"{r['PREDICATE_ID'].replace('skos:', '')} {r['CONFIDENCE']}")
          for r in rows if mapped(r["TARGET_CONCEPT_ID"]) and re.match(r"^(yes, )?other\b", r["SRC_CD_DESCRIPTION"].lower())]
    sections.append(("C1 'Other' rows and their predicates (should follow one convention)",
                     ["Line", "Field", "Source text", "Concept", "Target name", "Predicate"], c1, False))

    # C2
    pc = collections.Counter((r["PREDICATE_ID"] or "(blank)", r["CONFIDENCE"] or "(blank)") for r in rows)
    c2 = [(p, c, n) for (p, c), n in pc.most_common()]
    sections.append(("C2 Predicate / confidence combinations", ["Predicate", "Confidence", "Rows"], c2, False))

    # write report
    esc = lambda v: str(v).replace("|", "\\|").replace("\n", " ")
    md = [f"# Concept map audit\n\nSource: `{label}` ({len(rows)} data rows)\n",
           "Part A checks marked *expect 0* should report no rows. Parts B and C are review lists.\n",
           "Vocabulary checks (standard, valid, name match in the deployed `omop_vocab`) are in `validate_concept_map_vocab.sql`.\n"]
    print(f"{label}: {len(rows)} data rows")
    for title, hdr, data, expect0 in sections:
        flag = ""
        if expect0:
            flag = " - OK" if not data else " - CHECK"
        print(f"  {title}: {len(data)}{flag}")
        md.append(f"\n## {title}: {len(data)}{' (expect 0)' if expect0 else ''}\n")
        if data:
            md.append("| " + " | ".join(hdr) + " |\n|" + "---|" * len(hdr) + "\n")
            md.extend("| " + " | ".join(esc(v) for v in row) + " |\n" for row in data)
    if out:
        out = str(out)
        if out.startswith("file:"):  # Databricks-style URI -> local path
            out = out[len("file:"):]
        Path(out).write_text("".join(md), encoding="utf-8")
        print(f"Report: {out}")
    return {title: {"header": hdr, "rows": data} for title, hdr, data, _ in sections}


def run_audit(mapping, concept_manual, out="audit_concept_map_report.md"):
    """Notebook entry point, e.g. in Databricks after pasting this file into a cell:
    run_audit("/Volumes/<catalog>/<schema>/<volume>/_ai_readi_redcap_value_set_mapping_common.csv",
              "/Volumes/<catalog>/<schema>/<volume>/concept_manual.csv",
              "/Volumes/<catalog>/<schema>/<volume>/audit_concept_map_report.md")
    """
    main([str(mapping), "--concept-manual", str(concept_manual), "--out", str(out)])


if __name__ == "__main__" and "__file__" in globals():
    main()
