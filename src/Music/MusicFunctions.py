# -*- coding: utf-8 -*-
from src.Exceptions import MusicalError
from src.Music.SongPlayer import SongPlayer, song_to_str

import discord
from discord.ext import commands
from tinytag import TinyTag

import yt_dlp as youtube_dl
import os, re
import asyncio
import random
import json

from .YTDLSource import YTDLSource


###
#   Setting up constants
###



ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


try:
    musicas = os.listdir('./ressources/Musica/Main')
except FileNotFoundError:
    musicas = []



###
#   Background funcs
###



def matching_songs(regex:str, tab=musicas)->list:
    return [song for song in tab if re.match(rf'.*'+regex.lower()+'.*',song.lower())]

def info_from_id(id: str):
    url = url_from_id(id)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def url_from_id(id: str)->str:
    return f'https://www.youtube.com/watch?v={id}'

def show_progress(progress : float) -> str:
    percent = str(progress)[:4] + "%"
    bar = "■" * int(progress / 2) + (50 - int(progress / 2)) * "□"
    return percent + " | " + bar

def duration_detector(length):
    hours = length //3600
    length %= 3600
    mins = length // 60
    length %= 60
    seconds = length
    seconds = int(seconds) + 1

    return f"{hours}h {mins}m {seconds}s"

def gotoreview():
    r = os.listdir('./ressources/Musica/Update')
    for i in r:
        os.rename(f'./ressources/Musica/Update/{r}',f'./ressources/Musica/Review/{r}')

def make_embed(sg: SongPlayer) -> discord.Embed:
    tab = sg.songs
    counter = sg.counter
    embed = discord.Embed(title="Currently playing",
                          colour=0xFFc4d5,
                          description="")
    SongDisplaying = str('```ansi\n')
    for song in [sg.songs[i % len(sg.songs)]for i in range(sg.counter - 1, min(sg.counter + 20, len(sg.songs)-sg.counter-1))]:
      SongDisplaying += (song == sg.songs[sg.counter]) * "[0;31m" + song_to_str(song).split("(")[0].split(
        '[')[0] + '\n' + (song == sg.songs[sg.counter]) * "[0m"
    embed.add_field(name="", value=SongDisplaying + '```', inline=True)
    if sg.loop:
        embed.set_footer(text="The current song is on loop.")
    elif sg.loopqueue:
        embed.set_footer(text="The current playlist is on loop.")
    return embed


###
#   Cog Moment
###



class MusicFunctions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.musicPlayers = dict()
        self.message = None

    @commands.command(hidden=True)
    async def getfile(self, ctx, *, query=None):
        if query:
            match = matching_songs(query)
            if len(match) in range(1, 10):
                match = [discord.File('ressources/Musica/Main/'+k) for k in match]
                await ctx.author.send(content='Voici tes sons :', files=match)
        await ctx.message.delete()

    @commands.command(aliases=["p","pl","ambiance"],
    brief='Makes the bot play audio')
    async def play(self, ctx, *, url=None):
        await ctx.author.voice.channel.connect()

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.hybrid_command(aliases=["q","print"],
    brief='Shows the next songs to be played')
    async def queue(self, ctx, *, bullshit=None):
        if self.musicPlayers.get(ctx.guild,False):
            self.message = await ctx.send(embed=make_embed(self.musicPlayers[ctx.guild]))

    @commands.command(aliases=['search'], brief='Searches for a song in the databse', display_name="search")
    async def query(self, ctx, *, query=''):
        match = matching_songs(query)
        if (len(match)>20 or match==[]):
            await ctx.send(f'Please provide a better query, found {len(match)} songs')
        else:
            daMess = str()
            for song in match:
                daMess += song_to_str(song) + '\n'
            embed = discord.Embed(title='Matching songs :',description=daMess,color=0xffd1f3)
            await ctx.send(embed=embed)

    @commands.command(aliases=['calc'],brief='Does the maths for the length of the playlist')
    async def calculus(self, ctx, tab=musicas):
        totalsec = 0
        old_percent = 0
        failed = list()
        advancement = await ctx.send("Calculating total length of the playlist")
        try:
            for n in range(len(tab)):
                try:
                    tag = TinyTag.get("./ressources/Musica/Main/" + tab[n])
                    totalsec += tag.duration
                    if (100 * n/len(tab)) >= old_percent + 25:
                        await advancement.edit(content = show_progress(100 * n/len(tab)))
                        old_percent = 100 * n/len(tab)
                    assert tag.duration != 0
                except:
                    failed.append(tab[n])
            await advancement.edit(content = f"Calcul terminé, ça fait {duration_detector(totalsec)} en {len(tab)} musiques.")
        except:
            await ctx.send("Jo suis cassé")

    @commands.command(aliases=['s','sk','ski'],
    brief='Skips the current song')
    async def skip(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].skip()
            else: raise MusicalError("`skip`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['pr','prev'],
    brief='Plays the previous song')
    async def previous(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].previous()
            else: raise MusicalError("`previous`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['d','dco','disconnect', 'stop'],
    brief='Disconnects the bot from voice channel')
    async def deco(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                await self.musicPlayers[ctx.guild].deco()
            else: raise MusicalError("`deco`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['l','lop', 'boucle'],
    brief='Puts the current song on loop')
    async def loop(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].goloop()
            else: raise MusicalError("`loop`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['lq'],
    brief='Puts the current playlist on loop')
    async def loopqueue(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].goloopqueue()
            else: raise MusicalError("`loopqueue`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['random', 'melange'],
    brief='Shuffles the list of songs to come')
    async def shuffle(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].melangix()
            else: raise MusicalError("`shuffle`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['pt','ptop'],
    brief='Adds a song as first position in the wait list')
    async def playtop(self, ctx, *, query=None):
        print("processing playtop")
        if self.musicPlayers.get(ctx.guild, False):
            print("bot do be existing")
            await self.play(ctx=ctx, query=query)
            print("added to the queue")
            await self.musicPlayers[ctx.guild].playtop()
            print("job done")
        else:
            await self.play(ctx=ctx, query=query)

    @commands.command(aliases=['ps','pskip'],
    brief='Skips the current song to play the requested one')
    async def playskip(self, ctx, *, query=None):
        await self.playtop(ctx=ctx, query=query)
        await self.skip(ctx)

    @commands.command(aliases=['tocome'],
    brief='Shows the music waiting to join the playlist')
    async def upcoming(self, ctx):
        t='```'
        tab = os.listdir('./ressources/Musica/Update')
        for song in tab:
            if len(t+song)>+1990:
                await ctx.send(t+'```')
                t=f'```'
            t+=song_to_str(song) + '\n'
        await ctx.send(t+'```')


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicFunctions(bot))