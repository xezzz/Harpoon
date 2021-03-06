import discord
from discord.ext import commands

import logging

from ..Types import NotCachedError
from ..Types import PostParseError as _PostParseError
from ..functions import MissingRequiredArgument, PostParseError, BadArgument



log = logging.getLogger(__name__)


async def run(plugin, ctx, error):
    if isinstance(error, NotCachedError):
        if plugin.bot.ready is False:
            log.info("Tried to use a command while still chunking guilds - {}".format(ctx.guild.id))

    if isinstance(error, commands.CommandNotFound):
        pass

    if isinstance(error, commands.CheckFailure):
        await ctx.send(plugin.t(ctx.guild, "missing_user_perms", _emote="WARN"))
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(plugin.t(ctx.guild, "missing_bot_perms", _emote="WARN"))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(plugin.t(ctx.guild, "missing_user_perms", _emote="WARN"))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(plugin.t(ctx.guild, "on_cooldown", retry_after=round(error.retry_after)))

    elif isinstance(error, commands.MissingRequiredArgument):
        await MissingRequiredArgument.run(plugin, ctx)
    elif isinstance(error, _PostParseError):
        await PostParseError.run(plugin, ctx, error)
    elif isinstance(error, commands.BadArgument):
        await BadArgument.run(plugin, ctx, error)
    else:
        log.warn("Error in command {} - {}".format(ctx.command.name, error))
