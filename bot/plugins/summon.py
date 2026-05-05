import disnake
from disnake.ext.commands import Bot, Cog, command, slash_command


class Summon(Cog):
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
