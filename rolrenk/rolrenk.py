# -*- coding: utf-8 -*-
import asyncio
import logging
import re
from instagram_private_api import Client, ClientCompatPatch
from collections import namedtuple
from typing import Optional, Union
from mealdb import search

import discord
from redbot.core import checks, Config, commands, bot



class Rolrenk(commands.Cog):
    """başkalarının renklerine bakın"""
    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=UNIQUE_ID, force_registration=True)


    @commands.group(autohelp=False)
    @commands.guild_only()
    async def rolecolor(self, ctx, role: discord.Role):
        color = role.color
        await ctx.send(f"The color for the {role.name} role is {color}")
    
    
    



    @commands.group(autohelp=False)
    @commands.guild_only()
    async def yemek(self, ctx, *, yemek: str):
      # Search the Mealdb API for information about the food
      meals = search(yemek)
      if meals:
        # Get the first result from the search
        meal = meals[0]

        # Send a message to the channel with information about the food
        await ctx.send(f"{meal.strMeal} is a dish from {meal.strArea}. Here is the recipe: {meal.strInstructions}")
      else:
        # Send a message to the channel if the food could not be found
        await ctx.send('Sorry, I couldn\'t find any information about that food.')

    
    @commands.group(autohelp=False)
    @commands.guild_only()
    async def instagramlogin(ctx):
  # Ask the user for their Instagram username and password
      await ctx.send("Please enter your Instagram username:")
      username = await bot.wait_for("message")

      await ctx.send("Please enter your Instagram password:")
      password = await bot.wait_for("message")
  
   instagram_client = Client(username, password)

    async def instagram(ctx, instagram_url):
  # Use the Instagram API client to download the video from the given URL
     video_data = instagram_client.download_video(instagram_url)
  
  # Create a new Discord file object from the video data
     video_file = discord.File(video_data, filename="video.mp4")

  # Post the video in the channel
     await ctx.send(file=video_file)
  
  # Delete the video from the device
     video_data.delete()


  
    
