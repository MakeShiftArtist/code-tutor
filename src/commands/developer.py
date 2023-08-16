from discord.ext import commands
from dotenv import load_dotenv
from discord import Embed, Color, SlashCommandGroup
from os import getenv
from sys import exit

load_dotenv()

developer_ids = [int(i) for i in getenv("DEVELOPER_IDS").split(",")]

developer = SlashCommandGroup("dev", "Developer only commands.")

@commands.slash_command()
async def shutdown(ctx):
    if ctx.author.id not in developer_ids:
        await ctx.respond(embed=Embed(
            description="Must be an admin to use this feature.",
            color=Color.red()
        ))
        return
    await ctx.respond(embed=Embed(
        description="Shutting down...",
        color=Color.green()
    ))
    exit()