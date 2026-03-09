-- 001_create_tables.down.sql

BEGIN;

DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS users;

DROP EXTENSION IF EXISTS "pgcrypto";

COMMIT;
