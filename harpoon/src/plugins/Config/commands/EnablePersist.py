


async def run(plugin, ctx):
    plugin.db.configs.update(ctx.guild.id, "persist", True)
    await ctx.send(plugin.t(ctx.guild, "enabled_module_no_channel", _emote="YES", module="Persist"))