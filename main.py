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
from src.FakeContext import FakeContext

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
    await client.add_cog(MusicFunctions(client))
    await client.add_cog(SFWInteractions(client))
    await client.add_cog(AdminCommands(client))


###
#   Events
###



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

@client.command()
async def reload(ctx):
    for cog in client.cogs():
        client.remove_cog(cog)

    client.add_cog(MusicFunctions(client))
    client.add_cog(SFWInteractions(client))
    client.add_cog(AdminCommands(client))


class Potabot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="p!",help_command=None,intents=intents,application_id=694246129906483311)
        self.cogs_to_quire = ["src.Help"
                            #"src.AdminCommands",
                            #"src.Music.MusicFunctions"
                            ]
    
    async def on_ready(self):
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name = "p!help"))
        print("Jui co")
        await setup()
        
    async def on_message(self, message):
        if not message.guild and message.author != client.user:
            message.content = "p!process_download " + message.content
            await client.process_commands(message)
        else:
            print("en eussou el messago")
            for name, func in inspect.getmembers(src.EventsHandler, inspect.isfunction):
                await func(client, message)
            if message.content.startswith("p!"):
                cmd = message.content.split()[0][2:]
                for cog in client.cogs:
                    for command in client.get_cog(cog).get_commands():
                        if command.name == '_' + cmd or cmd in command.aliases:
                            await command.__call__(await client.get_context(message))

    async def setup_hook(self):
        for cog in self.cogs_to_quire:
            await self.load_extension(cog)
        await client.tree.sync()


if __name__ == '__main__':
    client = Potabot()
    token = open('.token','r').read()
    client.run(token)
