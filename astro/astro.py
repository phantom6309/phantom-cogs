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
        
        personal_match = re.search(r"Kişisel: (.+?)\n\n", emotions)
        personal = personal_match.group(1) if personal_match else None
        
        travel_match = re.search(r"Seyahat: (.+?)\n\n", emotions)
        travel = travel_match.group(1) if travel_match else None
        
        money_match = re.search(r"Para: (.+?)\n\n", emotions)
        money = money_match.group(1) if money_match else None
        
        career_match = re.search(r"Kariyer: (.+?)\n\n", emotions)
        career = career_match.group(1) if career_match else None
        
        health_match = re.search(r"Sağlık: (.+?)\n\n", emotions)
        health = health_match.group(1) if health_match else None
        
        feelings_match = re.search(r"Duygular: (.+?)\n\n", emotions)
        feelings = feelings_match.group(1) if feelings_match else None
        
        embed = discord.Embed(title=f"Today's horoscope for {burc.capitalize()}",
                              description=f"**Kişisel**: {personal}\n\n**Seyahat**: {travel}\n\n**Para**: {money}\n\n**Kariyer**: {career}\n\n**Sağlık**: {health}\n\n**Duygular**: {feelings}")
        
        await ctx.send(embed=embed)
