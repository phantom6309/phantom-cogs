import discord
import re
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
from redbot.core import commands

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
        burc = burc.lower()
        translator = Translator()
        soup = str(await self.get_burc_yorum(burc))
        emotions = str(translator.translate(soup, dest="tr").text)

        # Use regular expressions to extract individual horoscope sections
        personal = re.search(r'Kişisel: (.+?)</p>', emotions)                        
        travel = re.search(r"Seyahat: (.+?)\n\n", emotions).group(1)
        money = re.search(r"Para: (.+?)\n\n", emotions).group(1)
        career = re.search(r"Kariyer: (.+?)\n\n", emotions).group(1)
        health = re.search(r"Sağlık: (.+?)\n\n", emotions).group(1)
        feelings = re.search(r"Duygular: (.+?)$", emotions).group(1)

        # Create an embed with the horoscope sections as titles and descriptions
        embed = discord.Embed(title=f"{burc.upper()} Burcu Günlük Yorumu", color=0xffd700)
        embed.add_field(name="Kişisel", value=personal, inline=False)
        embed.add_field(name="Seyahat", value=travel, inline=False)
        embed.add_field(name="Para", value=money, inline=False)
        embed.add_field(name="Kariyer", value=career, inline=False)
        embed.add_field(name="Sağlık", value=health, inline=False)
        embed.add_field(name="Duygular", value=feelings, inline=False)

        await ctx.send(embed=embed)
