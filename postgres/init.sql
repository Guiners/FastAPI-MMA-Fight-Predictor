DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'mma_db'
   ) THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE mma_db');
   END IF;
END
$$;

DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin') THEN
      CREATE ROLE admin LOGIN PASSWORD 'test_password';
   END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE mma_db TO admin;