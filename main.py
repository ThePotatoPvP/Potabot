# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import os
import asyncio

#Potato#8999
#id = 694246129906483311
#public key = 70c7073417dc12f36435054a09b02e269b85acb1f89ded5724a8f9a20122f0e1

current_folder = os.path.dirname(os.path.abspath(__file__)) + "/"

import pytz
tz = pytz.timezone('Europe/Paris')


from src.Bots.Potabot import Potabot
from src.Bots.EventBot import EventBot

###
#   Booting bots
###

import concurrent.futures

def run_bot(token: str, bot: discord.Client):
    bot.run(token)

if __name__ == '__main__':
    token = open('.token', 'r').read()

    ptb = Potabot()
    evt = EventBot()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(run_bot, token, ptb)
        executor.submit(run_bot, token, evt)