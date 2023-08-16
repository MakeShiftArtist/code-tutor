\connect devdevdb;

CREATE SCHEMA guild;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE guild.information (
    id BIGINT NOT NULL UNIQUE,
    appeals_channel_id BIGINT,
    question_of_the_day_channel_id BIGINT
);

CREATE TABLE guild.embeds (
    id BIGINT NOT NULL,
    command_name VARCHAR NOT NULL,
    command_embed VARCHAR NOT NULL
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