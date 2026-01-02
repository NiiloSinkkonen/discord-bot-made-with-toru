import disnake
from disnake.ext.commands import Bot

from ..plugin import Plugin


class nicknamesnipe(Plugin):
    # This function is called when class is created, e.g. Shame()
    # When we create plugin with Shame(bot) we pass bot into this function,
    # so we need to add it to the parameters
    def __init__(self, snipebot: Bot):
        # Save the bot inside the class so it's accessible by every function.
        self.bot = snipebot
        # self.bot is now available in the entire plugin, because `self` refers to the class itself
        # nigger_bot_client is only available in this init function

    @Plugin.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        if before.display_name == after.display_name:
            return

        # Use self.bot that we stored in __init__ to retrieve the channel
        channel = self.bot.get_channel(1452715200896700640)

        await channel.send(
            f"**{before.display_name}** change their nick to **{after.display_name}**"
        )


# Called by bot.load_extensions() in the main file
def setup(bot: Bot):
    # Create the plugin and provide `bot` so it can access bot functions later
    plugin = nicknamesnipe(bot)
    # Register the plugin in the bot
    bot.add_cog(plugin)
