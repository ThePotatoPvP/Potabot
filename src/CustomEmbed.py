# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

class CustomEmbed():
    def __init__(self, ctx, desc=None, title=None, footer=None,color=0xffd1f3, image=None, author=None):
        self.ctx = ctx
        self.desc = desc
        self.title = title 
        self.footer = footer 
        self.color = color 
        self.image = image 
        self.author = author

    def make(self)->list:
        if len(self.desc) >= 0:
            nth = discord.Embed(title=self.title,description=self.desc[:1900])
            if self.author:
                nth.set_author(name=f'{self.ctx.guild.name}',icon_url=self.ctx.guild.icon_url)
            if self.footer:
                nth.set_footer(text=self.footer)
            if self.image:
                nth.set_image(url=self.image)
            self.desc = self.desc[1900:]
            return [nth] + self.make()
        return []

# This shall remain unused as I have no clue how to make it work