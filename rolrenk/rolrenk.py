# -*- coding: utf-8 -*-
import asyncio
import logging
import re
from collections import namedtuple
from typing import Optional, Union
from mealdb_api_client import Client

client = discord.Client()
mealdb_client = Client()
import discord
from redbot.core import checks, Config, commands, bot

log = logging.getLogger("red.cbd-cogs.bio")

__all__ = ["UNIQUE_ID", "Bio"]

UNIQUE_ID = 0x62696F68617A61726400


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
    
    

@client.event
async def on_message(message):
  # Check if the message starts with the `!food` command
  if message.content.startswith('!food'):
    # Get the food name from the message
    food = message.content.split(' ')[1]

    # Search the Mealdb API for information about the food
    result = await mealdb_client.search(food)
    if result.meals and len(result.meals) > 0:
      # Get the first result from the search
      meal = result.meals[0]

      # Send a message to the channel with information about the food
      await message.channel.send(f"{meal.strMeal} is a dish from {meal.strArea}. Here is the recipe: {meal.strInstructions}")
    else:
      # Send a message to the channel if the food could not be found
      await message.channel.send('Sorry, I couldn\'t find any information about that food.')


    
