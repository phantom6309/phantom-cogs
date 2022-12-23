# -*- coding: utf-8 -*-
import discord
import json

# Add the following import statement
from redbot.core import data_manager

from redbot.core import commands
from redbot.core import checks, Config, commands, bot
import random


class Gununsorusu(commands.Cog):
    """günün sorusu"""
    def __init__(self, bot):
        self.bot = bot
        self.items = []

        # Load the list of items from the JSON file
        self.items = data_manager.load_json('gununsorusu')

    @commands.command()
    async def soruekle(self, ctx, *, item: str):
          """Listeye soru ekler"""
        self.items.append(item)
        await ctx.send(f'Added "{item}" to the list')

        # Save the list of items to the JSON file
        data_manager.save_json('gununsorusu', self.items)

    @commands.command()
    async def gununsorusu(self, ctx):
      """Günün sorusunu atar"""
        if len(self.items) == 0:
            await ctx.send('No items in the list')
        else:
            item = random.choice(self.items)
            self.items.remove(item)
            await ctx.send(f'Random item: "{item}"')

    @commands.command()
    async def soruliste(self, ctx):
       """Listedeki soruları gösterir"""
        if len(self.items) == 0:
            await ctx.send('No items in the list')
        else:
            items_str = '\n'.join(self.items)
            await ctx.send(f'Items:\n{items_str}')

    # Add the following command
    @commands.command()
    async def sil(self, ctx, *, item):
      """Listeden soru kaldırır"""
        try:
            self.items.remove(item)
            await ctx.send(f'Removed "{item}" from the list')
            data_manager.save_json('gununsorusu', self.items)
        except ValueError:
            await ctx.send(f'Item "{item}" not found in the list')

    # Add the following command
    @commands.command()
    async def temizle(self, ctx):
    "Listeden tüm soruları kaldırır"""
        self.items.clear()
        await ctx.send('Cleared the list')
        data_manager.save_json('gununsorusu', self.items)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    __del__ = cog_unload
