from datetime import datetime
from re import IGNORECASE, compile

from discord import Message
from discord.ext.commands import Bot, Cog

from . import logging
from .constants import CPT_FROGS_USER_ID, MACIUS_USER_ID, PLOHKOON_USER_ID

SPOILER_REGEX = compile(r'\|\|(.+?)\|\|')
BASED_REGEX = compile(r'.*based.*', IGNORECASE)
DEBOUNCE_TIME = 1


async def setup(bot: Bot):
    await bot.add_cog(MessageCog(bot))


class MessageCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.last_spoiler_message = datetime.fromordinal(1)
        self.last_based_message = datetime.fromordinal(1)

    @Cog.listener("on_message")
    async def spoiler(self, message: Message):
        if message.author == self.bot.user:
            return

        if not SPOILER_REGEX.match(message.content):
            return

        logging.info("Found a spoiler", discord_msg=message)

        # We don't want to overwhelm conversations
        # so only allow it to fire every 2 minutes
        if (datetime.now() - self.last_spoiler_message).seconds <= DEBOUNCE_TIME:
            logging.info("Time threshold not elapsed, skipping.", discord_msg=message)
            return

        logging.info("Time threshold elapsed, pinging sir macius", discord_msg=message)
        self.last_spoiler_message = datetime.now()
        await message.channel.send(
            f"Hey <@{MACIUS_USER_ID}>, {message.author.nick} said something you might want to see!")
        self.last_spoiler_message = datetime.now()

    @Cog.listener("on_message")
    async def based(self, message: Message):
        if message.author == self.bot.user:
            return

        if message.author.id not in [CPT_FROGS_USER_ID]:
            return
        if not BASED_REGEX.match(message.content):
            return

        logging.info("Found a BASED from captain frogs", discord_msg=message)

        if (datetime.now() - self.last_based_message).seconds <= DEBOUNCE_TIME:
            logging.info("Time threshold not elapsed, skipping.", discord_msg=message)

        logging.info("Time threshold elapsed, responding to based", discord_msg=message)
        self.last_based_message = datetime.now()
        await message.channel.send(f"Hey <@{CPT_FROGS_USER_ID}>, https://youtu.be/RUExiGNHF5s")
