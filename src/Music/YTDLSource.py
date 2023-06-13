# -*- coding: utf-8 -*-
import yt_dlp as youtube_dl
import discord
import asyncio

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

ffmpeg_opts = {
    'options': '-vn',
    'reconnect': '1',
    'reconnect_streamed' : '1',
    'reconnect_delay_max': '5',
    'http_persistent': '0'
}

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