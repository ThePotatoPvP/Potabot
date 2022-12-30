# -*- coding: utf-8 -*-
import discord 
from discord.ext import commands 

class MusicalError(Exception):
    def __init__(self, command:str):
        self.message = f'Error occured : command {command} failed to execute, make sure the bot is playing music.'

class NotDownloadable(Exception):
    def __init__(self, media=None, media_type=None):
        if media_type == "file": self.message = f'Failed to download `{media}` please try again, or contact an administrator.'
        elif media_type == "youtube": self.message = f'Failed to download `{media}` make sure it is a valid link,if it the content may be restricted.'
        else : self.message = f'Failed to download `{media}`'