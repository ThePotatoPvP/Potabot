import discord

class FakeContext():
    def __init__(self, message):
        self.message = message

    @property
    def author(self):
        return self.message.author

    @property
    def guild(self):
        return self.message.guild
        
    async def send(self, content: str=None, embed: discord.Embed=None):
        await self.message.channel.send(content=content, embed=embed)