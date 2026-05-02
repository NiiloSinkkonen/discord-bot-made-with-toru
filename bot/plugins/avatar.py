import disnake
from disnake.ext.commands import Bot, slash_command

from bot.plugin import Plugin


class Avatar(Plugin):
    @slash_command(name="avatar", description="displays persons avatar")
    async def avatar(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
    ):
        avatar_embed = disnake.Embed()
        avatar_embed.set_author(name=member.display_name)
        avatar_embed.set_image(member.display_avatar)
        await inter.send(embed=avatar_embed)


def setup(bot: Bot):
    bot.add_cog(Avatar())
