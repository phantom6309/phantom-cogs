# -*- coding: utf-8 -*-
import re
from collections import namedtuple
from typing import Optional, Union



import discord
from redbot.core import checks, commands, bot




class Rolrenk(commands.Cog):
    """başkalarının renklerine bakın"""
    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        
        


    @commands.command()
    async def rolrenk(self, ctx, role: discord.Role):
        color = role.color
        await ctx.send(f"The color for the {role.name} role is {color}")


    


  
    
