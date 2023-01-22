# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord import app_commands

def _help_embed_maker(client: discord.Client, entree: str = 'base') -> discord.Embed:
    if entree == 'base':
        embed = discord.Embed(color=0xf8e3e1)
        for cog in client.cogs:
            cmd_lst = ''
            for command in client.get_cog(cog).get_commands():
                if not command.hidden:
                    cmd_lst += f'`{command.name[1:]}` | {command.brief}\n'
            if not 'admin' in cog.lower() and not 'songd' in cog.lower():
                embed.add_field(name=f"​", value=cmd_lst[:-1],inline=False)
        embed.set_author(name=f"{client.user.display_name}'s help page",
            icon_url=client.user.avatar.url)
        return embed
    print('lmao prout')

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['h'], brief='Shows this page')
    async def _help(self, ctx, *, entree='base'):
        await ctx.send(embed=_help_embed_maker(self.client))

    @app_commands.command(name='help', description='Shows all my commands')
    async def help(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=_help_embed_maker(self.client))

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))