# -*- coding: utf-8 -*-
import discord
from redbot.core import checks, commands, bot
from deemix import deezerdownload
from math import ceil


class Deemix(commands.Cog):
    
    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @commands.command()
    async def download(self, ctx, url):
        try:
            # Download the song using Deemix
            song_path = deezerdownload.download_track(url, quality='FLAC')
            
            # Send the song to Discord
            with open(song_path, 'rb') as f:
                await ctx.send(file=discord.File(f))
                
        except Exception as e:
            await ctx.send(f"Error downloading song: {e}")
