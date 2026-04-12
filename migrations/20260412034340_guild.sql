-- Add migration script here


-- Settings for specific guilds
CREATE TABLE IF NOT EXISTS guild_settings (
    guild_id TEXT PRIMARY KEY,
    appeals_channel_id TEXT,
    question_of_the_day_channel_id TEXT
);

-- Stored embeds for custom commands
CREATE TABLE IF NOT EXISTS guild_embeds (
    guild_id TEXT NOT NULL,
    command_name TEXT NOT NULL,
    command_embed TEXT NOT NULL,
    PRIMARY KEY (guild_id, command_name)
);

-- User warnings
CREATE TABLE IF NOT EXISTS guild_warnings (
    warning_id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for performance
CREATE INDEX IF NOT EXISTS idx_warnings_guild_user ON guild_warnings(guild_id, user_id);
