# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prefix = 'p!'


    async def _help_embed_maker(self, input='base') -> discord.Embed:
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

    @commands.command(aliases=['h'], brief='Shows this page', display_name="help")
    async def help(self, ctx, *, input='base'):
        await ctx.send(embed=self._help_embed_maker())

    @app_commands.command(name='help', description='Shows all my commands')
    async def _help(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self._help_embed_maker)

