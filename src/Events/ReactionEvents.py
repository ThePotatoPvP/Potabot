# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import re, asyncio
from src.Events.decorators import TriggeredEvent

@TriggeredEvent(keyword='(mercredi|wednesday)', guild_id=386474283804917760)
async def wednesday_event(client : discord.Client, message : discord.Message):
    if message.created_at.weekday() != 2:
        await message.channel.send('Fake news ! Nous ne sommes aucunement mercredi !')

@TriggeredEvent(keyword='Compile Error!',
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

