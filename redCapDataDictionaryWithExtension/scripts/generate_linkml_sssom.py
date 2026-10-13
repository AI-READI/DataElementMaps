#!/usr/bin/env python3
"""
generate_linkml_sssom.py
Regenerate the LinkML schema/data and SSSOM files from the AI-READI REDCap
value-set mapping CSV.

Usage:
    python generate_linkml_sssom.py <mapping.csv> <repo_root> [--mapping-date YYYY-MM-DD]

Writes:
    <repo_root>/redCapDataDictionaryWithExtension/linkml/
        ai_readi_redcap_value_set_mapping_schema.yaml
        ai_readi_redcap_value_set_mapping_data.yaml
        ai_readi_redcap_value_set_mapping_summary.md
    <repo_root>/redCapDataDictionaryWithExtension/sssom/
        ai_readi_redcap_value_set_mapping.sssom.tsv
        ai_readi_redcap_value_set_mapping.sssom.yaml
        ai_readi_redcap_value_set_mapping_sssom_README.md
        ai_readi_redcap_value_set_mapping_sssom_incomplete_rows.csv

Requires: PyYAML (pip install pyyaml)
"""
import argparse
import csv
import datetime as dt
import os
import re
from collections import Counter

import yaml

# (source column, slot name, range)
COLUMNS = [
    ("Map_to_OMOP", "map_to_omop", "MapToOmopEnum"),
    ("transferred_to_fairhub_REDCap_dataset", "transferred_to_fairhub_redcap_dataset", "YesNoEnum"),
    ("Protected_or_open-source", "protected_or_open_source", "ProtectedOpenSourceEnum"),
    ("Extension_Needed", "extension_needed", "YesNoEnum"),
    ("FORM_NAME", "form_name", "string"),
    ("FIELD_TYPE", "field_type", "FieldTypeEnum"),
    ("FIELD_ID", "field_id", "string"),
    ("FIELD_ID_NUM", "field_id_num", "integer"),
    ("temp_Question_or_Answer", "question_or_answer", "QuestionAnswerEnum"),
    ("SRC_CODE", "src_code", "string"),
    ("SRC_CODE_ID", "src_code_id", "string"),
    ("SRC_CD_DESCRIPTION", "src_cd_description", "string"),
    ("TARGET_CONCEPT_ID", "target_concept_id", "integer"),
    ("LOCAL_CONCEPT_ID", "local_concept_id", "integer"),
    ("TARGET_CONCEPT_NAME", "target_concept_name", "string"),
    ("TARGET_DOMAIN_ID", "target_domain_id", "OmopDomainEnum"),
    ("TARGET_VOCABULARY_ID", "target_vocabulary_id", "VocabularyEnum"),
    ("TARGET_CONCEPT_CLASS_ID", "target_concept_class_id", "string"),
    ("TARGET_CONCEPT_CODE", "target_concept_code", "string"),
    ("TARGET_STANDARD_CONCEPT", "target_standard_concept", "StandardConceptEnum"),
    ("PREDICATE_ID", "predicate_id", "PredicateEnum"),
    ("CONFIDENCE", "confidence", "float"),
    ("MODIFIER", "modifier", "string"),
    ("value_as_concept_id", "value_as_concept_id", "integer"),
    ("qualifier_concept_id", "qualifier_concept_id", "integer"),
    ("qualifier_source_value", "qualifier_source_value", "string"),
]
ENUM_ORDER = ["MapToOmopEnum", "YesNoEnum", "ProtectedOpenSourceEnum", "QuestionAnswerEnum",
              "OmopDomainEnum", "VocabularyEnum", "StandardConceptEnum", "PredicateEnum", "FieldTypeEnum"]

SSSOM_EXTRA = [  # (sssom column, source column)
    ("source_form_name", "FORM_NAME"), ("source_field_type", "FIELD_TYPE"),
    ("source_field_id", "FIELD_ID"), ("source_field_id_num", "FIELD_ID_NUM"),
    ("source_code", "SRC_CODE"), ("source_code_id", "SRC_CODE_ID"),
    ("question_or_answer", "temp_Question_or_Answer"), ("target_concept_id", "TARGET_CONCEPT_ID"),
    ("local_concept_id", "LOCAL_CONCEPT_ID"), ("target_domain_id", "TARGET_DOMAIN_ID"),
    ("target_vocabulary_id", "TARGET_VOCABULARY_ID"), ("target_concept_class_id", "TARGET_CONCEPT_CLASS_ID"),
    ("target_concept_code", "TARGET_CONCEPT_CODE"), ("target_standard_concept", "TARGET_STANDARD_CONCEPT"),
    ("extension_needed", "Extension_Needed"), ("protected_or_open_source", "Protected_or_open-source"),
    ("transferred_to_fairhub_redcap_dataset", "transferred_to_fairhub_REDCap_dataset"),
    ("value_as_concept_id", "value_as_concept_id"), ("qualifier_concept_id", "qualifier_concept_id"),
    ("qualifier_source_value", "qualifier_source_value"),
]
SSSOM_COLS = ["subject_id", "subject_label", "predicate_id", "object_id", "object_label",
              "mapping_justification", "confidence", "subject_source", "object_source",
              "mapping_provider", "mapping_tool", "comment"] + [c for c, _ in SSSOM_EXTRA]


class Dumper(yaml.SafeDumper):
    pass


def _str_rep(dumper, data):
    style = None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


Dumper.add_representer(str, _str_rep)


def ydump(obj, fh, width=None):
    kw = dict(Dumper=Dumper, sort_keys=False, allow_unicode=True, default_flow_style=False)
    if width:
        kw["width"] = width
    yaml.dump(obj, fh, **kw)


def clean(v):
    return (v or "").strip()


def to_int(v):
    try:
        return int(float(v))
    except ValueError:
        return v


def to_float(v):
    try:
        return float(v)
    except ValueError:
        return v


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return [{k: clean(v) for k, v in r.items()} for r in csv.DictReader(fh)]


def build_linkml(rows, src_name, out_dir):
    records = []
    for i, r in enumerate(rows, 1):
        rec = {"mapping_record_id": f"AIREADI_MAPPING_{i:04d}"}
        for col, slot, rng in COLUMNS:
            v = r.get(col, "")
            if not v:
                continue
            rec[slot] = to_int(v) if rng == "integer" else to_float(v) if rng == "float" else v
        records.append(rec)

    enums = {}
    for col, slot, rng in COLUMNS:
        if rng.endswith("Enum"):
            vals = sorted({r.get(col, "") for r in rows if r.get(col, "")})
            enums.setdefault(rng, set()).update(vals)
    enums = {e: {"permissible_values": {v: {} for v in sorted(enums[e])}} for e in ENUM_ORDER if e in enums}

    slots = {
        "mappings": {"range": "MappingRecord", "multivalued": True, "inlined": True,
                     "description": "Collection of source-to-OMOP mapping records."},
        "mapping_record_id": {"range": "string", "identifier": True,
                              "description": "Local identifier assigned to each mapping row during conversion."},
    }
    for col, slot, rng in COLUMNS:
        slots[slot] = {"range": rng, "description": f"Column imported from source CSV column `{col}`.",
                       "annotations": {"source_column": col}}
    schema = {
        "id": "https://w3id.org/ai-readi/redcap-value-set-mapping",
        "name": "ai_readi_redcap_value_set_mapping",
        "title": "AI-READI REDCap Value Set Mapping Schema",
        "description": f"LinkML schema generated from {src_name}. It represents source REDCap variables/question-response "
                       "values mapped to OMOP target concepts and related mapping metadata.",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "prefixes": {"linkml": "https://w3id.org/linkml/", "ai_readi": "https://w3id.org/ai-readi/",
                     "omop": "https://ohdsi.github.io/CommonDataModel/", "skos": "http://www.w3.org/2004/02/skos/core#"},
        "default_prefix": "ai_readi", "default_range": "string", "imports": ["linkml:types"],
        "classes": {
            "MappingFile": {"tree_root": True, "description": "Container for AI-READI REDCap to OMOP mapping records.",
                            "slots": ["mappings"]},
            "MappingRecord": {"description": "A single source-to-target mapping row from the AI-READI REDCap value set mapping file.",
                              "slots": ["mapping_record_id"] + [s for _, s, _ in COLUMNS]},
        },
        "slots": slots, "enums": enums,
    }
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "ai_readi_redcap_value_set_mapping_schema.yaml"), "w", encoding="utf-8") as fh:
        ydump(schema, fh, width=120)
    with open(os.path.join(out_dir, "ai_readi_redcap_value_set_mapping_data.yaml"), "w", encoding="utf-8") as fh:
        ydump({"mappings": records}, fh, width=120)

    def top(col, n=10):
        c = Counter(r.get(col, "") or "[blank]" for r in rows)
        return "\n".join(f"- {k}: {v}" for k, v in c.most_common(n))
    summary = (f"# AI-READI REDCap Value Set Mapping LinkML Conversion Summary\n\n"
               f"- Source file: `{src_name}`\n- Rows converted: {len(rows)}\n- Source columns: {len(COLUMNS)}\n\n"
               "## Generated files\n"
               "- `ai_readi_redcap_value_set_mapping_schema.yaml`: LinkML schema for the mapping table.\n"
               "- `ai_readi_redcap_value_set_mapping_data.yaml`: YAML instance data conforming to the schema container.\n\n"
               "## Top counts\n"
               f"### FORM_NAME\n{top('FORM_NAME')}\n\n### TARGET_DOMAIN_ID\n{top('TARGET_DOMAIN_ID', 50)}\n\n"
               f"### TARGET_VOCABULARY_ID\n{top('TARGET_VOCABULARY_ID', 50)}\n\n### PREDICATE_ID\n{top('PREDICATE_ID', 50)}\n\n"
               f"### Extension_Needed\n{top('Extension_Needed', 50)}\n")
    with open(os.path.join(out_dir, "ai_readi_redcap_value_set_mapping_summary.md"), "w", encoding="utf-8") as fh:
        fh.write(summary)
    return records


def _id_part(s):
    """Make a CURIE-safe identifier component: non [A-Za-z0-9_-] -> '_', collapse, trim."""
    s = re.sub(r"[^A-Za-z0-9_\-]", "_", s or "")
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "missing"


def subject_id(r, i):
    """AIREADI_REDCAP:<FORM_NAME>.<SRC_CODE | FIELD_ID | field_<FIELD_ID_NUM> | row<n>>[.<SRC_CODE_ID>]"""
    if r.get("SRC_CODE"):
        local = r["SRC_CODE"]
    elif r.get("FIELD_ID"):
        local = r["FIELD_ID"]
    elif r.get("FIELD_ID_NUM"):
        local = f"field_{r['FIELD_ID_NUM']}"
    else:
        local = f"row{i}"
    parts = [r.get("FORM_NAME", ""), local]
    if r.get("SRC_CODE_ID"):
        parts.append(r["SRC_CODE_ID"])
    return "AIREADI_REDCAP:" + ".".join(_id_part(p) for p in parts)


def build_sssom(rows, src_name, out_dir, mapping_date):
    os.makedirs(out_dir, exist_ok=True)
    included, incomplete = [], []
    for i, r in enumerate(rows, 2):
        if not r.get("TARGET_CONCEPT_ID") or not r.get("PREDICATE_ID"):
            incomplete.append(r)
            continue
        out = {
            "subject_id": subject_id(r, i),
            "subject_label": r.get("SRC_CD_DESCRIPTION", ""),
            "predicate_id": r["PREDICATE_ID"],
            "object_id": f"OMOP:{to_int(r['TARGET_CONCEPT_ID'])}",
            "object_label": r.get("TARGET_CONCEPT_NAME", ""),
            "mapping_justification": "semapv:ManualMappingCuration",
            "confidence": r.get("CONFIDENCE", ""),
            "subject_source": "AI-READI REDCap",
            "object_source": r.get("TARGET_VOCABULARY_ID", ""),
            "mapping_provider": "AI-READI",
            "mapping_tool": "manual_curation",
            "comment": r.get("MODIFIER", ""),
        }
        for c, src in SSSOM_EXTRA:
            out[c] = r.get(src, "")
        included.append(out)
    with open(os.path.join(out_dir, "ai_readi_redcap_value_set_mapping.sssom.tsv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=SSSOM_COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(included)
    with open(os.path.join(out_dir, "ai_readi_redcap_value_set_mapping_sssom_incomplete_rows.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(incomplete)
    meta = {
        "mapping_set_id": "https://w3id.org/ai-readi/mapping/redcap-to-omop",
        "mapping_set_title": "AI-READI REDCap value set mappings to OMOP concepts",
        "mapping_set_description": "SSSOM representation generated from the AI-READI REDCap value set mapping file. "
                                   "Subject identifiers represent AI-READI REDCap source variables/response options; "
                                   "object identifiers represent OMOP concept_id targets.",
        "license": "https://opensource.org/licenses/MIT",
        "creator_id": ["AI-READI"],
        "mapping_provider": "AI-READI",
        "mapping_tool": "manual_curation",
        "curie_map": {"AIREADI_REDCAP": "https://w3id.org/ai-readi/redcap/",
                      "OMOP": "https://athena.ohdsi.org/search-terms/terms/",
                      "skos": "http://www.w3.org/2004/02/skos/core#",
                      "semapv": "https://w3id.org/semapv/vocab/"},
        "subject_source": "AI-READI REDCap",
        "object_source": "OMOP Standardized Vocabularies",
        "mapping_date": mapping_date,
    }
    with open(os.path.join(out_dir, "ai_readi_redcap_value_set_mapping.sssom.yaml"), "w", encoding="utf-8") as fh:
        ydump(meta, fh)
    readme = f"""# AI-READI REDCap Value Set Mapping — SSSOM Representation

Generated from `{src_name}` with `generate_linkml_sssom.py`.

## Files

- `ai_readi_redcap_value_set_mapping.sssom.tsv` — SSSOM-style mapping table.
- `ai_readi_redcap_value_set_mapping.sssom.yaml` — SSSOM metadata file with CURIE prefixes.
- `ai_readi_redcap_value_set_mapping_sssom_incomplete_rows.csv` — rows not included in the SSSOM TSV because they were missing `TARGET_CONCEPT_ID` or `PREDICATE_ID`.

## Row counts

- Source rows: {len(rows):,}
- Rows included in SSSOM TSV: {len(included):,}
- Rows excluded as incomplete for SSSOM: {len(incomplete):,}

## Identifier conventions

- `subject_id`: generated as `AIREADI_REDCAP:<FORM_NAME>.<SRC_CODE>[.<SRC_CODE_ID>]` when source codes were available. When source codes were missing, the generator used `FIELD_ID`, `FIELD_ID_NUM`, or the source row number.
- `object_id`: generated as `OMOP:<TARGET_CONCEPT_ID>`.
- `predicate_id`: taken directly from the source mapping file, such as `skos:exactMatch` or `skos:closeMatch`.
- `mapping_justification`: set to `semapv:ManualMappingCuration` for all included rows.

## Notes

The TSV includes both standard SSSOM columns and AI-READI/OMOP-specific extension columns such as `target_domain_id`, `target_vocabulary_id`, `value_as_concept_id`, and `qualifier_concept_id`. These extension columns preserve information needed for OMOP ETL and downstream review.

Row counts here are rows in the mapping file. Manuscript counts (e.g., 1,900 mapped elements) additionally exclude REDCap survey timestamps; see `manuscript-tvst2026/README.md`.
"""
    with open(os.path.join(out_dir, "ai_readi_redcap_value_set_mapping_sssom_README.md"), "w", encoding="utf-8") as fh:
        fh.write(readme)
    return included, incomplete


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mapping_csv")
    ap.add_argument("repo_root")
    ap.add_argument("--mapping-date", default=dt.date.today().isoformat())
    a = ap.parse_args()
    rows = read_rows(a.mapping_csv)
    src = os.path.basename(a.mapping_csv)
    base = os.path.join(a.repo_root, "redCapDataDictionaryWithExtension")
    recs = build_linkml(rows, src, os.path.join(base, "linkml"))
    inc, exc = build_sssom(rows, src, os.path.join(base, "sssom"), a.mapping_date)
    print(f"LinkML records: {len(recs)}; SSSOM rows: {len(inc)}; incomplete: {len(exc)}")


if __name__ == "__main__":
    main()
