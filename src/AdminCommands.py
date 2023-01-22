# -*- coding: utf-8 -*-
import discord
from discord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(hidden=True)
    @commands.has_permissions(kick_members=True) 
    async def kick(self, ctx, member : discord.Member,*, reason = "surplus de wati-bizarrerie"):
        """Permet de kick qlqun"""
        await member.send("Yo la frappe \n Tu t'es fait **kick** du wati-serv pour : "+reason +"\n \n CHEH :woman_in_manual_wheelchair:")
        await member.kick(reason = reason)

    @commands.hybrid_command(aliases=['clear'], hidden=True)
    @commands.has_permissions(manage_messages = True)
    async def clean(self, ctx, number:int):
        if number<=16:
            await ctx.channel.purge(limit=int(number))
        else:
            await ctx.reply(f'Cannot delete more than 15 messages at once', delete_after=10)

    @commands.hybrid_command(hidden=True)
    @commands.is_owner()
    async def statut(self,ctx,*,statut=''):
        if statut == "":
            await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name = "p!help"))
        else:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(kk))
        await ctx.message.delete()

    @commands.hybrid_command(hidden=True)
    @commands.is_owner()
    async def serverslist(self, ctx):
        letxt = str("```")
        guilds = await self.client.fetch_guilds(limit=150).flatten()
        for server in guilds:
            l = len(server.name)
            letxt += str(server.name) + (30-l)*" " + ":" + str(server.id) + "\n"
        letxt += "```"
        await ctx.author.send(letxt)
        await ctx.message.delete()

    @commands.hybrid_command(hidden=True)
    @commands.is_owner()
    async def channelslist(self, ctx, serverid):
        """Donne la liste des channels d'un server et leur id"""
        f = open("temp.txt", "w")
        server = self.client.get_guild(int(serverid))
        for channel in server.text_channels:
            l = len(channel.name)
            f.write( channel.name + (30-l)*" " + str(channel.id) + "\n" )
        f.close()
        await ctx.author.send(f"Here's the list of all channles in server : {serverid}",file = discord.File("temp.txt"))
        f = open("temp.txt", "w")
        f.truncate(0)
        f.close()
        await ctx.message.delete()

    @commands.hybrid_command(hidden=True)
    @commands.is_owner()
    async def getinvite(self, ctx, channelid):
        channel = self.client.get_channel(int(channelid))
        inv = await channel.create_invite()
        await ctx.author.send(inv)
        await ctx.message.delte()

    @commands.hybrid_command(hidden=True)
    @commands.is_owner()
    async def attachmentslist(self, ctx, channelid):
        """Donne la liste des attachements dans le channel"""
        f = open("temp.txt", "w")
        channel = self.client.get_channel(int(channelid))
        messages = await channel.history(limit=None, oldest_first=True).flatten()
        print(f"je got la listen de longueur : {len(messages)}")
        for message in messages:
            if message.attachments:
                for image in message.attachments:
                    f.write(str(image.url) + "\n")
            elif "http" in message.content:
                for mot in message.content.split():
                    if mot.startswith("http"):
                        f.write(mot + "\n")
        f.close()
        await ctx.author.send(f"Here's the list of all images in channel : {channelid}",file = discord.File("temp.txt"))
        f = open("temp.txt", "w")
        f.truncate(0)
        f.close()
        await ctx.message.delete()