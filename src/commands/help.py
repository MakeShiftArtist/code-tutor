from discord.ext import commands
from discord import Embed, utils, Color

@commands.slash_command(description="Displays help meassage")
async def help(ctx):
    embed_command_id = utils.get(ctx.bot.commands, name="embed").id
    msg = f"Manage Guild Embeds: </embed help:{embed_command_id}>"
    await ctx.respond(embed=Embed(
        title="DD Bot Help Menu",
        description=msg,
        color=Color.random()
    ))


