import disnake
from disnake.ext import commands as cum


class Ping(cum.Cog):
    def __init__(self, bot: cum.Bot):
        self.bot = bot

    @cum.command()
    async def ping(self, ctx: cum.Context):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @cum.slash_command(name="ping", description="Check bot latency")
    async def slash_ping(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")


def setup(bot: cum.Bot):
    bot.add_cog(Ping(bot))
