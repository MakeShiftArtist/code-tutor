import discord
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")


bot.run(os.getenv("DISCORD_TOKEN"))  # Use DISCORD_TOKEN from .env
