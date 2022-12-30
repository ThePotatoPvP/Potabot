# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = 'p!'

    @commands.command(aliases=['h'], brief='Shows this page')
    async def help(self, ctx, *, input='base'):
        if input == 'base':
            embed = discord.Embed(color=0xf8e3e1)
            for cog in self.client.cogs:
                cmd_lst = ''
                for command in self.client.get_cog(cog).get_commands():
                    if not command.hidden:
                        cmd_lst += f'`{command.name}` | {command.brief}\n'
                if not 'admin' in cog.lower() and not 'songd' in cog.lower():
                    embed.add_field(name=f"​", value=cmd_lst[:-1],inline=False)
        embed.set_author(name=f"{self.client.user.display_name}'s help page",
            icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
