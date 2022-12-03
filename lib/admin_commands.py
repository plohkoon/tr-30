from discord.app_commands import command
from discord import Interaction
from discord.ext.commands import Cog, Bot
from .constants import PLOHKOON_USER_ID


class AdminCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="sync", description="Syncs the bot with the server")
    async def sync(self, interaction: Interaction) -> None:
        if interaction.user.id == PLOHKOON_USER_ID:
            await self.bot.tree.sync(guild=interaction.guild)
            print(f"Command tree synced to {interaction.guild.name}")
            await interaction.response.send_message("Command tree synced", ephemeral=True)
        else:
            await interaction.response.send_message("Piss off, you're not my dad", ephemeral=True)
