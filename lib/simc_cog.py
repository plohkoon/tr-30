from discord import Interaction, Message
from discord.app_commands import Group
from discord.ext.commands import Bot, Cog
import asyncio

from re import DOTALL, IGNORECASE, MULTILINE, compile

SIMC_REGEX = compile(
  r"```Simc (?P<type>character|raw)\n(?P<content>.+?)\n```",
  flags=MULTILINE | IGNORECASE | DOTALL
)

from . import logging

async def setup(bot: Bot):
    await bot.add_cog(SimcCog(bot))

class SimcCog(Cog):
    group = Group(name="simc", description="Simulate a character in wow")
    def __init__(self, bot: Bot):
        self.bot = bot

    @group.command(name="character", description="Simulate a character")
    async def character(self, interaction: Interaction, character: str, server: str = "Sargeras") -> None:
        logging.info("Starting to simulate character")
        await interaction.response.defer(ephemeral=True)

        char = await self._fetch_character(character, server)
        await self._simulate_character(char)

        await interaction.followup.send(f"Character simulated {character}-{server}")

    @group.command(name="raw", description="Simulate from the simc string")
    async def raw(self, interaction: Interaction, simc: str) -> None:
        logging.info("Starting to simulate raw")
        await interaction.response.defer(ephemeral=True)

        await self._simulate_character(simc)

        await interaction.followup.send(f"Simulated raw {simc}")

    @Cog.listener("on_message")
    async def simc_message(self, message: Message):
        if message.author == self.bot.user:
            return

        match = SIMC_REGEX.match(message.content)

        if not match:
            return

        logging.info("Simc message detected")

        simc_type = match.group("type")
        simc_content = match.group("content")

        if simc_type == "character":
            async with message.channel.typing():
                character, server = simc_content.split("-")
                logging.info("Fetching Character")
                character_info = await self._fetch_character(character, server)
                logging.info("Simulating Character")
                await self._simulate_character(character_info)

            await message.channel.send("Simulated character")
        elif simc_type == "raw":
            async with message.channel.typing():
                logging.info("Simulating Raw")
                await self._simulate_character(simc_content)

            await message.channel.send("Simulated raw")
        else:
            logging.error("Invalid simc type")
            await message.channel.send("Invalid simc type")

    async def _fetch_character(self, character: str, server: str) -> None:
        await asyncio.sleep(2)

    async def _simulate_character(self, character: str) -> None:
        await asyncio.sleep(2)

