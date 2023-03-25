# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import os, re, youtube_dl

from ..Exceptions import NotDownloadable

class SongDownloader(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'noplaylist' : True,
        }

    @commands.command(hidden=True)
    async def process_download(self, ctx):
        #Check si on reçoit un mp
        if not ctx.message.guild and ctx.message.author != self.client.user:

            #Si on a un lien
            if re.match(r'.*https:\/\/(www\.)?youtu(\.?)be(\.com)?\/(watch\?v=)?.*', ctx.message.content):
                msg = ctx.message.content.split()
                for mot in msg:
                    if re.match(r'https:\/\/(www\.)?youtu(\.?)be(\.com)?\/(watch\?v=)?.*', mot):

                        #On dl ce son divin
                        with youtube_dl.YoutubeDL(self.opts) as ydl:
                            try:
                                await ctx.send(f'Starting download of `{mot}`')
                                try:
                                    ydl.download([mot])
                                except: raise NotDownloadable(media=mot,media_type="youtube")
                            except NotDownloadable as e:
                                await ctx.send(e.message)
                        try:
                            filenames = os.listdir()
                            for filename in filenames:
                                if filename.endswith('.mp3'):
                                    os.rename(filename, "./ressources/Musica/Update/" + filename)
                                    await ctx.send(f"OK j'ai downlod {filename}")
                        except:
                            print("Couldn't move a downloaded file for some reason")
            if len(ctx.message.attachments) > 0:
                music_types = ["m4a","mp3"]
                for attachment in ctx.message.attachments:
                    if any(attachment.filename.lower().endswith(typee) for typee in music_types):
                        await ctx.message.channel.send(f"Starting download of `{attachment.filename}`")
                        try:
                            try:
                                await attachment.save('./ressources/Musica/Update/' + attachment.filename)
                                await ctx.send(f"OK j'ai downlod `{attachment.filename}`")
                            except: raise NotDownloadable(media=attachment.filename, media_type='file')
                        except NotDownloadable as e:
                            await ctx.send(e.message)
