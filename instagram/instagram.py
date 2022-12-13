from urllib.request import urlopen
from redbot.core import checks, Config
from redbot.core.i18n import Translator, cog_i18n
import discord
from redbot import version_info, VersionInfo
from discord.ext import commands
from redbot.core import commands
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, start_adding_reactions
from redbot.core.utils import mod
import asyncio
import datetime
import aiohttp
import requests
import os


class Instagram(commands.Cog):
    """İnstagram video download"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def insta(ctx, url: str):
    # Download the video from the given URL
    # You will need to use a library like requests to do this
    # The video will be saved to a local file

    # Get the channel where the video should be posted
     channel = ctx.message.channel

    # Post the video to the channel
    # You will need to use the `discord.File` class to attach the video file to the message
     await channel.send('Here is the Instagram video you requested:', file=discord.File(video_file))

    # Delete the video file from the local device
     os.remove(video_file)