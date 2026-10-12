"""Run count_mapping_concepts.sql with the DuckDB Python package and print each result.

Usage (from the folder containing this script, the SQL file and the mapping CSV):
    pip install duckdb
    python run_counts.py
"""
import sys
from pathlib import Path

import duckdb

sql_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("count_mapping_concepts.sql")
con = duckdb.connect()

for stmt in duckdb.extract_statements(sql_path.read_text(encoding="utf-8")):
    rel = con.sql(stmt.query)
    if rel is not None:          # SELECT statements return a relation; CREATE/load statements return None
        rel.show(max_width=200)
