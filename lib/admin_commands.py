from discord.app_commands import Group, CommandTree, guild_only, guilds, command
from discord import Interaction
from discord.ext.commands import Cog
from .constants import TR_GUILD_ID, IABW_GUILD_ID, PLOHKOON_USER_ID


@guild_only()
@guilds(TR_GUILD_ID, IABW_GUILD_ID)
class AdminCommands(Cog):
    def __init__(self, tree: CommandTree):
        super().__init__()
        self.tree = tree
        tree.add_command(self)

    @command(name="sync", description="Syncs the bot with the server")
    async def sync(self, interaction: Interaction) -> None:
        if interaction.user.id == PLOHKOON_USER_ID:
            await self.tree.sync(guild=interaction.guild)
            print(f"Command tree synced to {interaction.guild.name}")
            await interaction.response.send_message("Command tree synced", ephemeral=True)
        else:
            await interaction.response.send_message("Piss off, you're not my dad", ephemeral=True)
