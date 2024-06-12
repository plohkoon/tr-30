from discord import Interaction
from discord.app_commands import command
from discord.ext.commands import Bot, Cog

from . import logging


async def setup(bot: Bot):
    await bot.add_cog(EventCog(bot))

class EventCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="event", description="Event command")
    async def event(self, interaction: Interaction) -> None:
        logging.warning("Starting to track event")
        event = await interaction.guild.fetch_scheduled_events()[0]

        event
