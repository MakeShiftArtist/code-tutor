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
valid_warning_types = ["warn", "kick", "ban"]

class Guild:
    def __init__(self, guild_id: int, connection=connection) -> None:
        self.guild_id = guild_id
        self.con = connection
        pass

    def exists(self) -> bool:
        if self.guild_id in existing_guilds:
            return True
        else:
            with self.con.cursor() as cursor:
                cursor.execute("SELECT id FROM guild.information WHERE id = %s;", (self.guild_id,))
                result = cursor.fetchone()
                value = result[0] if result else None
                if value:
                    existing_guilds.append(value)
                    return True
                return False

    def create(self):
        with self.con.cursor() as cursor:
            cursor.execute("INSERT INTO guild.information (id) VALUES (%s)", (self.guild_id,))
            self.con.commit()

    def question_of_the_day_channel(self, channel_id=None):
        if not self.exists():
            self.create()

        with self.con.cursor() as cursor:
            cursor.execute("UPDATE guild.information SET question_of_the_day_channel_id=%s WHERE id=%s;", (channel_id, self.guild_id))
            self.con.commit()
            
    
    def get_embed(self, name: str):
        if not self.exists():
            self.create()
        
        with self.con.cursor() as cursor:
            cursor.execute("SELECT command_embed FROM guild.embeds WHERE command_name = %s;", (name,))
            value = cursor.fetchone()
            return value[0] if value else value

    def get_embed_names(self):
        if not self.exists():
            self.create()
        
        with self.con.cursor() as cursor:
            cursor.execute("SELECT command_name FROM guild.embeds WHERE id = %s", (self.guild_id,))
            value = cursor.fetchall()
            return [v[0] for v in value] if value else value
        
    def delete_embed(self, name: str):
        if not self.exists():
            self.create()

        with self.con.cursor() as cursor:
            cursor.execute("DELETE FROM guild.embeds WHERE id=%s AND command_name=%s;", (self.guild_id, name))
            self.con.commit()

    def create_embed(self, name, embed):
        if not self.exists():
            self.create()

        with self.con.cursor() as cursor:
            cursor.execute("INSERT INTO guild.embeds (id, command_name, command_embed) VALUES (%s, %s, %s)", (self.guild_id, name, embed))
            self.con.commit()
    
    def set_appeals_channel(self, channel_id=None):
        if not self.exists():
            self.create()
        
        with self.con.cursor() as cursor:
            cursor.execute("UPDATE guild.information SET appeals_channel_id = %s WHERE id = %s;", (channel_id, self.guild_id))
            self.con.commit()
        
    def warn_user(self, user_id, reason, warning_type="warn"):
        if warning_type not in valid_warning_types:
            raise Exception(f"Warning types must be one of: {valid_warning_types}")
        
        if not self.exists():
            self.create()

        with self.con.cursor() as cursor:
            cursor.execute("INSERT INTO guild.warnings (id, user_id, warning_type, reason) VALUES (%s, %s, %s, %s)", (
                self.guild_id,
                user_id,
                warning_type,
                reason
            ))
            self.con.commit()

    def get_warnings(self, user_id):
        if not self.exists():
            self.create()
        
        with self.con.cursor() as cursor:
            cursor.execute("SELECT user_id, warning_type, reason, created_at FROM guild.warnings WHERE id=%s;", (self.guild_id),)
            return cursor.fetchall()
