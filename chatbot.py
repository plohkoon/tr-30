import os
from dotenv import load_dotenv
import openai
import discord
from discord import app_commands, Interaction, Message
from random import random
import re
from datetime import datetime

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
discord_key = os.getenv("DISCORD_KEY")

discord_client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(discord_client)

# TODO REMOVE ME
tr_guild = discord.Object(id=737417939724009532)
iabw_guild = discord.Object(id=322608945833443328)

mark_id = 358490770896060417
tr_id = 99235095214313472
dyl_user = 174296942484914176

spoiler_regex = re.compile(r'\|\|(.+?)\|\|')
based_regex = re.compile(r'based', re.IGNORECASE)

# TODO: Update this to chat bot when I can get it working
DEFAULT_MODEL = "text-davinci-003"

MODEL_LIST_TEXT = f"""
Here are the available models:
```
THE_MODELS
```

The default is {DEFAULT_MODEL}

Don't know what any of this means? Check out the https: // beta.openai.com/docs/models/models for more information.
"""


@discord_client.event
async def on_ready():
    print(f'{discord_client.user} has connected to Discord!')


@discord_client.event
async def on_message(message: Message):
    if message.author == discord_client.user:
        return

    print(message.content)

    if spoiler_regex.match(message.content) and random() < 0.5:
        await message.channel.send(f"Hey <@{mark_id}>, {message.author.nick} said something you might want to see!")

    if message.author.id == dyl_user and based_regex.match(message.content):
        await message.channel.send(f"Hey <@{dyl_user}>, https://youtu.be/RUExiGNHF5s")


@tree.command(name="helloworld", description="Hello World", guilds=[tr_guild, iabw_guild])
async def hello_world(interaction: Interaction, argument: str):
    await interaction.response.send_message(f"Hello {argument}!")


@tree.command(name="chat", description="Chat with the AI", guilds=[tr_guild, iabw_guild])
async def chat(interaction: Interaction, prompt: str, model: str = DEFAULT_MODEL):
    print(interaction.expires_at, datetime.now())
    await interaction.response.defer()

    response = openai.Completion.create(
        model=model, prompt=prompt, max_tokens=4000)

    if interaction.command_failed or interaction.is_expired():
        print("The chat request likely timed out")

    # TODO: Any sort of error handling
    await interaction.followup.send(response["choices"][0]["text"])


@tree.command(name="list_models", description="List the available models", guilds=[tr_guild, iabw_guild])
async def list_models(interaction: Interaction):
    response = openai.Model.list()
    models = [model["id"] for model in response["data"]]

    text = re.sub(r'THE_MODELS', '\n'.join(models), MODEL_LIST_TEXT)
    await interaction.response.send_message(text, ephemeral=True)


@tree.command(name="sync", description="Owner Only", guilds=[tr_guild, iabw_guild])
async def sync(interaction: Interaction):
    if interaction.user.id == 99235095214313472:
        await tree.sync(guild=interaction.guild)
        print("Command tree synced")
        await interaction.response.send_message("Command tree synced", ephemeral=True)
    else:
        await interaction.response.send_message("Piss off, you're not my dad", ephemeral=True)


if __name__ == "__main__":
    discord_client.run(discord_key)
