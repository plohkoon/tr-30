from discord.ext.commands import Cog, Bot
from discord import Interaction, File
from discord.app_commands import command, guilds
from uuid import uuid4
from subprocess import run
from .constants import TR_GUILD, IABW_GUILD


class MathCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    def write_file(self, content) -> str:
        file_name = str(uuid4())

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

        # TODO deal with errors
        run(["pdflatex", "-interaction=nonstopmode",
            "-output-directory", "/tmp/", infile])

    def pdf_to_png(self, file_name) -> None:
        infile = f"/tmp/{file_name}.pdf"
        outfile = f"/tmp/{file_name}.png"

        # TODO deal with errors
        run(["convert", "-density", "300", infile,
            "-quality", "90", "+adjoin", "-resize", "150%", outfile])

    @ command(name="mathify", description="Renders a LaTeX expression")
    @ guilds(TR_GUILD, IABW_GUILD)
    async def mathify(self, interaction: Interaction, expression: str) -> None:
        file_name = self.write_file(expression)
        self.tex_to_pdf(file_name)
        self.pdf_to_png(file_name)

        await interaction.response.send_message(file=File(f"/tmp/{file_name}.png"))
