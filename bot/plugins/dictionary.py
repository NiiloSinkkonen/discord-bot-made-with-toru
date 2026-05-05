import io

import disnake
import httpx
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.utils import MISSING

WORD_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"


class Dictionary(Cog):
    def __init__(self) -> None:
        self.http = httpx.AsyncClient()

    @slash_command(description="Search in dictionary")
    async def define(self, inter: disnake.ApplicationCommandInteraction, word: str) -> None:
        await inter.response.defer()
        try:
            api_response = await self.http.get(WORD_URL + word)
            if not api_response.is_success:
                await inter.send("Definition not found.")
                return
            data = api_response.json()

            discord_file = MISSING

            try:
                if audio_url := data[0]["phonetics"][0]["audio"]:
                    audio_response = await self.http.get(audio_url)
                    audio = io.BytesIO(audio_response.content)
                    discord_file = disnake.File(audio, f"{word}.mp3")
            except Exception:
                pass

            definition = data[0]["meanings"][0]["definitions"][0]["definition"]
            await inter.send(f"The definition of **{word}** is _{definition}_ ", file=discord_file)
        except Exception as e:
            await inter.send(f"nigger nogger fialed because you are gei = {e}")


def setup(bot: Bot):
    bot.add_cog(Dictionary())
