# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

import asyncio

intents = discord.Intents().all()
intents.members = True

class Potabot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="p!", help_command=None, intents=intents)
        self.cogs_to_quire = [
            "src.Help",
            "src.AdminCommands",
            "src.SFWInteractions",
            "src.Music.MusicFunctions",
            "src.BasicCommands",
            "src.ClosedAI"
        ]

    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.listening, name="p!help"
            )
        )
        print("Potabot is online !")

    async def setup_hook(self):
        for cog in self.cogs_to_quire:
            await self.load_extension(cog)
        await self.tree.sync()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if "wati" in str(member.guild).lower():
            role = discord.utils.get(member.guild.roles, id=466166843132870667)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        cmd = ctx.command
        if isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            example = f"{ctx.prefix}{cmd.name} {cmd.signature.replace('[bullshit]','')}"
            await ctx.reply(f'Proper way to use {cmd.name} is {example}', delete_after=30)
        elif isinstance(error, commands.CommandNotFound):
            print(f'Failed on {ctx.message.content}')
        else:
            print(f'Error occured on {ctx.message.content} : \n {error}')

token = open('.token', 'r').read()
client = Potabot()
client.run(token)
