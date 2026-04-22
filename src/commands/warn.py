import database
from discord import (
    SlashCommandGroup,
    User,
    Embed,
    Color,
    ApplicationContext,
)
import discord

warn = SlashCommandGroup("warn")


@warn.command()
@discord.option("user", User, description="User to warn")
async def warning(ctx: ApplicationContext, user: User, reason: str):
    if ctx.guild is None:
        return await ctx.respond("This command can only be used in guilds")
    if (
        isinstance(ctx.author, discord.Member)
        and ctx.author.guild_permissions.manage_messages
    ):
        db = database.Guild(ctx.author.guild.id)

        # add other moderator perms or possibly add a settable moderator role.
        db.warn_user(user.id, reason)
        await ctx.respond(
            embed=Embed(description=f"{user.name} was warned.", color=Color.green())
        )


@warn.command(contexts={discord.InteractionContextType.guild})
@discord.option("user", User, description="User to check warnings for")
async def get_warnings(ctx: ApplicationContext, user: User):
    async def get_embed(user_id):
        if ctx.guild_id is None:
            return await ctx.respond("Can only be used in guilds")

        db = database.Guild(ctx.guild_id)
        warnings = await db.get_warnings(user_id)
        embed = Embed()
        i = 0
        for guild_id, user_id, reason, created_at in warnings:
            if guild_id == guild_id:
                i += 1

        return embed

    if user:
        if (
            isinstance(ctx.author, discord.Member)
            and ctx.author.guild_permissions.manage_messages
        ):  # add other moderator perms or possibly add a settable moderator role.
            await ctx.respond(embed=get_embed(user.id))
        else:
            await ctx.respond(
                embed=Embed(description="Missing permissions to run this command.")
            )
        return

    await ctx.respond(embed=get_embed(ctx.author.id))


@warn.command(description="delete all warnings for a user")
@discord.option("user", User, description="User whose warnings are being deleted")
async def delete_warnings(ctx, user: User):
    pass
