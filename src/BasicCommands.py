# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord import app_commands

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

    @commands.command(brief='Transforms an image into a fun gif')
    async def bubblify(self, ctx, link: str):
        if re.match(r'.*\.(png|jpeg|gif|jpg|webm)$', link):
            try:
                img_data = requests.get(link).content
                with open(link.split('/')[-1], 'wb') as handler:
                    handler.write(img_data)
                src.Utils.image.togif(link.split('/')[-1])
                src.Utils.image.booblify(link.split('/')[-1])
                await ctx.send(file=discord.File(link.split('/')[-1]))
                os.remove(link.split('/')[-1])
            except ValueError as e:
                await ctx.send(str(e))
        else:
            await ctx.send('Please only provide an image url, if the link you send is an image url feel free to report the issue')

    @app_commands.command(name='bubble', description='Adds a text bubble to an image')
    async def _bubblify(self, interaction: discord.Interaction, link: str):
        if re.match(r'^https\:\/\/tenor\.com\/view\/[a-z,A-Z,0-9-]+', link):
            link = src.Utils.image.tenorScrapper(link)
        if re.match(r'.*\.(png|jpeg|gif|jpg|webm)$', link):
            await interaction.response.defer()
            try:
                img_data = requests.get(link).content
                img_name = link.split('/')[-1]
                with open(img_name, 'wb') as handler:
                    handler.write(img_data)
                src.Utils.image.togif(img_name)
                img_name = img_name[:-4]+'.gif'
                src.Utils.image.booblify(img_name)
                await interaction.followup.send(file=discord.File(img_name))
                os.remove(img_name)
            except ValueError as e:
                await interaction.followup.send(str(e))
        else:
            await interaction.response.send_message(
                content='Please only provide image url, if the link you send is a image url feel free to report the issue',
                ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Basics(bot))