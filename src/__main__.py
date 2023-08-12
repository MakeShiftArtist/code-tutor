import discord
import os
import commands.help as help
from dotenv import load_dotenv

import database

load_dotenv()  # take environment variables from .env.
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

bot.add_application_command(help.help)

bot.run(os.getenv("DISCORD_TOKEN"))  # Use DI