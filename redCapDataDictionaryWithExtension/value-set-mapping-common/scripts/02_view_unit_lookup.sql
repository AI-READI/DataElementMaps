-- =============================================================================
-- 02_view_unit_lookup.sql
-- AI-READI concept map: review the unit_lookup table
--
-- Requires unit_lookup (01_create_unit_lookup.sql). Dialect: Databricks / Spark SQL.
-- =============================================================================

-- Row counts by key type. v1.6: field 88, string 25.
SELECT key_type, COUNT(*) AS n
FROM unit_lookup
GROUP BY key_type
ORDER BY key_type;

-- Lookup by measurement field name (88 rows).
SELECT lookup_key AS field_name, unit_concept_id, unit_source_value
FROM unit_lookup
WHERE key_type = 'field'
ORDER BY lookup_key;

-- Lookup by unit text (25 rows).
SELECT lookup_key AS unit_string, unit_concept_id
FROM unit_lookup
WHERE key_type = 'string'
ORDER BY lookup_key;

-- Check: must return 0 rows (one row per key, so joins never add rows).
SELECT key_type, lookup_key, COUNT(*) AS n
FROM unit_lookup
GROUP BY key_type, lookup_key
HAVING COUNT(*) > 1;
