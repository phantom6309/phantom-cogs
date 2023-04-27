# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from bs4 import BeautifulSoup
import requests
from math import ceil 
class Astro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    async def get_burc_yorum(self, burc):
        url = f"https://astrotalk.com/horoscope/todays-horoscope/{burc}"
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        burc_yorumu = soup.find("div", class_="parah_{burc}_horocope")
        return soup

    @commands.command()
    async def astro(self, ctx, burc:str):
        member = ctx.author
        burc = burc.lower()
        soup = await self.get_burc_yorum(burc)
        burc_url = f"https://i.elle.com.tr/elle-test-images/elle_{burc}.jpg"
        for i in range(ceil(len(soup) / 4096)):
            embed = discord.Embed(title='Hello World')
            embed.description = (my_text[(4096*i):(4096*(i+1))])
            await ctx.send(embed=embed)
