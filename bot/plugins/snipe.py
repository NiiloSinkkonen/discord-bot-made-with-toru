import disnake
from disnake.ext.commands import Bot, Cog


class NicknameSnipe(Cog):
    def __init__(self, snipebot: Bot):
        self.bot = snipebot

    @Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        if before.display_name == after.display_name:
            return
        channel = self.bot.get_channel(1452715200896700640)

        await channel.send(f"**{before.display_name}** change their nick to **{after.display_name}**")


def setup(bot: Bot):
    plugin = NicknameSnipe(bot)
    bot.add_cog(plugin)
