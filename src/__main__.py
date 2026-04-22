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
import asyncio


def main():
    # 1. Manually create the event loop
    loop = asyncio.new_event_loop()

    # 2. Set it as the current loop for the thread
    asyncio.set_event_loop(loop)

    # 3. Now initialize the bot
    intents = discord.Intents.default()
    bot = Bot(intents=intents)

    load_dotenv()  # take environment variables from .env.

    intents = Intents.default()
    intents.message_content = True

    bot = Bot(intents=intents)

    @bot.event
    async def on_ready():
        # await bot.sync_commands()
        print(f"We have logged in as {bot.user}")

    @bot.event
    async def on_application_command_error(ctx: discord.ApplicationContext, error):
        await ctx.respond(
            embed=discord.Embed(
                description="Error processing command...", color=discord.Color.red()
            )
        )
        e = format_exception(error)
        error_channel = os.getenv("ERROR_LOG_CHANNEL")
        if error_channel is None:
            print(e)
            return
        channel = ctx.bot.get_channel(int(error_channel))
        arguments = (
            dumps(ctx.selected_options, indent=4)
            if ctx.selected_options
            else ctx.selected_options
        )
        traceback = "\n".join([f"```\n{i}```" for i in e])
        if isinstance(channel, discord.TextChannel):
            if ctx.command is None:
                return
            await channel.send(
                embed=discord.Embed(
                    description=f"Error occurred while processing {ctx.user.display_name}'s command\n\nCommand Name:\n/{ctx.command.qualified_name}\n\nArguments:\n```json\n{arguments}```\n\nError:\n{traceback}"
                )
            )

    bot.add_application_command(developer.developer)
    bot.add_application_command(help.help)
    bot.add_application_command(embed.embed)
    bot.add_application_command(compiler.compile)

    # 4. Start the bot using the loop
    try:
        bot.run(os.getenv("DISCORD_TOKEN"))  # Use DI
    finally:
        loop.close()


if __name__ == "__main__":
    main()
