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
        burc_url = f"https://i.elle.com.tr/elle-test-images/elle_{burc}.jpg"
        emotions = re.search(r'Emotions: (.+?)</p>', soup).group(1)
        emotions = str(translator.translate(emotions, dest="tr"))
        career = re.search(r'Career: (.+?)</p>', soup).group(1)
        health = re.search(r'Health: (.+?)</p>', soup).group(1)
        money = re.search(r'Money: (.+?)</p>', soup).group(1)
        travel = re.search(r'Travel: (.+?)</p>', soup).group(1)
        personal = re.search(r'Personal: (.+?)</p>', soup).group(1)
        await ctx.send(emotions)
        await ctx.send(personal)
