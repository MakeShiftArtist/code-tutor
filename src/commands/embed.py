from discord import SlashCommandGroup, Embed, Color, File
from database import create_command, get_command, get_commands, delete_command
from json import loads
from dotenv import load_dotenv
from os import getenv
import discord
from traceback import format_exc
import discord.utils as utils
from io import BytesIO

load_dotenv()

embed = SlashCommandGroup("embed", "Manage custom guild commands")

@embed.command()
async def create(ctx, command_name: str, embed_json: str):
    if len(command_name) > 10:
        await ctx.respond(embed=Embed(
            description=f"Command name must be shorter than 10 characters. You submitted a command name with a length of {len(command_name)}.",
            color=Color.red()
        ))
        return
    elif " " in command_name:
        await ctx.respond(embed=Embed(
            description=f"Your command name may not include spaces.", color=Color.red()
        ))
        return
    create_command(ctx.guild_id, command_name, embed_json)
    e = Embed(
        description=f"{command_name} created.",
        color=Color.green()
    )
    await ctx.respond(embed=e)

@embed.command()
async def get(ctx, command_name: str):
    command = get_command(ctx.guild_id, command_name)
    if not command:
        await ctx.respond(embed=Embed(
            description=f"`{command_name}` not found. Try creating it!",
            color=Color.red()
        ))
        return
    await ctx.respond(embed=Embed.from_dict(loads(command)))

@embed.command()
async def delete(ctx, command_name):
    delete_command(ctx.guild_id, command_name)
    await ctx.respond(embed=Embed(
        description=f"{command_name} deleted",
        color=Color.green()
    ))
    return


help_file_1 = File(BytesIO(open("./src/dump/00.jpg", "rb").read()), "help_file_1.jpg")
help_file_2 = File(BytesIO(open("./src/dump/01.jpg", "rb").read()), "help_file_2.jpg")
@embed.command()
async def help(ctx: discord.ApplicationContext):

    embed_command_id = utils.get(ctx.bot.commands, name="embed").id

    msg = f"Create a new command: </embed create:{embed_command_id}>\n" + \
          f"Get a command: </embed get:{embed_command_id}>\n" + \
          f"Delete a command: </embed delete:{embed_command_id}>\n" + \
          f"List all commands: </embed list:{embed_command_id}>\n" + \
          "\nWhen creating a new command, you are required to submit the json of your command embed. " + \
          "The easiest way to do this is to visit [message.style](https://message.style/app/) and create one, it has a nice user interface for all kinds of discord json formatting. " + \
          "Keep in mind, [message.style](https://message.style/app/) is used for more than just embeds, so you will need to select ONLY the embed part of the `JSON` to submit when you create a custom command." 
    
    await ctx.respond(embed=Embed(
        title="Guild Embed Command Help Menu",
        description=msg,
        color=Color.green()
    ), ephemeral=True, files=[help_file_1, help_file_2])

@embed.command()
async def list(ctx):
    commands = get_commands(ctx.guild_id)
    if commands:
        await ctx.respond(embed=Embed(
            title="Custom Commands (Guild)",
            description="\n".join(commands),
            color=Color.green()
        ))
    else:
        await ctx.respond(embed=Embed(
            description="No custom commands found for your guild. Try `/embed create` !",
            color=Color.red()
        )) 

#@custom_command.error
#async def on_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
#    await ctx.respond("Error processing command.")
#    channel = ctx.bot.get_channel(int(getenv("ERROR_LOG_CHANNEL")))
#    await channel.send(embed=Embed(
#        description=f"Error occured while processing {ctx.user.display_name}'s command.\n\nError:\n```{format_exc()}```"
#    ))
    