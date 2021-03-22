-- Create tables for user & class management inside a transaction block
BEGIN;

CREATE TABLE users (
    id serial PRIMARY KEY,
    username text UNIQUE NOT NULL,
    role text NOT NULL,
    name text,
    light_mode boolean NOT NULL DEFAULT TRUE
);

CREATE TABLE classes (
  id serial PRIMARY KEY,
  name text NOT NULL,
  class_code text NOT NULL,
  semester text NOT NULL,
  token text
);

CREATE TABLE users_classes (
  user_id integer NOT NULL,
  class_id integer NOT NULL
);

COMMIT;

-- Initial seed data goes here, e.g. prefilled classes data