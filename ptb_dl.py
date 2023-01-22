# -*- coding: utf-8 -*-


#Potato#8999
#id = 694246129906483311
#public key = 70c7073417dc12f36435054a09b02e269b85acb1f89ded5724a8f9a20122f0e1


"""
///////////////////////////////////
/// Le bot du turfu de moi même ///
///////////////////////////////////
"""

perms = "Vous n'avez pas les droits suffisants pour utiliser cette commande"

###########################
# Import de trucs rigolos #
###########################



import discord
from discord.ext import commands
import asyncio
import ffmpeg
import os
import youtube_dl
import datetime
import time
import nest_asyncio
import requests
import re

nest_asyncio.apply()

current_folder = os.path.dirname(os.path.abspath(__file__)) + "/"



################################
# On met le prefixe de la joie #
################################



intents = discord.Intents().default()
intents.members = True

client  = commands.Bot(command_prefix = "P!", help_command=None, intents = intents)



token = open(current_folder + ".token","r").readlines()[0]
  
    

##################################
# Mtn on fait des le downloader  #
##################################

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'noplaylist' : True,
}

@client.event
async def on_ready():
    print("Jui co")

@client.event
async def on_message(message):
    global ydl_opts

    #Check si on reçoit un mp
    if not message.guild and message.author != client.user:
        t = message.attachments

        #Si on a un lien
        if re.match("https:\/\/(www\.)?youtu(\.?)be(\.com)?\/(watch\?v=)?.*", message.content):
            msg = message.content.split()
            for mot in msg:
                if re.match("https:\/\/(www\.)?youtu(\.?)be(\.com)?\/(watch\?v=)?.*", mot):

                    #On dl ce son divin
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        try:
                            await message.channel.send(f"Starting download of `{mot}`")
                            ydl.download([mot])
                        except:
                            await message.channel.send(f"Failed to download `{mot}`")
                    try:
                        filenames = os.listdir()
                        for filename in filenames:
                            if filename.endswith(".mp3"):
                                os.rename(filename, "ressources/Musica/Update/" + filename)
                                await message.channel.send(f"OK j'ai downlod {filename}")
                    except:
                        print("nop")
        if len(t) > 0:
            music_types = ["m4a","mp3"]
            for attachment in t:
                if any(attachment.filename.lower().endswith(typee) for typee in music_types):
                    await message.channel.send(f"Starting download of `{attachment.filename}`")
                    await attachment.save("ressources/Musica/Update/" + attachment.filename)
                    await message.channel.send(f"OK j'ai downlod {attachment.filename}")

##################
#  Le démarreur  #
##################

