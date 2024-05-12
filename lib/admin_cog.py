from discord.app_commands import command
from discord import Interaction
from discord.ext.commands import Cog, Bot
from .constants import PLOHKOON_USER_ID
import sys

async def setup(bot: Bot):
    await bot.add_cog(AdminCog(bot))

class AdminCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="sync", description="Syncs the bot with the server")
    async def sync(self, interaction: Interaction) -> None:
        if await self.guard(interaction):
          await self.bot.tree.sync(guild=interaction.guild)
          print(
              f"Command tree synced to {interaction.guild.name}", file=sys.stderr)
          await interaction.followup.send("Command tree synced", ephemeral=True)

    async def guard(self, interaction: Interaction) -> None:
        if interaction.user.id == PLOHKOON_USER_ID:
            await interaction.response.send_message("Piss off, you're not my dad", ephemeral=True)
            return False

        await interaction.response.defer(ephemeral=True)
        return True
