# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

import asyncio
import inspect
import sys

sys.path.append("..")

import src.Events.ScheduledEvents
import src.Events.TriggeredEvents

intents = discord.Intents().all()
intents.members = True

class Eventbot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="p!", help_command=None, intents=intents)

    async def on_ready(self):
        asyncio.create_task(scheduled_events_loop(self))
        print("Events are set up!")

    async def on_message(self, message):
        if message.author != self.user:
            for name, func in inspect.getmembers(src.Events.TriggeredEvents, inspect.iscoroutinefunction):
                await func(self, message)

    async def setup_hook(self):
        await self.tree.sync()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print('', endline=False)

async def scheduled_events_loop(client: discord.Client):
    while True:
        events = [func for name, func in inspect.getmembers(src.Events.ScheduledEvents,
                                                                predicate=lambda x: inspect.iscoroutinefunction(x))]
        tasks = [event(client) for event in events]
        await asyncio.gather(*tasks)
        await asyncio.sleep(1)


token = open('.token', 'r').read()
client = Eventbot()
client.run(token)
