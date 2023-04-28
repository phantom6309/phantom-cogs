# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from bs4 import BeautifulSoup
from googletrans import Translator
import requests
import re
class Astro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    async def get_burc_yorum(self, burc):
        url = f"https://astrotalk.com/horoscope/todays-horoscope/{burc}"
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        burc_yorumu = soup.find("div", class_=f"parah_aries_horocope")
        return burc_yorumu

    @commands.command()
    async def astro(self, ctx, burc:str):
        member = ctx.author
        burc = burc.lower()
        translator = Translator()
        soup = str(await self.get_burc_yorum(burc))

        emotions = str(translator.translate(soup, dest="tr"))
        await ctx.send(emotions)
        await ctx.send(personal)
