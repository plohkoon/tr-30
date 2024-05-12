from discord import Intents
from discord.ext.commands import Bot
from .constants import DISCORD_KEY
import sys
import os

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
        print(f'{self.user} has connected to Discord!', file=sys.stderr)

        for file in os.listdir("./lib"):
            if file.endswith("_cog.py"):
                await self.load_extension(name=f"lib.{file[:-3]}")

        await self.tree.sync()

    def run(self) -> None:
        super().run(DISCORD_KEY)
