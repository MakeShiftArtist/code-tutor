import os
import sqlite3
import dotenv

dotenv.load_dotenv()

URL = os.getenv("DATABASE_URL")

connection = sqlite3.connect("code-tutor.sqlite")

existing_guilds = []


class Guild:
    def __init__(self, guild_id: int, connection=connection) -> None:
        self.guild_id = guild_id
        self.con = connection
        pass

    def exists(self) -> bool:
        if self.guild_id in existing_guilds:
            return True
        else:
            cursor = self.con.cursor()
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM guild_settings WHERE guild_id = ?)",
                (self.guild_id,),
            )
            result = cursor.fetchone()
            value = result[0] if result else None
            if value:
                existing_guilds.append(value)
                return True
            return False

    def create(self):
        cursor = self.con.cursor()
        cursor.execute(
            "INSERT INTO guild_settings (guild_id) VALUES (?)", (self.guild_id,)
        )
        self.con.commit()

    def set_question_of_the_day_channel(self, channel_id=None):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "UPDATE guild_settings SET question_of_the_day_channel_id=? WHERE guild_id=?;",
            (channel_id, self.guild_id),
        )
        self.con.commit()

    def get_question_of_the_day_channel(self):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "SELECT question_of_the_day_channel_id FROM guild_settings WHERE guild_id=?;",
            (self.guild_id,),
        )

    def get_embed(self, name: str):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "SELECT command_embed FROM guild_embeds WHERE command_name = ?;",
            (name,),
        )
        value = cursor.fetchone()
        return value[0] if value else value

    def get_embed_names(self):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "SELECT command_name FROM guild_embeds WHERE guild_id = ?", (self.guild_id,)
        )
        value = cursor.fetchall()
        return [v[0] for v in value] if value else value

    def delete_embed(self, name: str):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "DELETE FROM guild_embeds WHERE guild_id=? AND command_name=?;",
            (self.guild_id, name),
        )
        self.con.commit()

    def create_embed(self, name, embed):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "INSERT INTO guild_embeds (guild_id, command_name, command_embed) VALUES (?, ?, ?)",
            (self.guild_id, name, embed),
        )
        self.con.commit()

    def set_appeals_channel(self, channel_id=None):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "UPDATE guild_settings SET appeals_channel_id = ? WHERE guild_id = ?;",
            (channel_id, self.guild_id),
        )
        self.con.commit()

    def get_appeals_channel(self):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "SELECT appeals_channel_id FROM guild_settings WHERE guild_id=?;",
            (self.guild_id,),
        )
        value = cursor.fetchone()
        return value[0] if value else value

    def warn_user(self, user_id, reason):

        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "INSERT INTO guild_warnings (guild_id, user_id, reason) VALUES (?, ?, ?, ?)",
            (self.guild_id, user_id, reason),
        )
        self.con.commit()

    def get_warnings(self, user_id):
        if not self.exists():
            self.create()

        cursor = self.con.cursor()
        cursor.execute(
            "SELECT user_id, reason, created_at FROM guild_warnings WHERE guild_id = ? AND user_id = ?;",
            (str(self.guild_id), str(user_id)),
        )
        return cursor.fetchall()
