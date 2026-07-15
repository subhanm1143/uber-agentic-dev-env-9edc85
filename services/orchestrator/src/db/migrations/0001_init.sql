-- Migration 0001: initial schema.
-- Migrations are forward-only; each is wrapped in a transaction so a partial
-- apply never leaves the database half-migrated.
BEGIN;

\i services/orchestrator/src/db/schema.sql

COMMIT;
