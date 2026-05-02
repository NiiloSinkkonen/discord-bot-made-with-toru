import disnake
import httpx
from disnake.ext.commands import Bot, slash_command

from bot.plugin import Plugin

API_URL = "https://api.binance.com/api/v3/ticker/price"


class Crypto(Plugin):
    def __init__(self) -> None:
        self.http = httpx.AsyncClient()

    @slash_command(description="Check current market value for a crypto")
    async def crypto(self, inter: disnake.ApplicationCommandInteraction, coin: str, currency: str):
        await inter.response.defer()
        coin = coin.upper()
        currency = currency.upper()
        response = await self.http.get(API_URL, params={"symbol": coin + currency})
        if response.is_error:
            await inter.edit_original_response("Invalid coin")
            return

        data = response.json()
        price = float(data["price"])
        await inter.edit_original_response(f"{coin} is {price:.02f} {currency}")


def setup(bot: Bot):
    bot.add_cog(Crypto())
