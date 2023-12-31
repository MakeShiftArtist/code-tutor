from discord import SlashCommandGroup, Option, User, Embed, Color, ApplicationContext
from database import warn_user
from datetime import T

warn = SlashCommandGroup("warn")

@warn.command()
async def warning(ctx, user: Option(User, "User to warn"), reason: str):
    if ctx.author.guild_permissions.manage_messages: # add other moderator perms or possibly add a settable moderator role.
        warn_user(ctx.guild_id, user.id, "warn", reason)
        await ctx.respond(embed=Embed(
            description=f"{user.name} was warned.",
            color=Color.green()
        ))

@warn.command()
async def get_warnings(ctx: ApplicationContext, user: Option(User, "User whos warnings to get") = None):

    def get_embed(user_id):
        warnings = get_warnings(ctx.guild_id, user_id)
        embed = Embed()
        i = 0
        for guild_id, user_id, reason, created_at in warnings:
            if guild_id == guild_id:
                embed.add_field()
                i += 1
        return embed

    if user:
        if ctx.author.guild_permissions.manage_messages: # add other moderator perms or possibly add a settable moderator role.
            await ctx.respond(embed=get_embed(user.id))
        else:
            await ctx.respond(embed=Embed(
                description="Missing permissions to run this command."
            ))
        return

    await ctx.respond(embed=get_embed(ctx.author.id))

@warn.command(description="delete all warnings for a user")
async def delete_warnings(ctx, user: Option(User, "User to delete warnings of")):
    pass