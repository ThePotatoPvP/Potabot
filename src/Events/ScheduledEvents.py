# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import re, asyncio
import datetime


@tasks.loop(hours=24)
async def nineteenth(client : discord.Client):
    date = datetime.datetime.now()
    if date.day == 19:
        channel = client.get_channel(821754215540981820)
        await channel.send("https://media.discordapp.net/attachments/763535317360705606/1076848517143859291/ssstik.io_1676808935083.mp4")

@tasks.loop(hours=24)
async def wednesday(client : discord.Client):
    date = datetime.datetime.now()
    if date.weekday() == 2:
        channel = client.get_channel(717298046144217099)
        await channel.send("https://i.kym-cdn.com/photos/images/newsfeed/001/091/264/665.jpg")