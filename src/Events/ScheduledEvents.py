# -*- coding: utf-8 -*-

import discord
from discord.ext import tasks, commands

import datetime
import asyncio


from src.Events.decorators import ScheduledEvent

import src.Utils.reddit
'''

This file should only countain ScheduledEvents functions formatted as the following :
@ScheduledEvent()
async def <func-name>(client : discord.Client):
    ...

'''

@ScheduledEvent(day_of_month=19)
async def funny_cat(client: discord.Client):
    channel = client.get_channel(821754215540981820)
    await channel.send("https://media.discordapp.net/attachments/763535317360705606/1076848517143859291/ssstik.io_1676808935083.mp4")


@ScheduledEvent(day_of_week=2)
async def wednesday(client: discord.Client):
    channel = client.get_channel(717298046144217099)
    await channel.send("https://i.kym-cdn.com/photos/images/newsfeed/001/091/264/665.jpg")

@ScheduledEvent(hour=13, minute=00)
async def watinewsmidi(client: discord.Client):
    print('omjej c l event ')
    imgz = src.Utils.reddit.grab_img('rienabranler')
    channel = client.get_channel(734814108159049737)
    await channel.send(f":rotating_light: Flash Info :rotating_light:\n Wati-Bonjourr à tous, voici le titre le ce matin.")
    await channel.send(imgz[0])

@ScheduledEvent(hour=20, minute=00)
async def watinewssoir(client: discord.Client):
    print('omjej c l event ')
    imgz = src.Utils.reddit.grab_img('rienabranler')
    channel = client.get_channel(734814108159049737)
    await channel.send(f":rotating_light: Flash Info :rotating_light:\n Wati-Bonsoir à tous, voici l'actualité qui a marqué cette journée.")
    await channel.send(imgz[0])
    await channel.send(imgz[2])