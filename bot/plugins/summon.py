import disnake
from disnake.ext.commands import Bot, command, slash_command

from bot.plugin import Plugin


class Summon(Plugin):
    @slash_command(description="summon person by sending private message")
    async def summon(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        content: str,
    ):
        await member.send(content)
        await inter.send(f"{inter.author.mention} Summoned {member.mention}")


def setup(bot: Bot):
    bot.add_cog(Summon())
