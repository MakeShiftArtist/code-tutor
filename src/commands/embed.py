from discord import SlashCommandGroup, Embed, File, Option, AutocompleteContext
from database import connection, Guild
from json import loads
from dotenv import load_dotenv
import discord
from discord.utils import basic_autocomplete, get
from io import BytesIO
from utils.embeds import SuccessEmbed, ErrorEmbed

load_dotenv()

embed = SlashCommandGroup("embed", "Manage custom guild commands")

@embed.command()
async def create(ctx, embed_name: str, embed_json: str):
    if len(embed_name) > 10:
        await ctx.respond(embed=ErrorEmbed(description=f"Embed name must be shorter than 10 characters. You submitted a command name with a length of {len(embed_name)}."))
        return
    elif " " in embed_name:
        await ctx.respond(embed=ErrorEmbed(description=f"Your embed name may not include spaces."))
        return
    
    try: 
        message = await ctx.send(embed=Embed.from_dict(loads(embed_json)))
        await message.delete()
    except:
        await ctx.respond(embed=ErrorEmbed(description="We attempted to send your embed JSON as a test and it failed :(, please check your formatting."))
        return
    
    Guild(ctx.guild_id).create_embed(embed_name, embed_json)

    await ctx.respond(embed=SuccessEmbed(description=f"{embed_name} created."))

def embed_name_autocomplete(ctx: AutocompleteContext):
    embed_name = ctx.options["embed_name"]
    return [emb for emb in Guild(ctx.interaction.guild.id).get_embed_names() if embed_name.lower() in embed_name]

@embed.command()
async def get(ctx, embed_name: Option(str, autocomplete=basic_autocomplete(embed_name_autocomplete))):
    command = Guild(ctx.guild_id).get_embed(embed_name)
    if not command:
        await ctx.respond(embed=ErrorEmbed(description=f"`{embed_name}` not found. Try creating it!"))
        return
    await ctx.respond(embed=Embed.from_dict(loads(command)))

@embed.command()
async def delete(ctx, command_name):
    Guild(ctx.guild_idbet
          ).delete_embed(command_name)
    await ctx.respond(embed=SuccessEmbed(
        description=f"{command_name} deleted"
    ))
    return


help_file_1 = File(BytesIO(open("./src/dump/00.jpg", "rb").read()), "help_file_1.jpg")
help_file_2 = File(BytesIO(open("./src/dump/01.jpg", "rb").read()), "help_file_2.jpg")

@embed.command()
async def help(ctx: discord.ApplicationContext):

    embed_command_id = get(ctx.bot.commands, name="embed").id

    msg = f"Create a new command: </embed create:{embed_command_id}>\n" + \
          f"Get a command: </embed get:{embed_command_id}>\n" + \
          f"Delete a command: </embed delete:{embed_command_id}>\n" + \
          f"List all commands: </embed list:{embed_command_id}>\n" + \
          "\nWhen creating a new command, you are required to submit the json of your command embed. " + \
          "The easiest way to do this is to visit [message.style](https://message.style/app/) and create one, it has a nice user interface for all kinds of discord json formatting. " + \
          "Keep in mind, [message.style](https://message.style/app/) is used for more than just embeds, so you will need to select ONLY the embed part of the `JSON` to submit when you create a custom command." 
    
    await ctx.respond(embed=SuccessEmbed(title="Guild Embed Command Help Menu", description=msg), ephemeral=False, files=[help_file_1, help_file_2])

@embed.command()
async def list(ctx):
    embeds = Guild(ctx.guild_id).get_embed_names()
    if embeds:
        await ctx.respond(embed=SuccessEmbed(title="Custom Embeds (Guild)", description="\n".join(embeds)))
    else:
        await ctx.respond(embed=ErrorEmbed(description="No custom commands found for your guild. Try `/embed create` !",))
