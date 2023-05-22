# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import re, asyncio
from src.Events.decorators import TriggeredEvent

def mkrgx(keyword="", keywords=None, before:bool=1, after:bool=1):
    if keywords is None: keywords = []
    if keyword: keywords.append(keyword)
    rgx = '('+ str.join('|', keywords)+')'
    if before: rgx = '(|.*\s)'+ rgx
    if after: rgx += '(\s.*|)'
    return rgx + r'(\.|\?|\:|\;|\,|\*|\$|\!|\s)*($|\n)'


@TriggeredEvent(rgx = mkrgx(keywords=['mercredi', 'wednesday']), guild_id=386474283804917760)
async def wednesday_event(client : discord.Client, message : discord.Message):
    if message.created_at.weekday() != 2:
        await message.channel.send('Fake news ! Nous ne sommes aucunement mercredi !')

@TriggeredEvent(rgx=mkrgx(keyword='Compile Error!'),
                user_id=510789298321096704,
                guild_id=386474283804917760,
                case_sensitive=True,
                chance=50,
                channel_id=717005277706059783)
async def latex_event(client : discord.Client, message : discord.Message):
    epic_latex = 'https://tenor.com/view/epic-latex-fail-latex-latex-fail-bad-latex-bad-tex-gif-26615851'
    shame = await message.channel.send(epic_latex)
    await asyncio.sleep(1200)
    await shame.delete()

@TriggeredEvent(rgx = mkrgx(keyword='quoi'))
async def coiffeur(client : discord.Client, message : discord.Message):
    await message.reply(message.content.split('quoi')[0]+'feur')

@TriggeredEvent(rgx = mkrgx(keywords=['oui', 'ui'], after=False))
async def ouistiti(client: discord.Client, message : discord.Message):
    await message.reply('stiti')

@TriggeredEvent(rgx = mkrgx(keywords=['ouais', 'oe', 'we', 'ouai'], after=False))
async def western(client: discord.Client, message : discord.Message):
    await message.reply('stern')

@TriggeredEvent(rgx = mkrgx(keywords=['non', 'nom'], after=False))
async def nombril(client: discord.Client, message : discord.Message):
    await message.reply('bril')