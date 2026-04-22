from discord import SlashCommandGroup
from os import execv
from sys import exit, executable, argv
from utils.embeds import SuccessEmbed
from discord.ext import commands


developer = SlashCommandGroup("dev", "Developer only commands.")


@developer.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.respond(embed=SuccessEmbed(description="Shutting down..."))
    exit()


@developer.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.respond(embed=SuccessEmbed(description="Attempting restart..."))
    execv(executable, ["python"] + argv)
