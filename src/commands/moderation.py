import database
from discord import SlashCommandGroup, User, Embed, Color, ApplicationContext
import discord

moderation = SlashCommandGroup("moderation", "Moderation commands for the guild.")


@moderation.command()
@discord.option("user", User, description="User to warn")
async def warn(ctx: ApplicationContext, user: User, reason: str):
    if isinstance(ctx.author, discord.User):
        return await ctx.respond("Can only be used in guilds")

    if (
        ctx.author.guild_permissions.manage_messages
    ):  # add other moderator perms or possibly add a settable moderator role.
        if ctx.guild_id is None:
            return await ctx.respond("Can only be used in guilds")

        db = database.Guild(ctx.guild_id)
        db.warn_user(user.id, reason)
        await ctx.respond(
            embed=Embed(description=f"{user.name} was warned.", color=Color.green())
        )


@moderation.command()
@discord.option("user", User, description="User to get warnings for")
async def get_warnings(ctx: ApplicationContext, user: User):

    async def get_embed(user_id):
        warnings = await get_warnings(ctx.guild_id, user_id)
        embed = Embed()
        i = 0
        for guild_id, user_id, reason, created_at in warnings:
            if guild_id == guild_id:
                embed.add_field(name=f"Warning {i}", value=reason)
                i += 1
        return embed

    if user:
        if (
            isinstance(ctx.author, discord.Member)
            and ctx.author.guild_permissions.manage_messages
        ):  # add other moderator perms or possibly add a settable moderator role.
            await ctx.respond(embed=await get_embed(user.id))
        else:
            await ctx.respond(
                embed=Embed(description="Missing permissions to run this command.")
            )
        return

    await ctx.respond(embed=get_embed(ctx.author.id))
