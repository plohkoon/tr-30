from discord.ext.commands import Cog, Bot
from discord import Interaction, File, Message
from discord.app_commands import command, guilds
from uuid import uuid4
from subprocess import run
from .constants import TR_GUILD, IABW_GUILD
import sys
from re import compile, MULTILINE, IGNORECASE, DOTALL
from . import logging

LATEX_REGEX = compile(r"```Latex\n(.+?)\n```",
                      flags=MULTILINE | IGNORECASE | DOTALL)
MATH_MODE_REGEX = compile(r"\\\[(.*?)\\\]", flags=MULTILINE | DOTALL)

def setup(bot: Bot):
    bot.add_cog(MathCog(bot))

class MathCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def write_file(self, content) -> str:
        file_name = str(uuid4())

        logging.debug(f"Writing latex to /tmp/{file_name}.tex")

        with open(f"/tmp/{file_name}.tex", "w") as f:
            f.write(
                "\\documentclass[varwidth=true, border=1pt]{standalone}")
            f.write("\\usepackage{xcolor}")
            f.write("\\begin{document}")
            f.write("\\pagecolor{white}")
            f.write(content)
            f.write("\\end{document}")

        return file_name

    def tex_to_pdf(self, file_name) -> None:
        infile = f"/tmp/{file_name}.tex"
        outfile = f"/tmp/{file_name}.pdf"

        logging.debug(f"Converting {infile} to {outfile}")
  
        # TODO deal with errors
        run(["pdflatex", "-interaction=nonstopmode",
            "-output-directory", "/tmp/", infile])

    def pdf_to_png(self, file_name) -> None:
        infile = f"/tmp/{file_name}.pdf"
        outfile = f"/tmp/{file_name}.png"

        logging.debug(f"Converting {infile} to {outfile}")
        # TODO deal with errors
        run(["convert", "-density", "300", infile,
            "-quality", "90", "+adjoin", "-resize", "150%", outfile])

    def make_png(self, expression: str) -> str:
        logging.debug("Making png")

        expression = MATH_MODE_REGEX.sub(r"$$\1$$", expression)

        file_name = self.write_file(expression)
        self.tex_to_pdf(file_name)
        self.pdf_to_png(file_name)

        return f"/tmp/{file_name}.png"

    @command(name="mathify", description="Renders a LaTeX expression")
    async def mathify(self, interaction: Interaction, expression: str) -> None:
        logging.info("Got command to render LaTeX expression", interaction)
        file_name = self.make_png(expression)

        await interaction.response.send_message(file=File(file_name))

    @Cog.listener("on_message")
    async def latex_codeblock(self, message: Message) -> None:
        if message.author == self.bot.user:
            return

        match = LATEX_REGEX.match(message.content)

        if match:
            logging.info("Found a LaTeX code block", message)
            file_name = self.make_png(match.group(1))
            await message.channel.send(file=File(file_name))
