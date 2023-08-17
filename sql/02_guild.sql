\connect devdevdb;

CREATE SCHEMA guild;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE guild.settings (
    id BIGINT NOT NULL UNIQUE,
    appeals_channel_id BIGINT,
    question_of_the_day_channel_id BIGINT,
    appeals_channel_id BIGINT
);

CREATE TABLE guild.embeds (
    id BIGINT NOT NULL,
    command_name VARCHAR NOT NULL,
    command_embed VARCHAR NOT NULL
);

CREATE TABLE guild.warnings (
    id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    reason VARCHAR,
    created_at TIMESTAMPTZ DEFAULT Now()
);