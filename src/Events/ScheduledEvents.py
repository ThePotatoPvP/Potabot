# -*- coding: utf-8 -*-

import discord
from discord.ext import tasks, commands

import datetime
import asyncio

class ScheduledEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __start_loops__(self):
        await self.teeest.start()

    @tasks.loop(hours=24.0)
    async def nineteenth(self):
        date = datetime.datetime.now()
        if date.day == 19:
            channel = self.bot.get_channel(821754215540981820)
            await channel.send("https://media.discordapp.net/attachments/763535317360705606/1076848517143859291/ssstik.io_1676808935083.mp4")

    @tasks.loop(hours=24.0)
    async def wednesday(self):
        date = datetime.datetime.now()
        print('test credi')
        if date.weekday() == 2:
            print('c le credi')
            channel = self.bot.get_channel(717298046144217099)
            await channel.send("https://i.kym-cdn.com/photos/images/newsfeed/001/091/264/665.jpg")


async def setup(bot: commands.Bot):
    await bot.add_cog(ScheduledEvents(bot))