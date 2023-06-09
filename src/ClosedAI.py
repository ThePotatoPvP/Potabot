import discord
from discord.ext import commands

class ClosedAI(commands.Cog):
    def __init__(self, client):
        self.client = client

async def setup(bot: commands.Bot):
    await bot.add_cog(ClosedAI(bot))