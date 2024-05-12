from discord.ext.commands import Cog, Bot
from discord import Message
from .constants import MACIUS_USER_ID, CPT_FROGS_USER_ID
from re import compile, IGNORECASE
import sys
from datetime import datetime

spoiler_regex = compile(r'\|\|(.+?)\|\|')
based_regex = compile(r'based', IGNORECASE)

async def setup(bot: Bot):
    await bot.add_cog(MessageCog(bot))

class MessageCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.last_spoiler_message = datetime.fromordinal(1)

    @Cog.listener("on_message")
    async def spoiler(self, message: Message):
        if message.author == self.bot.user:
            return

        if spoiler_regex.match(message.content):
            print("Found a spoiler!!!", file=sys.stderr)
            if (datetime.now() - self.last_spoiler_message).seconds > 120:
                self.last_spoiler_message = datetime.now()
                await message.channel.send(f"Hey <@{MACIUS_USER_ID}>, you posted a spoiler!")
                self.last_spoiler_message = datetime.now()

    @Cog.listener("on_message")
    async def based(self, message: Message):
        if message.author == self.bot.user:
            return

        if message.author.id == CPT_FROGS_USER_ID and based_regex.match(message.content):
            print("Found a BASED", file=sys.stderr)
            await message.channel.send(f"Hey <@{CPT_FROGS_USER_ID}>, https://youtu.be/RUExiGNHF5s")
