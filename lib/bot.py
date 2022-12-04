from discord import Message, Intents
from discord.ext.commands import Bot
from .constants import MACIUS_USER_ID, CPT_FROGS_USER_ID, DISCORD_KEY, TR_GUILD
from re import compile, IGNORECASE
from random import random
import sys

from .admin_commands import AdminCommands
from .ai_commands import AICommands
from .test_commands import TestCommands
from .math_commands import MathCommands

spoiler_regex = compile(r'\|\|(.+?)\|\|')
based_regex = compile(r'based', IGNORECASE)


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

        await self.add_cog(AdminCommands(self))
        await self.add_cog(AICommands(self))
        await self.add_cog(TestCommands(self))
        await self.add_cog(MathCommands(self))

        await self.tree.sync(guild=TR_GUILD)

    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return

        if spoiler_regex.match(message.content):
            print("Found a spoiler!!!", file=sys.stderr)
            if random() < 0.5:
                await message.channel.send(f"Hey <@{MACIUS_USER_ID}>, {message.author.nick} said something you might want to see!")

        if message.author.id == CPT_FROGS_USER_ID and based_regex.match(message.content):
            print("Found a BASED", file=sys.stderr)
            await message.channel.send(f"Hey <@{CPT_FROGS_USER_ID}>, https://youtu.be/RUExiGNHF5s")

    def run(self) -> None:
        super().run(DISCORD_KEY)
