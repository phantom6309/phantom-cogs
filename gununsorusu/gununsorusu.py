# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from redbot.core import checks, Config, commands, bot
import random


class Gununsorusu(commands.Cog):
    """günün sorusu"""
    def __init__(self, bot):
        self.bot = bot
        self.items = []


    @commands.command()
    async def soruekle(self, ctx, *, item):
        self.items.append(item)
        await ctx.send(f'Added "{item}" to the list')

    @commands.command()
    async def gununsorusu(self, ctx):
        if len(self.items) == 0:
            await ctx.send('No items in the list')
        else:
            item = random.choice(self.items)
            self.items.remove(item)
            await ctx.send(f'Random item: "{item}"')

    @commands.command()
    async def soruliste(self, ctx):
        if len(self.items) == 0:
            await ctx.send('No items in the list')
        else:
            items_str = '\n'.join(self.items)
            await ctx.send(f'Items:\n{items_str}')

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    __del__ = cog_unload
    


  
    
