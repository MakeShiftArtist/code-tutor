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

CREATE TABLE guild.moderation (
    id BIGINT NOT NULL UNIQUE,
    max_warnings_before_kick SMALLINT,
    max_warnings_before_ban SMALLINT,
    allow_appeals BOOLEAN DEFAULT FALSE,
    appeals_channel_id BIGINT
);

CREATE TABLE guild.warnings (
    id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    warning_type VARCHAR(10), -- ban, kick, warn
    reason VARCHAR,
    created_at TIMESTAMPTZ DEFAULT Now()
);

CREATE TABLE guild.appeals (
    id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    reason VARCHAR NOT NULL,
    created_at TIMESTAMPTZ DEFAULT Now(),
    UNIQUE(id, user_id) -- Only one submission per user, per guild.
)