# -*- coding: utf-8 -*-
from src.Music.YTDLSource import YTDLSource

import discord
from tinytag import TinyTag
import asyncio
import random
import os

def getVidFromLink(url:str):
    #song = await YTDLSource.from_url(url, loop=False, stream=True)
    return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url))

def song_to_str(song) -> str:
    if type(song) is str: return song[:-4]
    return song[1]

async def update_annonce(client):
    musiks = os.listdir("Musica/Review")
    monstr = ""
    channel = client.get_channel(396377450550001674)
    annonce = discord.Embed(title="Grande nouvelle RedPilled people", description="Votre playlist préférée a de nouveaux ajouts !", color=0xffd1f3)
    for musik in musiks:
        if len(monstr + "- "+musik[:-4] + "\n") > 1024:
                annonce.add_field(name = "Nouvelles musiques", value = monstr, inline = False)
                annonce.add_field(name = "Participez !", value = "N'hésitez pas à venir en voc, profiter des toutes dernières musiques, comme de celles qui rythment ce discord depuis sa création. Et n'oubliez pas que vous pouvez faire vos propositions en envoyant des liens youtube au bot en mp. En espérant vous ambiencer bientôt", inline = False)
                await channel.send(embed = annonce)
                annonce = discord.Embed(title="Grande nouvelle RedPilled people", description="Votre playlist préférée a de nouveaux ajouts !", color=0xffd1f3)
                monstr = str()
        monstr += "- "+musik[:-4] + "\n"
        os.rename("Musica/Review/"+musik, "Musica/Main/"+musik)
    annonce.add_field(name = "Nouvelles musiques", value = monstr, inline = False)
    annonce.add_field(name = "Participez !", value = "N'hésitez pas à venir en voc, profiter des toutes dernières musiques, comme de celles qui rythment ce discord depuis sa création. Et n'oubliez pas que vous pouvez faire vos propositions en envoyant des liens youtube au bot en mp. En espérant vous ambiencer bientôt", inline = False)
    await channel.send(embed = annonce)
    await channel.send("<@&848629399422500904>")

class SongPlayer():
    """Creates an instance of the bot to play music in a voice channel

        3 possible modes, the names are rather intuitives so I  won't explain
        -casu
        -review
        -focus
        """
    def __init__(self, musicPlayers: dict, context: discord.ext.commands.Context, guild: discord.Guild, songs: list[str|tuple], client: discord.Client, mode: str = "casu"):
        self.guild = guild
        self.add_songs(songs)
        self.ctx = context
        self.bot = client
        self.loop, self.loopqueue = False, False
        self.mode = mode
        self.counter = 0
        self.musicPlayers = musicPlayers

    @property
    def songs_left(self):return len(self.songs)-self.counter

    def add_songs(self, songs : list) -> None:
        try:
            self.songs += songs
        except AttributeError:
            self.songs = songs

    def is_alone(self) -> bool:
        try:
            aim_channel = self.voice_channel
            return len(aim_channel.members) < 2
        except: return True

    def time_left(self) -> int:
        totalsec = int()
        for i in range(self.songs_left):
            try:
                tag = TinyTag.get("./ressources/Musica/Main/" + self.songs[self.counter+i])
                print(f"{100*i/len(self.songs_left)} %")
                totalsec += tag.duration
            except: pass
        return totalsec

    def skip(self) -> None:
        self.player.stop()

    def previous(self) -> None:
        self.counter -= 2
        self.skip()

    def goloop(self) -> None:
        self.loop = not self.loop
        self.loopqueue = False

    def goloopqueue(self) -> None:
        self.loopqueue = not self.loopqueue
        self.loop = False

    def playtop(self) -> None:
        s = self.songs[-1]
        for i in range(self.songs_left-2,self.counter,-1):
            self.songs[i+1] = self.songs[i]
        self.songs[self.counter] = s

    def melangix(self) -> None:
        """Shuffles the queue while keeping the previous songs at their place"""
        if self.player.is_playing():
            if self.loopqueue:
                rest = self.songs[::self.counter] + self.songs[self.counter+1::]
                random.shuffle(rest)
                self.songs = rest[::self.counter] + [self.songs[self.counter]] + rest[self.counter::]
            else:
                rest = self.songs[self.counter+1::]
                random.shuffle(rest)
                self.songs = self.songs[::self.counter] + rest
        else:
            random.shuffle(self.songs)

    async def deco(self) -> None:
        self.loop = False
        self.loopqueue = False

        try:
            self.player.stop()
            await self.ctx.voice_client.disconnect()
            if self.mode == 'review':
                await update_annonce(self.bot)
        except:
            pass
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name = 'p!help'))
        del self.musicPlayers[self.guild]

    async def prepare_next(self):
        # Make first song clean if from youtube and not ready yet
        if type(self.songs[self.counter]) is tuple and type(self.songs[self.counter][0]) is str:
            self.songs[self.counter] = (await YTDLSource.from_url(self.songs[self.counter][0], stream=True),self.songs[self.counter][1])

        # Make song readable
        if type(self.songs[self.counter]) is str:
            if self.mode == 'review': media = './ressources/Musica/Review/' + self.songs[self.counter]
            else: media = './ressources/Musica/Main/' + self.songs[self.counter]
            self.media = discord.FFmpegPCMAudio(media)
        else:
            self.media = self.songs[self.counter][0]
        self.title = song_to_str(self.songs[self.counter])

        # Prepare next song if from youtube
        if self.songs_left>=2 and type(self.songs[self.counter+1]) is tuple:
            self.songs[self.counter+1] = (getVidFromLink(self.songs[self.counter+1][0]), self.songs[self.counter+1][1])

    async def play(self):
        user=self.ctx.author
        self.voice_channel=user.voice.channel
        # make first song readable if it's form youtube
        if self.songs_left and type(self.songs[self.counter]) is tuple:
            self.songs[0] = (getVidFromLink(self.songs[0][0]),self.songs[0][1])

        # only play music if user is in a voice channel
        if self.voice_channel:
            await self.voice_channel.connect()
            self.player = self.voice_client
            self.melangix()
            while self.songs_left:
                await self.prepare_next()
                self.player.play(self.media, after=lambda e: print(f'Player error: {e}') if e else None)
                #Changing status, only for the main server
                if str(self.guild.id) == '386474283804917760' and type(self.songs[self.counter]) is str:
                    await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(self.title))
                while self.player.is_playing():
                    await asyncio.sleep(1)

                if self.is_alone():
                    await self.deco()

                if not self.loop:
                    self.counter += 1

            if self.loopqueue:
                self.counter = 0
                await self.play()
            else:
                await self.deco()
        else:
            await self.ctx.send("Vas dans un vocal avant de m'appeler, idiot")