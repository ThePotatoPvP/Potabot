# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import os
import inspect
import asyncio
import importlib
from concurrent.futures import ThreadPoolExecutor

import src.Events.ReactionEvents
import src.Events.ScheduledEvents

from src.Music.MusicFunctions import MusicFunctions
#from src.Music.Downloader import SongDownloader

#Potato#8999
#id = 694246129906483311
#public key = 70c7073417dc12f36435054a09b02e269b85acb1f89ded5724a8f9a20122f0e1

current_folder = os.path.dirname(os.path.abspath(__file__)) + "/"

import pytz
tz = pytz.timezone('Europe/Paris')

################################
# On met le prefixe de la joie #
################################



intents = discord.Intents().all()
intents.members = True

client  = commands.Bot(command_prefix = "p!", help_command=None, intents = intents)

###
#   Events
###



@client.command()
async def reload(ctx):
    for cog in client.cogs():
        client.remove_cog(cog)


class Potabot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="p!",help_command=None,intents=intents,)
        self.cogs_to_quire = ["src.Help",
                            "src.AdminCommands",
                            "src.SFWInteractions",
                            "src.Music.MusicFunctions"
                            ]

    async def on_ready(self):
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name = "p!help"))
        asyncio.create_task(scheduled_events_loop(client))
        print("Potabot is online !")

    async def on_message(self, message):
        for name, func in inspect.getmembers(src.Events.ReactionEvents, inspect.iscoroutinefunction):
            await func(client, message)
        await client.process_commands(message)

    async def setup_hook(self):
        for cog in self.cogs_to_quire:
            await self.load_extension(cog)
        await client.tree.sync()

    @client.event
    async def on_member_join(member):
        if "wati" in str(member.guild).lower():
            role = discord.utils.get(member.guild.roles, id = 466166843132870667)
            await member.add_roles(role)

    @client.event
    async def on_command_error(ctx, error):
        cmd = ctx.command
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            example = f"{ctx.prefix}{cmd.name} {cmd.signature.replace('[bullshit]','')}"
            await ctx.reply(f'Proper way to use {cmd.name} is {example}', delete_after=30)
        elif isinstance(error, commands.CommandNotFound):
            print(f'Failed on {ctx.message.content}')
        else:
            print(f'Error occured on {ctx.message.content} : \n {error}')

async def scheduled_events_loop(client: discord.Client):
    # Call the wrapped function of each ScheduledEvent decorator at the scheduled time
    while True:
        for name, func in inspect.getmembers(src.Events.ScheduledEvents, inspect.iscoroutinefunction):
            await func(client)

if __name__ == '__main__':
    client = Potabot()
    token = open('.token','r').read()

    client.run(token)
