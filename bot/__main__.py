import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(
    command_prefix="!",
    intents=disnake.Intents.all(),
    reload=True,
    test_guilds=[705809739912577094],
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")
    print("Shit giggles")


def main():
    token = os.getenv("TOKEN")

    if not token:
        print("TOKEN environment variable not set.")
        return

    # This scans the folder and calls setup() on each .py file
    bot.load_extensions("bot/plugins")

    bot.run(token)


if __name__ == "__main__":
    main()
