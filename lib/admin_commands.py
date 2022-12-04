from discord.app_commands import command, guilds
from discord import Interaction
from discord.ext.commands import Cog, Bot
from .constants import PLOHKOON_USER_ID
from .constants import TR_GUILD, IABW_GUILD
import sys


class AdminCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="sync", description="Syncs the bot with the server")
    @guilds(TR_GUILD, IABW_GUILD)
    async def sync(self, interaction: Interaction) -> None:
        if interaction.user.id == PLOHKOON_USER_ID:
            await self.bot.tree.sync(guild=interaction.guild)
            print(
                f"Command tree synced to {interaction.guild.name}", file=sys.stderr)
            await interaction.response.send_message("Command tree synced", ephemeral=True)
        else:
            await interaction.response.send_message("Piss off, you're not my dad", ephemeral=True)
