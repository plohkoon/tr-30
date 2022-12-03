import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
# print(openai.Completion.create(
# model="text-davinci-003", prompt="Tell me why people should use the Python programming language but explain it like a 1970’s stoner", max_tokens=4000))
# print([model["id"] for model in openai.Model.list()['data']])

print(openai.Image.create(prompt="The man named Tall Randy",
      n=1, size="512x512", response_format="url"))
