import discord
import os
import commands.help as help
import commands.developer as developer
import commands.embed as embed
from dotenv import load_dotenv
from json import dumps
from traceback import format_exception
import commands.compiler as compiler
from discord import Bot, Intents

import database

load_dotenv()  # take environment variables from .env.

intents = Intents.default()
intents.message_content = True

bot = Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error):
    await ctx.respond(embed=discord.Embed(
        description=f"Error processing command...",
        color=discord.Color.red()
    ))
    print(error)
    e = format_exception(error)
    channel = ctx.bot.get_channel(int(os.getenv("ERROR_LOG_CHANNEL")))
    arguments = dumps(ctx.selected_options, indent=4) if ctx.selected_options else ctx.selected_options
    traceback = "\n".join([f"```\n{i}```" for i in e])
    await channel.send(embed=discord.Embed(
        description=f"Error occurred while processing {ctx.user.display_name}'s command\n\nCommand Name:\n/{ctx.command.qualified_name}\n\nArguments:\n```json\n{arguments}```\n\nError:\n{traceback}"
    ))

bot.add_application_command(developer.shutdown)
bot.add_application_command(help.help)
bot.add_application_command(embed.embed)
bot.add_application_command(compiler.compile)

bot.run(os.getenv("DISCORD_TOKEN"))  # Use DI