from discord.app_commands import CommandTree
from .client import TR30Client


class TR30CommandTree(CommandTree):
    def __init__(self, client: TR30Client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client.tree = self
