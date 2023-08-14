\connect devdevdb;

CREATE SCHEMA guild;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE guild.consent (
    id BIGINT NOT NULL UNIQUE,
    question_of_the_day VARCHAR,
    error_forwarding BOOLEAN
);

CREATE TABLE guild.commands (
    id BIGINT NOT NULL,
    command_name VARCHAR NOT NULL,
    command_embed VARCHAR NOT NULL
);