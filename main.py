# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import os
import datetime
import inspect

from src.SFWInteractions import SFWInteractions
from src.Help import Help

from src.AdminCommands import AdminCommands
import src.EventsHandler

from src.Music.MusicFunctions import MusicFunctions
#from src.Music.Downloader import SongDownloader

#Potato#8999
#id = 694246129906483311
#public key = 70c7073417dc12f36435054a09b02e269b85acb1f89ded5724a8f9a20122f0e1

current_folder = os.path.dirname(os.path.abspath(__file__)) + "/"



################################
# On met le prefixe de la joie #
################################



intents = discord.Intents().all()
intents.members = True

client  = commands.Bot(command_prefix = "p!", help_command=None, intents = intents)


async def setup():
    client.add_cog(MusicFunctions(client))
    #client.add_cog(SongDownloader(client))
    client.add_cog(SFWInteractions(client))
    client.add_cog(Help(client))
    client.add_cog(AdminCommands(client))


###
#   Events
###


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name = "p!help"))
    print("Jui co")
    await setup()

@client.event
async def on_member_join(member):
    if "wati" in str(member.guild).lower():
        role = discord.utils.get(member.guild.roles, id = 466166843132870667)
        await member.add_roles(role)

@client.event
async def on_message(message):
    #Check si on reçoit un mp
    if not message.guild and message.author != client.user:
        message.content = "p!process_download " + message.content
        await client.process_commands(message)
    else:
        for name, func in inspect.getmembers(src.EventsHandler, inspect.isfunction):
            await func(client, message)
        if message.content.startswith("P!"):
            message.content = "p!" + message.content[2:]
        await client.process_commands(message)

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

@client.command()
async def reload(ctx):
    for cog in client.cogs():
        client.remove_cog(cog)

    client.add_cog(MusicFunctions(client))
    client.add_cog(SongDownloader(client))
    client.add_cog(SFWInteractions(client))
    client.add_cog(Help(client))
    client.add_cog(AdminCommands(client))


@client.command()
async def pong(ctx):
    await ctx.send('ping')

if __name__ == '__main__':
    token = open('.token','r').read()
    client.run(token)
