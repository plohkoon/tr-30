import sys
from datetime import datetime

from discord import Interaction, Message

from .constants import LOG_LEVEL


def debug(msg: str, interaction: Interaction = None, discord_msg: Message = None):
    if LOG_LEVEL in ["INFO", "WARNING", "ERROR"]:
        return

    log(msg, "debug", interaction, discord_msg)

def info(msg: str, interaction: Interaction = None, discord_msg: Message = None):
    if LOG_LEVEL in ["WARNING", "ERROR"]:
        return

    log(msg, "info", interaction, discord_msg)

def warning(msg: str, interaction: Interaction = None, discord_msg: Message = None):
    if LOG_LEVEL in ["ERROR"]:
        return

    log(msg, "warning", interaction, discord_msg)

def error(msg: str, interaction: Interaction = None, discord_msg: Message = None):
    log(msg, "error", interaction, discord_msg)

def log(msg: str, level: str = "info", interaction: Interaction = None, discord_msg: Message = None):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", end=" ", file=sys.stderr)
    print(f"[{level.upper():8}]", end=" ", file=sys.stderr)

    if interaction:
        print(f"(Guild {interaction.guild.name})", end=" ", file=sys.stderr)
        print(f"(Channel {interaction.channel.name})", end=" ", file=sys.stderr)
        print(f"(Nick {interaction.user.name})", end=" ", file=sys.stderr)
    elif discord_msg:
        print(f"(Guild {discord_msg.guild.name})", end=" ", file=sys.stderr)
        print(f"(Channel {discord_msg.channel.name})", end=" ", file=sys.stderr)
        print(f"(Nick {discord_msg.author.name})", end=" ", file=sys.stderr)

    print(msg, file=sys.stderr)
