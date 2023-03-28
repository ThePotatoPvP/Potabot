# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

import asyncio
import inspect

import src.Events.ScheduledEvents
import src.Events.TriggeredEvents

intents = discord.Intents().all()
intents.members = True

class EventBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="p!", help_command=None, intents=intents)
        self.event_loop = asyncio.get_event_loop()

    async def on_ready(self):
        asyncio.create_task(scheduled_events_loop(self))
        print("Events are set up!")

    async def on_message(self, message):
        for name, func in inspect.getmembers(
            src.Events.TriggeredEvents, inspect.iscoroutinefunction
        ):
            self.event_loop.create_task(func(self, message))

        await self.process_commands(message)

    async def setup_hook(self):
        await self.tree.sync()

async def scheduled_events_loop(client: discord.Client):
    while True:
        events = [func for name, func in inspect.getmembers(src.Events.ScheduledEvents, 
                                                                predicate=lambda x: inspect.iscoroutinefunction(x))]                                                          
        tasks = [event(client) for event in events]
        print("Démarrage de la boucle pour les événements")
        await asyncio.gather(*tasks)
        await asyncio.sleep(1)