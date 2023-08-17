
from dotenv import load_dotenv
from discord import SlashCommandGroup
from os import getenv, execv
from sys import exit, executable, argv
from utils.embeds import SuccessEmbed, ErrorEmbed

load_dotenv()

developer_ids = [int(i) for i in getenv("DEVELOPER_IDS").split(",")]

developer = SlashCommandGroup("dev", "Developer only commands.")

@developer.command()
async def shutdown(ctx):
    if ctx.author.id not in developer_ids:
        await ctx.respond(embed=ErrorEmbed(description="Must be an developer to use this feature."))
        return
    await ctx.respond(embed=SuccessEmbed(description="Shutting down..."))
    exit()

@developer.command()
async def restart(ctx):
    if ctx.author.id not in developer_ids:
        return
    await ctx.respond(embed=SuccessEmbed(description="Attempting restart..."))
    execv(executable, ['python'] + argv)

