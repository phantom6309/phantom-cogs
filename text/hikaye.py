# Post animal pics by Eslyium#1949 & Yukirin#0048

# Discord
import discord
import requests
# Red
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, humanize_list
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
import random
import json
# Libs
import aiohttp

BaseCog = getattr(commands, "Cog", object)
class Hikaye(BaseCog):
    """Animal commands."""

    def __init__(self, bot):
        self.bot = bot
  

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def ekle(self,ctx, text):
     with open('data.json', 'r') as f:
      data = json.load(f)
     data['text'].append(text)
     await ctx.send(f"Text added: {text}")

    @commands.command()
    async def rastgele(self,ctx):
     text = random.choice(data)
     await ctx.send(f"Random text: {text}")