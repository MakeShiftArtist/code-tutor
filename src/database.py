import psycopg2, os, dotenv

dotenv.load_dotenv()

connection = psycopg2.connect(
    database="devdevdb",
    host=os.getenv("POSTGRES_HOST"),
    user=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT")
)

existing_guilds = []

def does_guild_exist(guild_id) -> bool:
    if guild_id in existing_guilds:
        return True
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM guild.consent WHERE id = %s;", (guild_id,))
        result = cursor.fetchone()
        value = result[0] if result else None
        if value:
            existing_guilds.append(value)
            return True
        return False
    

def create_guild(guild_id) -> None:
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO guild.consent (id) VALUES (%s)", (guild_id,))
        cursor.execute("INSERT INTO guild.moderation (id) VALUES (%s)", (guild_id))
        connection.commit()

def opt_qotd(guild_id, channel_id=None) -> None:
    if not does_guild_exist(guild_id):
        create_guild(guild_id)

    with connection.cursor() as cursor:
        cursor.execute("UPDATE guild.consent SET question_of_the_day = %s WHERE id = %s", (channel_id, guild_id))
        connection.commit()

def opt_in_error_forwarding(guild_id, forward_errors=True):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)

    with connection.cursor() as cursor:
        cursor.execute("UPDATE guild.consent SET error_forwarding = %s WHERE id = %s", (forward_errors, guild_id))
        connection.commit()

def get_command(guild_id, command_name):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)

    with connection.cursor() as cursor:
        cursor.execute("SELECT command_embed FROM guild.commands WHERE id = %s AND command_name = %s", (guild_id, command_name))
        value = cursor.fetchone()
        return value[0] if value else value

def get_commands(guild_id):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT command_name FROM guild.commands WHERE id = %s", (guild_id,))
        value = cursor.fetchall()
        return [v[0] for v in value] if value else value

def delete_command(guild_id, command_name):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM guild.commands WHERE id=%s AND command_name=%s;", (guild_id, command_name))
        connection.commit()

def create_command(guild_id, command_name, command_embed):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)

    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO guild.commands (id, command_name, command_embed) VALUES (%s, %s, %s)", (guild_id, command_name, command_embed))
        connection.commit()

def set_max_warnings_before_kick(guild_id, max_warnings: int = None):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)

    with connection.cursor() as cursor:
        cursor.execute("UPDATE guild.moderation SET max_warnings_before_kick=%s WHERE id = %s;", (max_warnings, guild_id))
        connection.commit()

def set_max_warnings_before_ban(guild_id, max_warnings: int = None):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)
    
    with connection.cursor() as cursor:
        cursor.execute("UPDATE guild.moderation SET max_warnings_before_ban=%s WHERE id=%s;", (max_warnings, guild_id))
        connection.commit()

def allow_appeals(guild_id, allow: bool = False):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)
    
    with connection.cursor() as cursor:
        cursor.execute("UPDATE guild.moderation SET allow_appeals = %s WHERE id=%s;", (allow, guild_id))
        connection.commit()

def set_appeals_channel_id(guild_id, channel_id: int = None):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)
    
    with connection.cursor() as cursor:
        cursor.execute("UPDATE guild.moderation SET appeals_channel_id = %s WHERE id=%s;")
        connection.commit()

def warn_user(guild_id, user_id, warning_type, reason):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)

    if warning_type not in ["warn", "kick", "ban"]:
        raise Exception("Warning type must be one of: warn, ban, kick")
    
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO guild.warnings (id, user_id, warning,_type reason) VALUES (%s, %s, %s, %s)", (guild_id, user_id, warning_type, reason))
        connection.commit()

def get_user_warnings(guild_id, user_id):
    if not does_guild_exist(guild_id):
        create_guild(guild_id)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT (*) FROM guild.warnings WHERE id = %s AND user_id = %s;", (guild_id, user_id))
        return cursor.fetchall()