# -*- coding: utf-8 -*-
import discord
import json

# Add the following import statement
from redbot.core import data_manager

from redbot.core import commands
from redbot.core import checks, Config, commands, bot
from random import choice 


class Gununsorusu(commands.Cog):
    """günün sorusu"""
    def __init__(self, bot):
        self.bot = bot
        self.items = []
        self.filename = 'items.json'
        # Load items from file if it exists
        try:
            with open(self.filename, 'r') as f:
                self.items = json.load(f)
        except FileNotFoundError:
            pass

    @commands.command()
    async def soruekle(self, ctx, *, item):
        """Havuza soru ekleyin"""
        self.items.append(item)
        with open(self.filename, 'w') as f:
            json.dump(self.items, f)
        await ctx.send(f'Saved "{item}" to the list of items!')

    @commands.command()
    async def gününsorusu(self, ctx):
        """Günün sorusunu isteyin""""
        if not self.items:
            await ctx.send('No items have been saved yet!')
        else:
            item = choice(self.items)
            await ctx.send(f'Here is a random item from the list: "{item}"')

    @commands.command()
    async def sorulistesi(self, ctx):
        """Soru havuzunu görüntüleyin"""
        if not self.items:
            await ctx.send('No items have been saved yet!')
        else:
            item_list = '\n'.join(self.items)
            await ctx.send(f'Here is the full list of items:\n{item_list}')

    @commands.command()
    async def çıkart(self, ctx, *, item):
        """Listeden soru çıkartın"""
        try:
            self.items.remove(item)
        except ValueError:
            await ctx.send(f'Item "{item}" not found in the list!')
        else:
            with open(self.filename, 'w') as f:
                json.dump(self.items, f)
            await ctx.send(f'Removed "{item}" from the list of items!')
    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())

    __del__ = cog_unload
