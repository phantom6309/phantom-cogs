# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from bs4 import BeautifulSoup
import requests

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
        await ctx.send(soup)
