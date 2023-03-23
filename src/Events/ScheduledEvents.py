# -*- coding: utf-8 -*-

import discord
from discord.ext import tasks, commands

import datetime
import asyncio

from src.Events.decorators import ScheduledEvent

@ScheduledEvent(day_of_month=19)
async def funny_cat(client: discord.Client):
    channel = client.get_channel(821754215540981820)
    await channel.send("https://media.discordapp.net/attachments/763535317360705606/1076848517143859291/ssstik.io_1676808935083.mp4")


@ScheduledEvent(day_of_week=2)
async def wednesday(client: discord.Client):
    channel = client.get_channel(717298046144217099)
    await channel.send("https://i.kym-cdn.com/photos/images/newsfeed/001/091/264/665.jpg")

@ScheduledEvent(hour=16, minute=53)
async def foo(client: discord.Client):
    print('ayou le event')
    channel = client.get_channel(822927544948359228)
    await channel.send('foo')
