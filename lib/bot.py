from discord import Client, Message, Intents
from discord.app_commands import CommandTree
from discord.ext.commands import Bot
from .constants import MACIUS_USER_ID, CPT_FROGS_USER_ID, DISCORD_KEY, TR_GUILD_ID
from re import compile, IGNORECASE
from random import random

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

        super().__init__(*args, intents=Intents.all(), **kwargs)

        self.tree: CommandTree = None

    async def on_ready(self) -> None:
        print(f'{self.user} has connected to Discord!')

        if self.tree is CommandTree:
            await self.tree.sync(guild=TR_GUILD_ID)

    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return

        print(message.content)

        if spoiler_regex.match(message.content):
            print("Found a spoiler!!!")
            if random() < 0.5:
                await message.channel.send(f"Hey <@{MACIUS_USER_ID}>, {message.author.nick} said something you might want to see!")

        if message.author.id == CPT_FROGS_USER_ID and based_regex.match(message.content):
            print("Found a BASED")
            await message.channel.send(f"Hey <@{CPT_FROGS_USER_ID}>, https://youtu.be/RUExiGNHF5s")

    def run(self) -> None:
        super().run(DISCORD_KEY)
