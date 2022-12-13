# -*- coding: utf-8 -*-
import asyncio
import logging
import re
from collections import namedtuple
from typing import Optional, Union
from mealdb import search

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

    
