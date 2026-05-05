import disnake
import httpx
from disnake import Option, OptionType
from disnake.ext.commands import Bot, Cog, slash_command

REACTION_URL = "https://api.otakugifs.xyz/gif"


class Waifu(Cog):
    def __init__(self) -> None:
        self.http = httpx.AsyncClient()

    async def send_reaction(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        reaction: str,
        fmt: str | None = None,
    ):
        if member == inter.author:
            await inter.send(f"You can't {reaction} yourself! Baffoon.")
            return
        await inter.response.defer()

        response = await self.http.get(REACTION_URL, params={"reaction": reaction})
        data = response.json()

        if fmt is None:
            if reaction.endswith("y"):
                ending = "ies"
            elif reaction.endswith(("s", "sh")):
                ending = "es"
            else:
                ending = "s"

            header = f"{inter.author.mention} {reaction}{ending} {member.mention}!"
        else:
            header = fmt.format(author=inter.author.mention, target=member.mention)

        embed = disnake.Embed(description=header, color=0xFF69B4)
        embed.set_image(url=data["url"])

        await inter.send(embed=embed)

    for reaction in [
        "airkiss",
        "bite",
        "bleh",
        "blush",
        "brofist",
        "cuddle",
        "hug",
        "huh",
        "kiss",
    ]:  # Go through each command that is generic enough

        async def _temp_command(
            self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reaction: str = reaction
        ) -> None:  # Create a generic version of a command
            await self.send_reaction(inter, member, reaction)

        command = slash_command(  # Specify slash command options for this command
            name=reaction,
            description=f"{reaction.title()} the person you want to {reaction}",
            options=[Option(name="member", description=f"Member to {reaction}", required=True, type=OptionType.user)],
        )
        locals()[reaction] = command(_temp_command)  # Add command to the class scope

    @slash_command(description="Angrystare the person you want to angrystare")
    async def angrystare(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "angrystare", "{author} stares at {target} angrily")

    @slash_command(description="Celebrate the person you want to celebrate")
    async def celebrate(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "celebrate", "{author} celebrates {target}'s funeral")

    @slash_command(description="Cheers the person you want to cheers")
    async def cheers(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "cheers", "{author} cheers with {target}")

    @slash_command(description="Clap the person you want to clap")
    async def clap(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "clap", "{author} claps with {target}")

    @slash_command(description="Confused the person you want to confused")
    async def confused(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "confused", "{author} is confused about {targett}")

    @slash_command(description="Cry the person you want to cry")
    async def cry(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "cry", "{author} cries with {target}")

    @slash_command(description="Dance the person you want to dance with")
    async def dance(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "dance", "{author} dances with {target}")

    @slash_command(description="Drool the person you want to drool")
    async def drool(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "drool", "{author} drools about {target}")

    @slash_command(description="Facepalm the person you want to facepalm")
    async def facepalm(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "facepalm", "{author} facepalms at {target}")

    @slash_command(description="Handhold the person you want to handhold")
    async def handhold(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member) -> None:
        await self.send_reaction(inter, member, "handhold", "{author} holds {target}'s hand")


def setup(bot: Bot) -> None:
    bot.add_cog(Waifu())
