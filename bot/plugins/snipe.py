import disnake
from disnake.ext.commands import Bot

from bot.plugin import Plugin


class nicknamesnipe(Plugin):

    def __init__(self, snipebot: Bot):
        self.bot = snipebot

    @Plugin.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        if before.display_name == after.display_name:
            return
        channel = self.bot.get_channel(1452715200896700640)

        await channel.send(
            f"**{before.display_name}** change their nick to **{after.display_name}**"
        )



def setup(bot: Bot):
    plugin = nicknamesnipe(bot)
    bot.add_cog(plugin)
