"""Identify which concept map release a mapping CSV came from, or write the map metadata file.

1. Identify (for a mapping file that came back from an ETL run, possibly edited or re-saved):

    python redCapDataDictionaryWithExtension/scripts/identify_map_version.py some_mapping_file.csv

   Compares the file with the mapping file of every git tag in this repository and reports the
   closest release, then lists the rows that differ from it. The comparison ignores row order and
   undoes the usual spreadsheet re-formatting (long codes shown in scientific notation, ranges
   such as "3-4" turned into dates), so only real content edits are reported. Which variant is
   compared (common, map2omop or open-source public) is chosen by the best match.

2. Write the metadata file (release step, after the mapping files are final):

    python redCapDataDictionaryWithExtension/scripts/identify_map_version.py --write-metadata v1.8.4 \\
        --release v1.8.6 --date 2026-10-29

   Writes value-set-mapping-common/ai_readi_redcap_value_set_mapping.metadata.json with the map
   version (the release that last changed the mapping content), the repository release, and the
   row count and MD5 of each mapping file.

Run from anywhere inside a clone of the repository (needs git and the tags: git fetch --tags).
Standard library only.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MAP_DIR = "redCapDataDictionaryWithExtension/value-set-mapping-common/"
VARIANTS = {
    "common": "_ai_readi_redcap_value_set_mapping_common.csv",
    "map2omop": "_ai_readi_redcap_value_set_mapping_common_map2omop.csv",
    "public": "_ai_readi_redcap_value_set_mapping_map2omop_open_source_public_version.csv",
}
KEY_COLS = ["FORM_NAME", "FIELD_ID", "SRC_CODE", "temp_Question_or_Answer", "TARGET_DOMAIN_ID"]
MON = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], stderr=subprocess.DEVNULL)


def norm(v):
    """Undo spreadsheet re-formatting so it does not count as a content change."""
    v = (v or "").strip()
    m = re.fullmatch(r"(\d+)-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", v)
    if m:
        return f"{MON[m.group(2)]}-{m.group(1)}"
    m = re.fullmatch(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d+)", v)
    if m:
        return f"{MON[m.group(1)]}-{m.group(2)}"
    if re.fullmatch(r"\d(\.\d+)?E\+\d+", v, re.I) or re.fullmatch(r"\d{12,}", v):
        return "NUM:%.5e" % float(v)          # long code, compared at spreadsheet precision
    return v


def read_rows(text):
    rows = list(csv.DictReader(io.StringIO(text.lstrip("﻿"))))
    return rows, (list(rows[0].keys()) if rows else [])


def as_counter(rows, cols):
    return collections.Counter(tuple(norm(r.get(c, "")) for c in cols) for r in rows)


def tags():
    out = git("tag", "-l").decode().split()
    return [t for t in out if t.startswith("v")]


def identify(path):
    data = Path(path).read_bytes()
    text = data.decode("utf-8-sig", errors="replace")
    rows, cols = read_rows(text)
    if not rows:
        sys.exit("No data rows in " + path)
    md5 = hashlib.md5(data).hexdigest()
    print(f"File: {path}\n  rows {len(rows)}, columns {len(cols)}, MD5 {md5}\n")

    results = []
    for t in tags():
        for v, f in VARIANTS.items():
            try:
                tdata = git("show", f"{t}:{MAP_DIR}{f}")
            except subprocess.CalledProcessError:
                continue
            trows, tcols = read_rows(tdata.decode("utf-8-sig"))
            common_cols = [c for c in tcols if c in cols]
            S, T = as_counter(rows, common_cols), as_counter(trows, common_cols)
            only_file, only_tag = sum((S - T).values()), sum((T - S).values())
            exact = hashlib.md5(tdata).hexdigest() == md5
            results.append((0 if exact else only_file + only_tag, t, v, len(trows), only_file, only_tag,
                            exact, common_cols, trows))
    if not results:
        sys.exit("No tagged mapping files found (run: git fetch --tags).")
    results.sort(key=lambda r: (r[0], r[1]))

    print("Closest releases (rows differing, ignoring order and spreadsheet re-formatting):")
    print(f"  {'tag':<12}{'variant':<10}{'rows':>6}{'only in file':>14}{'only in tag':>13}  exact")
    for r in results[:6]:
        print(f"  {r[1]:<12}{r[2]:<10}{r[3]:>6}{r[4]:>14}{r[5]:>13}  {'yes' if r[6] else ''}")

    best = results[0]
    _, tag, variant, _, n_file, n_tag, exact, common_cols, trows = best
    print(f"\nBest match: {tag} ({variant})" + (" - identical file." if exact else ""))
    if exact or (n_file == 0 and n_tag == 0):
        if not exact:
            print("Content identical; the bytes differ only by row order, line endings or re-formatting.")
        return

    # Report differences by row key
    def keyed(rs):
        d = collections.defaultdict(list)
        for r in rs:
            d[tuple((r.get(c) or "").strip() for c in KEY_COLS)].append(r)
        return d
    F, T = keyed(rows), keyed(trows)
    changed, added, removed = [], [], []
    for k in sorted(set(F) | set(T)):
        a, b = F.get(k, []), T.get(k, [])
        if a and b:
            for ra, rb in zip(a, b):
                diff = [c for c in common_cols if norm(ra.get(c)) != norm(rb.get(c))]
                if diff:
                    changed.append((k, [(c, rb.get(c, ""), ra.get(c, "")) for c in diff]))
        elif a:
            added.extend((k, r) for r in a)
        else:
            removed.extend((k, r) for r in b)

    # Rows whose key itself was edited show up as one added + one removed; pair them by FIELD_ID_NUM
    by_num = {(r.get("FIELD_ID_NUM") or "").strip() + "|" + (r.get("SRC_CD_DESCRIPTION") or "").strip(): (k, r)
              for k, r in removed}
    still_added = []
    for k, r in added:
        n = (r.get("FIELD_ID_NUM") or "").strip() + "|" + (r.get("SRC_CD_DESCRIPTION") or "").strip()
        if n in by_num:
            k2, r2 = by_num.pop(n)
            diff = [c for c in common_cols if norm(r.get(c)) != norm(r2.get(c))]
            changed.append((k2, [(c, r2.get(c, ""), r.get(c, "")) for c in diff]))
        else:
            still_added.append((k, r))
    removed = list(by_num.values())

    print(f"\nDifferences from {tag}: {len(changed)} rows edited, {len(still_added)} rows only in the file, "
          f"{len(removed)} rows only in the release.")
    cols_changed = collections.Counter(c for _, d in changed for c, _, _ in d)
    if cols_changed:
        print("  Edited columns: " + ", ".join(f"{c} ({n})" for c, n in cols_changed.most_common()))
    for k, d in changed[:60]:
        print(f"  ~ {k[1] or k[2]} [{k[3]}]: " + "; ".join(f"{c}: {o!r} -> {n!r}" for c, o, n in d))
    for k, r in still_added[:30]:
        print(f"  + {k[1] or k[2]} [{k[3]}] -> {r.get('TARGET_CONCEPT_ID')} {r.get('TARGET_CONCEPT_NAME')}")
    for k, r in removed[:30]:
        print(f"  - {k[1] or k[2]} [{k[3]}] -> {r.get('TARGET_CONCEPT_ID')} {r.get('TARGET_CONCEPT_NAME')}")

    # Spreadsheet re-formatting found in the file (informational)
    sci = sum(1 for r in rows for v in r.values() if v and re.fullmatch(r"\d(\.\d+)?E\+\d+", v.strip(), re.I))
    dates = sum(1 for r in rows for v in r.values()
                if v and re.fullmatch(r"\d+-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)|"
                                      r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d+", v.strip()))
    if sci or dates:
        print(f"\nSpreadsheet re-formatting in the file: {sci} values in scientific notation (digits lost), "
              f"{dates} values turned into dates. Open the CSV as text, not in Excel.")


def write_metadata(map_version, release, date):
    files = {}
    for v, f in VARIANTS.items():
        p = ROOT / MAP_DIR / f
        data = p.read_bytes()
        rows, _ = read_rows(data.decode("utf-8-sig"))
        files[f] = {"variant": v, "rows": len(rows), "md5": hashlib.md5(data).hexdigest()}
    meta = {
        "name": "AI-READI REDCap to OMOP concept map",
        "map_version": map_version,
        "map_version_note": "Release that last changed the mapping content; later releases may change only scripts or documentation.",
        "repository_release": release,
        "date": date,
        "repository": "https://github.com/AI-READI/DataElementMaps",
        "changelog": f"https://github.com/AI-READI/DataElementMaps/blob/{release}/CHANGELOG.md",
        "files": files,
        "record_in_omop": {
            "cdm_source.source_description": f"AI-READI concept map {map_version} (common file MD5 "
                                             f"{files[VARIANTS['common']]['md5']})",
            "metadata.name": "AI-READI concept map version",
            "metadata.value_as_string": map_version,
        },
        "check": "python redCapDataDictionaryWithExtension/scripts/identify_map_version.py <mapping file>",
    }
    out = ROOT / MAP_DIR / "ai_readi_redcap_value_set_mapping.metadata.json"
    out.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print("Wrote", out.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="?", help="mapping CSV to identify")
    ap.add_argument("--write-metadata", metavar="MAP_VERSION", help="write the metadata file for this map version")
    ap.add_argument("--release", help="repository release the metadata file ships in (default: MAP_VERSION)")
    ap.add_argument("--date", help="release date, YYYY-MM-DD")
    a = ap.parse_args()
    if a.write_metadata:
        write_metadata(a.write_metadata, a.release or a.write_metadata, a.date or "")
    elif a.csv:
        identify(a.csv)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
