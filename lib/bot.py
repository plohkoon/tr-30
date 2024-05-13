from discord import Intents
from discord.ext.commands import Bot
from .constants import DISCORD_KEY
import sys
import os
from . import logging

class TR30Bot(Bot):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TR30Bot, cls).__new__(
                cls, *args, **kwargs)

        return cls._instance

    def __init__(self, *args, **kwargs):
        if 'intents' in kwargs:
            del kwargs['intents']

        super().__init__("$", *args, intents=Intents.all(), **kwargs)

    async def on_ready(self) -> None:
        logging.info(f'{self.user} has connected to Discord!')

        for file in os.listdir("./lib"):
            if file.endswith("_cog.py"):
                logging.info(f"Loading {file[:-3]}")

                await self.load_extension(name=f"lib.{file[:-3]}")

        await self.tree.sync()

    def run(self) -> None:
        logging.info("Starting TR30...")
        super().run(DISCORD_KEY)
