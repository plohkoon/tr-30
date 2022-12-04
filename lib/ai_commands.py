from discord.app_commands import command, guilds
from discord import Interaction
from discord.ext.commands import Cog, Bot
from .constants import TR_GUILD, IABW_GUILD
from openai import Completion, Image
import sys


# TODO: Update this to chat bot when I can get it working
DEFAULT_MODEL = "text-davinci-003"

MODEL_LIST_TEXT = f"""
Here are the available models:

**Davinci** (Default):

Model Key: `text-davinci-003`

```
Davinci is the most capable model family and can perform any task the other models can perform and often with less instruction. For applications requiring a lot of understanding of the content, like summarization for a specific audience and creative content generation, Davinci is going to produce the best results. These increased capabilities require more compute resources, so Davinci costs more per API call and is not as fast as the other models.

Good at: Complex intent, cause and effect, summarization for audience
```

**Curie**:

Model Key: `text-curie-001`

```
Curie is extremely powerful, yet very fast. While Davinci is stronger when it comes to analyzing complicated text, Curie is quite capable for many nuanced tasks like sentiment classification and summarization. Curie is also quite good at answering questions and performing Q&A and as a general service chatbot.

Good at: Language translation, complex classification, text sentiment, summarization
```

**Babbage**:

Model Key: `text-babbage-001`

```
Babbage can perform straightforward tasks like simple classification. It’s also quite capable when it comes to Semantic Search ranking how well documents match up with search queries.

Good at: Moderate classification, semantic search classification
```

**Ada**:

Model Key: `text-ada-001`

```
Ada is usually the fastest model and can perform tasks like parsing text, address correction and certain kinds of classification tasks that don’t require too much nuance. Ada’s performance can often be improved by providing more context.

Good at: Parsing text, simple classification, address correction, keywords
```

For more information see https://beta.openai.com/docs/models/finding-the-right-model
"""

MODEL_LIST = [
    "text-davinci-003",
    "text-curie-001",
    "text-babbage-001",
    "text-ada-001",
]

MAX_TOKENS = {
    "text-davinci-003": 4000,
    "text-curie-001": 2000,
    "text-babbage-001": 2000,
    "text-ada-001": 2000,
}

IMAGE_SIZES = {
    "small": "256x256",
    "medium": "512x512",
    "large": "1024x1024",
}


class AICommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="chat", description="Chat with the AI")
    @guilds(TR_GUILD, IABW_GUILD)
    async def chat(self, interaction: Interaction, prompt: str, model: str = DEFAULT_MODEL) -> None:
        if model not in MODEL_LIST:
            await interaction.response.send_message("Model not found. To see available models use /list_models", ephemeral=True)
            return

        await interaction.response.defer()

        print(
            f"Generating a completion for the prompt: {prompt}", file=sys.stderr)

        response = Completion.create(
            model=model, prompt=prompt, max_tokens=MAX_TOKENS[model])

        # TODO: Any sort of error handling
        await interaction.followup.send(response["choices"][0]["text"])

    @command(name="list_models", description="List the available models")
    @guilds(TR_GUILD, IABW_GUILD)
    async def list_models(self, interaction: Interaction) -> None:
        await interaction.response.send_message(MODEL_LIST_TEXT, ephemeral=True)

    @command(name="visualize", description="Make an image")
    @guilds(TR_GUILD, IABW_GUILD)
    async def visualize(self, interaction: Interaction, prompt: str, size: str = "medium") -> None:
        if size not in IMAGE_SIZES:
            await interaction.response.send_message("Invalid image size. Use one of: small, medium, large", ephemeral=True)
            return

        await interaction.response.defer()

        print(
            f"Generating an image according to the prompt: {prompt}", file=sys.stderr)
        response = Image.create(
            prompt=prompt, size=IMAGE_SIZES[size], n=1, response_format="url", user=f"{interaction.user.id}")

        # TODO any sort of error handling
        await interaction.followup.send(response["data"][0]["url"])
