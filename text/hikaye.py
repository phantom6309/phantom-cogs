# Post animal pics by Eslyium#1949 & Yukirin#0048

# Discord
import discord
import requests
# Red
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, humanize_list
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
import random
# Libs
import aiohttp

BaseCog = getattr(commands, "Cog", object)
class Hikaye(BaseCog):
    """Animal commands."""

    def __init__(self, bot):
        self.bot = bot
  

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def ekle(ctx, *, text):
     texts.append(text)
     await ctx.send(f"Text added: {text}")
 
# Define a command to get a random text from the list
    @commands.command()
    async def rastgele(ctx):
     text = random.choice(texts)
     await ctx.send(f"Random text: {text}")