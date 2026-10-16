"""Run count_concept_map.sql (working version) with DuckDB and print each result.

Counts the working mapping file
redCapDataDictionaryWithExtension/value-set-mapping-common/_ai_readi_redcap_value_set_mapping_common.csv.
For the frozen TVST 2026 manuscript counts, use manuscript-tvst2026/run_counts.py instead.

Usage (from any folder):
    pip install duckdb
    python redCapDataDictionaryWithExtension/scripts/run_counts.py
"""
import os
import sys
from pathlib import Path

import duckdb

 
# Windows consoles default to cp1252, which cannot print DuckDB's box-drawing table borders.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sql_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().with_name("count_concept_map.sql")
# The SQL reads the mapping CSV by a path relative to the repository root.
os.chdir(Path(__file__).resolve().parents[2])
con = duckdb.connect()

for stmt in duckdb.extract_statements(sql_path.read_text(encoding="utf-8")):
    rel = con.sql(stmt.query)
    if rel is not None:          # SELECT statements return a relation; CREATE/load statements return None
        rel.show(max_width=200)
