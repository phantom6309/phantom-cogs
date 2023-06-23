# -*- coding: utf-8 -*-
import discord
import json

# Add the following import statement
from redbot.core import data_manager

from redbot.core import commands
from redbot.core import checks, Config, commands, bot
from random import choice 


class Gununsorusu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=965854745)
        self.config.register_guild(items=[])
    
    @commands.command()
    async def soruekle(self, ctx, *, item):
        """Havuza soru ekleyin"""
        guild_id = ctx.guild.id
        items = await self.config.guild(ctx.guild).items()
        items.append(item)
        await self.config.guild(ctx.guild).items.set(items)
        await ctx.send(f'Soru eklendi!')
        await ctx.message.delete()
    
    @commands.command()
        @checks.admin_or_permissions(manage_guild=True)
    async def gününsorusu(self, ctx):
        """Günün sorusunu isteyin"""
        guild_id = ctx.guild.id
        items = await self.config.guild(ctx.guild).items()
        if not items:
            await ctx.send('No items have been saved yet!')
        else:
            item = choice(items)
            await ctx.send(f'Günün sorusu: "{item}"')
            items.remove(item)
            await self.config.guild(ctx.guild).items.set(items)
    
    @commands.command()
    async def sorulistesi(self, ctx):
        """Soru havuzunu görüntüleyin"""
        guild_id = ctx.guild.id
        items = await self.config.guild(ctx.guild).items()
        if not items:
            await ctx.send('Havuzda soru yok!')
        else:
            item_list = '\n'.join(items)
            await ctx.send(f'Havuzdaki bütün sorular:\n{item_list}')

    @commands.command()
    async def çıkart(self, ctx, *, item):
         """Listeden soru çıkartın"""
         guild_id = ctx.guild.id
         items = await self.config.guild(ctx.guild).items()
         try:
            items.remove(item)
         except ValueError:
          await ctx.send(f'Item "{item}" sorusu listede bulunamadı!')
         else:
           await self.config.guild(ctx.guild).items.set(items)
           await ctx.send(f'Removed "{item}" sorusu listeden çıkarıldı!')
         
    
    @commands.command()
    async def temizle(self, ctx):
        """Tüm listeyi temizleyin"""
        self.items.clear()
        with open(self.filename, 'w') as f:
            json.dump(self.items, f)
        await ctx.send('soru havuzu temizlendi!')
  
    
    @commands.command()
    async def temizle(self, ctx):
     """Tüm listeyi temizleyin"""
     await self.config.guild(ctx.guild).items.set([])
     await ctx.send('soru havuzu temizlendi!')
     

