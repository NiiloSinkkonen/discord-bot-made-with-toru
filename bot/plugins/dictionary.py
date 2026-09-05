import disnake
import httpx2
from async_lru import alru_cache
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.utils import find

WORD_URL = "https://freedictionaryapi.com/api/v1"


class Dictionary(Cog):
    def __init__(self) -> None:
        self.http = httpx2.AsyncClient(base_url=WORD_URL)

    @slash_command(description="Search in dictionary")
    async def define(self, inter: disnake.ApplicationCommandInteraction, word: str, language: str = "en") -> None:
        await inter.response.defer()

        languages = await self.get_languages()
        lang_code = languages.get(language.title()) or find(lambda code: code == language.lower(), languages.values())

        if not lang_code:
            await inter.send("Your language is invalid! 😏")
            return

        for _ in range(2):  # Run this loop twice
            try:
                api_response = await self.http.get(f"/entries/{lang_code}/{word}")
            except Exception as e:
                await inter.send(f"Failed to find your request = {e}")
                return

            data = api_response.json()

            if entries := data["entries"]:
                break
            if word.lower() == word:
                word = word.title()

            elif word.title() == word:
                word = word.lower()
        else:  # Run if loop did not break
            await inter.send(f"No definition found for **{word}**.")
            return

        sense = entries[0]["senses"][0]
        definition: str = sense["definition"]
        examples: list[str] = sense["examples"]

        message = f"The definition of **{word}** is _{definition}_."

        if examples:
            message += f"\nExample: {examples[0]}"

        await inter.send(message)

    @alru_cache(ttl=86400)  # 1 day
    async def get_languages(self) -> dict[str, str]:
        response = await self.http.get("/languages")
        data = sorted(response.json(), key=lambda lang: lang["words"], reverse=True)
        return {lang["name"]: lang["code"] for lang in data}

    @define.autocomplete("language")
    async def filter_languages(self, inter: disnake.ApplicationCommandInteraction, user_input: str) -> dict[str, str]:
        languages = await self.get_languages()
        languages = filter(lambda lang: lang[0].lower().startswith(user_input.lower()), languages.items())
        return dict(list(languages)[:25])


def setup(bot: Bot):
    bot.add_cog(Dictionary())
