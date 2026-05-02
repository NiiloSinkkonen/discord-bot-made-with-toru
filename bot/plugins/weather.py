import os
from datetime import datetime

import disnake
import httpx
from disnake.ext import commands as cum
from disnake.utils import format_dt

# all common errors
ERRORS = {
    "400001": "Imputed location does not exist.",
    "400002": "The entries provided as query parameters were not valid for the request.",
    "400003": "The request is missing some required body parameters.",
    "400004": "The request is missing the required query parameters.",
    "400005": "The request violated some logic requirement.",
    "400006": "The request is missing some required header parameters.",
    "400007": "The entries provided as path parameters were not valid for the request.",
    "401001": "The method requires authentication, but it was not presented or is invalid.",
    "402001": "Adding additional tokens is required.",
    "403001": "The authentication token in use is restricted and cannot access the requested resource.",
    "403002": "The plan limit for a resource has been reached.",
    "403003": "The plan is restricted and cannot perform this action.",
    "404001": "A resource id was not found.",
    "500001": "Possibly a temporary issue due to downtime. Wait and retry the operation.",
    "503001": "Service is currently unavailable, please wait for a while and retry the operation. Supporting header: Retry-After",
}


class Weather(cum.Cog):
    def __init__(self, bot: cum.Bot):
        self.bot = bot
        self.http = httpx.AsyncClient(
            base_url="https://api.tomorrow.io/v4/weather",
            params={
                "units": "metric",
                "apikey": os.getenv("TOMMOROWIO_API_KEY"),
            },
            headers={
                "accept": "application/json",
                "accept-encoding": "deflate, gzip, br",
            },
        )

    @cum.slash_command(description="Show weather")
    async def weather(self, inter: disnake.ApplicationCommandInteraction, location: str):
        await inter.response.defer()
        response = await self.http.get("/realtime", params={"location": location})
        if response.is_error:
            for code, description in ERRORS.items():
                if code in response.text:
                    await inter.send(description)
                    break
            else:
                await inter.send("Absolte shit fuck happend and it didnt work. KYS")
            return

        data = response.json()
        temperature = data["data"]["values"]["temperature"]
        time = datetime.fromisoformat(data["data"]["time"])
        location_name = data["location"]["name"]
        await inter.send(f"It is {temperature}°C in {location_name} at {format_dt(time)}.")


def setup(bot: cum.Bot):
    bot.add_cog(Weather(bot))


# https://api.tomorrow.io/v4/weather/forecast ?units=metric &apikey=NIGA &location=new%20york
