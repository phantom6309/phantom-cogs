# -*- coding: utf-8 -*-
import discord
from redbot.core import checks, commands, bot
from recipe_scrapers import scrape_me



class Tarif(commands.Cog):
    """başkalarının renklerine bakın"""
    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        
        


    @commands.command()
    async def tarif(self, ctx, yemek:str):
        scraper = scrape_me('https://yemek.com/tarif/{yemek}/')
  
        yapılış = scraper.instructions()  # or alternatively for results as a Python list: scraper.instructions_list()

        await ctx.send(f'{yapılış}')


  
    
