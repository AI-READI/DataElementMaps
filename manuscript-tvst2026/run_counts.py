"""Run count_concept_map.sql with the DuckDB Python package and print each result.

Usage (from the folder containing this script, the SQL file and the mapping CSV):
    pip install duckdb
    python run_counts.py
"""
import sys
from pathlib import Path

import duckdb

 
# Windows consoles default to cp1252, which cannot print DuckDB's box-drawing table borders.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sql_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("count_concept_map.sql")
con = duckdb.connect()

for stmt in duckdb.extract_statements(sql_path.read_text(encoding="utf-8")):
    rel = con.sql(stmt.query)
    if rel is not None:          # SELECT statements return a relation; CREATE/load statements return None
        rel.show(max_width=200)
