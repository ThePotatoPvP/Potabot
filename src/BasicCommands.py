# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import os, re
import requests
import src.Utils.image

class Basics(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @commands.hybrid_command(brief='Answers pong')
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.hybrid_command(aliases=['say'],brief='Make the bot say something')
    async def send(self, ctx, *, text='issou'):
        await ctx.send(text)
        try:
            await ctx.message.delete()
        finally: pass

    @commands.hybrid_command(brief='Make the bot say something, privately')
    async def mp(self, ctx, target : discord.Member, *, text='pd'):
        try:
            await target.send(text)
            await ctx.message.delete()
        finally: pass

    @commands.command(brief='Transform an image into a fun gif')
    async def bubblify(self, ctx, link: str):
        if re.match(r'.*\.(png|jpeg|gif|jpg|webm)$', link):
            try:
                img_data = requests.get(link).content
                with open(link.split('/')[-1], 'wb') as handler:
                    handler.write(img_data)
                src.Utils.image.togif(link.split('/')[-1])
                src.Utils.image.booblify(link.split('/')[-1])
                try:
                    await ctx.send(file=discord.File(link.split('/')[-1]), ephemeral=True)
                finally:
                    await ctx.send(file=discord.File(link.split('/')[-1]))
                os.remove(link.split('/')[-1])
            except ValueError as e:
                await ctx.send(str(e))
        else:
            await ctx.send('Please only provide image url, if the link you send is a image url feel free to report the issue')

async def setup(bot: commands.Bot):
    await bot.add_cog(Basics(bot))