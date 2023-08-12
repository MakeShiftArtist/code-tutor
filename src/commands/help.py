from discord.ext import commands

@commands.slash_command()
async def help(ctx):
    await ctx.respond("test")


