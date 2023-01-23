# -*- coding: utf-8 -*-
from ..Exceptions import MusicalError

import discord
from discord.ext import commands
from tinytag import TinyTag

import youtube_dl
import os, re 
import asyncio
import random
import json


###
#   Setting up constants
###


ytdl_format_options ={
    'format' : 'bestaudio/best',
    'restrictfilenames' : True,
    'nocheckcertificate' : True,
    'ignoreerrors' : False,
    'logtostderr' : False,
    'quiet' : True,
    'no_warnings' : True,
    'default_search' : 'auto',
    'source_address' : '0.0.0.0'
}

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

ffmpeg_opts = {
    'options': '-vn'
}

musicas = os.listdir('./ressources/Musica/Main')



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

def url_from_id(id:str)->str:
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

def song_to_str(song):
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

def gotoreview():
    r = os.listdir('./ressources/Musica/Update')
    for i in r:
        os.rename(f'./ressources/Musica/Update/{r}',f'./ressources/Musica/Review/{r}')

def make_embed(tab: list, counter: int) -> discord.Embed:
    embed = discord.Embed(title="Currently playing",
                          colour=0xFFc4d5,
                          description="")
    SongDisplaying = str('```ansi\n')
    for song in [tab[i % len(tab)]for i in range(counter - 1, counter + 20)]:
      SongDisplaying += (song == tab[counter]) * "[0;31m" + song.split("(")[0].split(
        '[')[0] + '\n' + (song == tab[counter]) * "[0m"
    embed.add_field(name="", value=SongDisplaying + '```', inline=True)
    return embed

###
#   Player Class
###

async def getVidFromLink(url:str):
    song = await YTDLSource.from_url(url, loop=False, stream=True)
    return song

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source, volume)
        self.data=data
        self.url=''

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, play=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f'ytsearch:{url}',download=not stream or play))

        try:
            data = data['entries'][0]
        except: pass
        try:
            filename = data['url'] if stream else ytdl.prepare_filename(data)
        except: filename = ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_opts), data=data)

class song_player():
    """Creates an instance of the bot to play music in a voice channel
    
        3 possible modes, the names are rather intuitives so I  won't explain
        -casu
        -review
        -focus
        """
    def __init__(self, musicPlayers, context, guild, songs, client, mode):
        self.guild = guild 
        self.add_songs(songs)
        self.ctx = context
        self.bot = client
        self.loop, self.loopqueue = False, False
        self.mode=mode
        self.counter=0
        self.queue_message = None
        self.musicPlayers = musicPlayers

    @property
    def songs_left(self):return len(self.songs)
    
    def add_songs(self, songs : list):
        try:
            self.songs += songs
        except AttributeError:
            self.songs = songs

    def is_alone(self):
        try:
            aim_channel = self.voice_channel
            return len(aim_channel.members) < 2
        except: return True 

    def time_left(self):
        totalsec = int()
        for i in range(self.songs_left):
            try:
                tag = TinyTag.get("./ressources/Musica/Main/" + self.songs[i])
                print(f"{100*i/len(self.songs_left)} %")
                totalsec += tag.duration
            except: pass
        return totalsec

    def skip(self):
        self.player.stop()

    def previous(self):
        self.counter -= 2
        self.skip
        
    def goloop(self):
        self.loop = not self.loop
        self.loopqueue = False

    def goloopqueue(self):
        self.loopqueue = not self.loopqueue
        self.loop = False

    def playtop(self):
        s = self.songs[-1]
        for i in range(self.songs_left-2,1,-1):
            self.songs[i+1] = self.songs[i]
        self.songs[1] = s

    def melangix(self):
        if self.player.is_playing():
            rest = self.songs[1:]
            random.shuffle(rest)
            self.songs = [self.songs[0]] + rest
        else:
            random.shuffle(self.songs)

    async def deco(self):
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
        self.musicPlayers[self.guild] = None
        self = None

    async def play(self):
        # grab the user who sent the command
        user=self.ctx.author
        self.voice_channel=user.voice.channel

        # make first song readable if it's form youtube
        if self.songs_left and type(self.songs[0]) is tuple:
            self.songs[0] = (await getVidFromLink(self.songs[0][0]),self.songs[0][1])
            print("str has been transformed")
        # only play music if user is in a voice channel
        if self.voice_channel:
            #await ctx.send(f"coming to {channel}")
            self.player = await self.voice_channel.connect()
            self.melangix()
            while self.counter < self.songs_left:
                if type(self.songs[self.counter]) is tuple and type(self.songs[self.counter][0]) is str:
                    self.songs[self.counter] = (await getVidFromLink(self.songs[self.counter][0]),self.songs[self.counter][1])
                    
                if type(self.songs[self.counter]) is str:
                    if self.mode == 'review': media = './ressources/Musica/Review/' + self.songs[self.counter]
                    else: media = './ressources/Musica/Main/' + self.songs[self.counter]
                    title = song_to_str(self.songs[self.counter])
                    media = discord.FFmpegPCMAudio(media)
                else:
                    media = self.songs[self.counter][0]
                    title = song_to_str(self.songs[self.counter])
                if self.songs_left>=2 and type(self.songs[self.counter+1]) is tuple:
                    self.songs[self.counter+1] = (await getVidFromLink(self.songs[self.counter+1][0]), self.songs[self.counter+1][1])
                    print("str has been transformed")
                
                print(f'{type(media)} : {media}\n title : {title}\n')
                self.player.play(media)

                #Changing status, only for the main server
                if str(self.guild.id) == '386474283804917760' and type(self.songs[self.counter]) is str: 
                    await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(title))

                while self.player.is_playing():
                    await asyncio.sleep(1)

                if self.is_alone():
                    await self.deco()

                if not self.loop:
                    self.counter += 1
            
            if self.loopqueue:
                self.counter = 1
                await self.play()
            else:
                await self.deco()
        else:
            await self.ctx.send("Vas dans un vocal avant de m'appeler, idiot")



class PlayerButtons(discord.ui.View):
    def __init__(self, song_player, ctx, MusicFunctions):
        self.song_player = song_player
        super().__init__(timeout=None)
        self.ctx = ctx
        self.announce = MusicFunctions.message
    
    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple, custom_id="previous_song")
    async def _previous(self, interaction, button) -> None:
        self.song_player.previous()
        if self.announce:
            await self.announce.edit(embed=make_embed(self.song_player.songs, self.song_player.counter))
        else:
            await self.ctx.edit(embed=make_embed(self.song_player.songs, self.song_player.counter))
            await interaction.response.defer()

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple, custom_id="next_song")
    async def _skip(self, interaction, button) -> None:
        self.song_player.skip()
        if self.announce:
            await self.announce.edit(embed=make_embed(self.song_player.songs, self.song_player.counter))
        else:
            await self.ctx.edit(embed=make_embed(self.song_player.songs, self.song_player.counter))
            await interaction.response.defer()





###
#   Cog Moment
###



class MusicFunctions(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.musicPlayers = dict()

    @commands.command(aliases=["p","pl","ambiance"],
    brief='Makes the bot play audio', display_name="play")
    async def play(self, ctx, *, query=None):
        if query:
            match = matching_songs(query)
            if match == []:
                songs = list()
                with youtube_dl.YoutubeDL(ydl_opts) as yold:
                    result = yold.extract_info(query, download=False)
                    with open('sample.json','w') as f:
                            json.dump(result, f)
                    try:
                        songs = [(url_from_id(result['entries'][i]['id']),result['entries'][i]['title']) for i in range(len(result['entries']))]
                    except:
                        songs = [(query,result['title'])]
            else:       
                songs = match
        else: songs = musicas
        print(songs)
        if self.musicPlayers.get(ctx.guild,False):
            self.musicPlayers[ctx.guild].add_songs(songs)
        else: 
            self.musicPlayers[ctx.guild] = song_player(self.musicPlayers, ctx, ctx.guild, songs, self.client, 'casu')
            await self.musicPlayers[ctx.guild].play()

    @commands.hybrid_command(aliases=["q","print"], 
    brief='Shows the next songs to be played', display_name="queue")
    async def queue(self, ctx, *, bullshit=None):
        if self.musicPlayers.get(ctx.guild,False):
            self.message = await ctx.send(embed=make_embed(self.musicPlayers[ctx.guild].songs, self.musicPlayers[ctx.guild].counter), view=PlayerButtons(self.musicPlayers[ctx.guild], ctx, self))

    @commands.command(aliases=['search'], brief='Searches for a song in the databse', display_name="search")
    async def query(self, ctx, *, query):
        match = matching_songs(query)
        if (len(match)>20 or match==[]):
            await ctx.send(f'Please provide a better query, found {len(match)} songs')
        else:
            daMess = str()
            for song in match:
                daMess += song_to_str(song) + '\n'
            embed = discord.Embed(title='Matching songs :',description=daMess,color=0xffd1f3)
            await ctx.send(embed=embed)

    @commands.command(aliases=['calc'],brief='Does the maths for the length of the playlist', display_name="calc")
    async def calculus(self, ctx, tab=musicas):
        #if self.musicPlayers.get(ctx.guild,False):
        #    tab = self.musicPlayers[ctx.guild].songs
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
    brief='Skips the current song', display_name="skip")
    async def skip(self, ctx): 
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].skip()
            else: raise MusicalError("`skip`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['d','dco','disconnect'],
    brief='Disconnects the bot from voice channel', display_name="deco")
    async def deco(self, ctx): 
        try:
            if self.musicPlayers.get(ctx.guild,False):
                await self.musicPlayers[ctx.guild].deco()
            else: raise MusicalError("`deco`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['l','lop', 'boucle'],
    brief='Puts the current song on loop', display_name="loop")
    async def loop(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].goloop()
            else: raise MusicalError("`loop`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['lq'],
    brief='Puts the current playlist on loop', display_name="loopqueue")
    async def loopqueue(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].goloopqueue()
            else: raise MusicalError("`loopqueue`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['random', 'melange'],
    brief='Shuffles the list of songs to come', display_name="shuffle")
    async def shuffle(self, ctx):
        try:
            if self.musicPlayers.get(ctx.guild,False):
                self.musicPlayers[ctx.guild].melangix()
            else: raise MusicalError("`shuffle`")
        except MusicalError as e:
            await ctx.send(e.message)

    @commands.command(aliases=['pt','ptop'],
    brief='Adds a song as first position in the wait list', display_name="playtop")
    async def playtop(self, ctx, *, query=None):
        if self.musicPlayers.get(ctx.guild, False):
            await self._play(ctx=ctx, query=query)
            await self.musicPlayers[ctx.guild].playtop()
        else:
            await self._play(ctx=ctx, query=query)

    @commands.command(aliases=['ps','pskip'], 
    brief='Skips the current song to play the requested one', display_name="playskip")
    async def playskip(self, ctx, *, query=None):
        if self.musicPlayers.get(ctx.guild, False):
            await self._playtop(ctx=ctx, query=query)
            await self._skip(ctx)
        else:
            await self._play(ctx=ctx, query=query)

    @commands.command(aliases=['tocome'],
    brief='Shows the music waiting to join the playlist', display_name="playskip")
    async def upcoming(self, ctx):
        t='```'
        tab = os.listdir('./ressources/Musica/Update')
        for song in tab:
            if len(t+song)>+1990:
                await ctx.send(t+'```')
                t=f'```'
            t+=song_to_str(song) + '\n'
        await ctx.send(t+'```')