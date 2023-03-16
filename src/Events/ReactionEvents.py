# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import re, asyncio


async def wednesday_event(client : discord.Client, message : discord.Message):
    if message.author!=client.user and message.created_at.weekday() == 2 and re.match(r'.*(mercredi|wednesday).*', message.content.lower()):
        await message.channel.send('Fake news ! Nous ne sommes aucunement mercredi !')

async def latex_event(client : discord.Client, message : discord.Message):
    epic_latex = 'https://tenor.com/view/epic-latex-fail-latex-latex-fail-bad-latex-bad-tex-gif-26615851'
    if (message.channel.id == 717005277706059783) and (message.author.id == 510789298321096704) and ('Compile Error!' in message.content):
        shame = await message.channel.send(epic_latex)
        await asyncio.sleep(1200)
        await shame.delete()
