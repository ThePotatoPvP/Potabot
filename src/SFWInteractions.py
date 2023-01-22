# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

import random

class sfw_init():
    def __init__(self):
        self.punchlines = open("./ressources/SFW_Interactions/punchlines.txt","r").readlines()
        self.disquettes = open("./ressources/SFW_Interactions/disquettes.txt","r").readlines()
        self.emotes = open("./ressources/SFW_Interactions/emotes.txt","r").readlines()
        self.eight_b = open("./ressources/SFW_Interactions/eight_b.txt","r").readlines()
        self.images = open("./ressources/SFW_Interactions/images.txt","r").readlines()

class SFWInteractions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.values = sfw_init()

    @commands.hybrid_command(brief='Answers pong')
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.hybrid_command(aliases=["8b","8ball"],
    brief='To get true wisdom')
    async def eight_ball(self, ctx, *, wonder=None):
        await ctx.send(random.choice(self.values.eight_b))

    @commands.hybrid_command(aliases=["clash","punchline"],
    brief='Sends a masterclass punchline to roast someone')
    async def roast(self, ctx, target : discord.Member, * , bullshit = None):
        desc = random.choice(self.values.punchlines)
        title = f'From {ctx.author.display_name} to {target.display_name}'
        e = discord.Embed(title=title, description=desc, color = 0xffd1f3)
        await ctx.send(embed=e)

    @commands.hybrid_command(aliases=['disquette','pecho'],
    brief='Sends a cute pickupline to secure a date')
    async def luv(self, ctx, target : discord.Member, *, bullshit = None):
        desc = random.choice(self.values.disquettes)
        title = f'From {ctx.author.display_name} to {target.display_name}'
        e = discord.Embed(title=title, description=desc, color = 0xffd1f3)
        await ctx.send(embed=e)

    @commands.hybrid_command(aliases=['image'], 
    brief='Sends a pic of a potato')
    async def pic(self, ctx):
        e = discord.Embed(title="Here's a potato pic", color=0xffd1f3)
        e.set_image(url= random.choice(self.values.images))
        await ctx.send(embed = e)

    @commands.hybrid_command(aliases=['rdm'],brief='Sends an emote judged funny')
    async def emote(self, ctx):
        await ctx.send(random.choice(self.values.emotes))

    @commands.hybrid_command(aliases=['say'],brief='Make the bot say something')
    async def send(self, ctx, *, text='issou'):
        await ctx.send(text)
        try:
            await ctx.message.delete()
        except: pass

    @commands.hybrid_command(brief='Make the bot say something, privately')
    async def mp(self, ctx, target : discord.Member, *, text='pd'):
        try:
            await target.send(text)
            await ctx.message.delete()
        except: pass
        
async def setup(bot: commands.Bot):
    await bot.add_cog(SFWInteractions(bot))