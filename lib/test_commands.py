from discord.app_commands import command
from discord import Interaction
from discord.ext.commands import Cog, Bot


class TestCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="helloworld", description="Hello World")
    async def hello_world(self, interaction: Interaction, argument: str) -> None:
        await interaction.response.send_message(f"Hello {argument}!")
