import discord

from urllib import parse

from ....utils.RegEx import getPattern, Match




INVITE_RE = getPattern(
    r"(?:https?://)?(?:www\.)?(?:discord(?:\.| |\[?\(?\"?'?dot'?\"?\)?\]?)?(?:gg|io|me|li)|discord(?:app)?\.com/invite)/+((?:(?!https?)[\w\d-])+)"
)


async def handleDeletion(plugin, message, found_invite):
    try:
        await message.delete()
    except discord.NotFound:
        pass
    await plugin.action_validator.figure_it_out(
        message, 
        message.guild, 
        message.author,
        "invite_censor",
        moderator=plugin.bot.user,
        moderator_id=plugin.bot.user.id,
        reason=f"Advertising (Sending Discord invite): {found_invite}",
        link=found_invite,
        _type="invite"
    )


async def check(plugin, message):
    decoded = parse.unquote(message.content)
    found_invites = Match(decoded, INVITE_RE, option="findall", _return=True)
    allowed_invites = plugin.db.configs.get(message.guild.id, "whitelisted_invites")

    if found_invites:
        for inv in found_invites:
            try:
                invite: discord.Invite = await plugin.bot.fetch_invite(inv)
            except discord.NotFound:
                plugin.bot.ignore_for_event.add("messages", message.id)
                return await handleDeletion(plugin, message, inv)
            if invite.guild is None:
                plugin.bot.ignore_for_event.add("messages", message.id)
                return await handleDeletion(plugin, message, inv)
            else:
                if invite.guild is None or (not invite.guild.id in allowed_invites and invite.guild.id != message.author.guild.id):
                    plugin.bot.ignore_for_event.add("messages", message.id)
                    return await handleDeletion(plugin, message, inv)