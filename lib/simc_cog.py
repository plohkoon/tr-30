from discord import Interaction, Message
from discord.app_commands import Group
from discord.ext.commands import Bot, Cog
import asyncio
from typing import Union

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
        self.queue = asyncio.Queue()
        self.workers = [asyncio.create_task(self.process(self.queue)) for _ in range(3)]

    async def cog_unload(self):
        await self.queue.join()
        for worker in self.workers:
            worker.cancel()

        await asyncio.gather(*self.workers, return_exceptions=True)

    @group.command(name="character", description="Simulate a character")
    async def character(self, interaction: Interaction, character: str, server: str = "Sargeras") -> None:
        logging.info("Starting to simulate character")
        await interaction.response.defer(ephemeral=True)

        await self.queue.put(("char", (character, server), interaction))

    @group.command(name="raw", description="Simulate from the simc string")
    async def raw(self, interaction: Interaction, simc: str) -> None:
        logging.info("Starting to simulate raw")
        await interaction.response.defer(ephemeral=True)

        await self.queue.put(("raw", simc, interaction))

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
            character, server = simc_content.split("-")
            await self.queue.put(("char", (character, server), message))
        elif simc_type == "raw":
            await self.queue.put(("raw", simc_content, message))
        else:
            logging.error("Invalid simc type")
            await message.channel.send("Invalid simc type")

    async def _fetch_character(self, character: str, server: str) -> None:
        await asyncio.sleep(2)

    async def _simulate_character(self, character: str) -> None:
        await asyncio.sleep(2)

    async def _response(self, object: Union[Interaction, Message]) -> None:
        if isinstance(object, Interaction):
            await object.followup.send("Simulation complete")
        elif isinstance(object, Message):
            await object.channel.send("Simulation complete")

    async def process(self, queue):
        while True:
            type, data, object = await queue.get()
            logging.info("Processing a simc request")

            async with object.channel.typing():
                if type == "char":
                    await self._fetch_character(*data)
                    await self._simulate_character(data[0])
                elif type == "raw":
                    await self._simulate_character(data)

            logging.info("Done processing simc request, responding")

            await self._response(object)
