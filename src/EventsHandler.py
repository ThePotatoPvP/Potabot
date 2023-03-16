# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import re, asyncio

already_sent_wednesday = False

# All events shall have the same type

async def wednesday_event(client : discord.Client, message : discord.Message):
    global already_sent_wednesday
    if message.author!=client.user and message.created_at.weekday() == 2 and not already_sent_wednesday:
        channel = client.get_channel(717298046144217099)
        await channel.send('https://i.kym-cdn.com/photos/images/newsfeed/001/091/264/665.jpg')
        already_sent_wednesday = True
    elif re.match(r'.*(mercredi|wednesday).*', message.content.lower()) and message.author.id != client.user.id:
        await message.channel.send('Fake news ! Nous ne sommes aucunement mercredi !')
    elif message.created_at.weekday() != 2:
        already_sent_wednesday = False

async def latex_event(client : discord.Client, message : discord.Message):
    epic_latex = 'https://tenor.com/view/epic-latex-fail-latex-latex-fail-bad-latex-bad-tex-gif-26615851'
    if (message.channel.id == 717005277706059783) and (message.author.id == 510789298321096704) and ('Compile Error!' in message.content):
        shame = await message.channel.send(epic_latex)
        await asyncio.sleep(1200)
        await shame.delete()
