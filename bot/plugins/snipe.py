import disnake
from disnake.ext.commands import Bot, Cog


class NicknameSnipe(Cog):
    channel: disnake.TextChannel | None

    def __init__(self, snipebot: Bot):
        self.bot = snipebot
        self.channel = None

    @Cog.listener()
    async def on_audit_log_entry_create(self, entry: disnake.AuditLogEntry):
        if entry.action is not disnake.AuditLogAction.member_update:
            return

        target: disnake.Member = entry.target  # could be disnake.User if left, disnake.Object if deleted

        author = entry.user.display_name
        target_display_name_before = entry.before.nick or target.global_name or target.name
        target_display_name_after = entry.after.nick or target.global_name or target.name
        await self.channel.send(
            f"**{author}** changed **{target_display_name_before}**'s name to **{target_display_name_after}**"
        )

    async def cog_load(self):
        await self.bot.wait_until_ready()
        self.channel = self.bot.get_channel(1452715200896700640)


def setup(bot: Bot):
    plugin = NicknameSnipe(bot)
    bot.add_cog(plugin)
