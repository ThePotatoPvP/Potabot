import discord
from discord.ext import commands
from discord import app_commands

from src.Utils.ScrapAI.text import generate_response

class ClosedAI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="askgpt4", description="Ask GPT4 for a response")
    async def askgpt4(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()

        gpt4_response = await generate_response(prompt)
        await interaction.followup.send(gpt4_response[0])

        for k in range(1, len(gpt4_response)):
            interaction.channel.send(gpt4_response[k])

async def setup(bot: commands.Bot):
    await bot.add_cog(ClosedAI(bot))