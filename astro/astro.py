import discord
import re
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
from redbot.core import commands,app_commands

class Astro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def get_burc_yorum(self, burc):
        url = f"https://astrotalk.com/horoscope/todays-horoscope/{burc}"
        page = requests.get(url).text   
        soup = BeautifulSoup(page, "html.parser")
        burc_yorumu = soup.find("div", class_=f"parah_aries_horocope")
        return burc_yorumu

    async def get_burc_yorum2(self, burc):  
        url = f"https://astrotalk.com/todays-love-horoscope/{burc}"
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        burc_yorumu2 = soup.find("div", class_=f"parah_aries_horocope")
        return burc_yorumu2

    @app_commands.command()
    @app_commands.describe(burc="burcunuzu seçiniz")
    @app_commands.choices(burc=[
     app_commands.Choice(name="Akrep", value="scorpio"),
     app_commands.Choice(name="İkizler", value="gemini"),
         ])
    async def astro(self, interaction: discord.Interaction, burc: burc):
        burc = burc.lower()
        translator = Translator()
        soup = str(await self.get_burc_yorum(burc))
        output = str(await self.get_burc_yorum2(burc))
        emotions = str(translator.translate(soup, dest="tr"))
        output = str(translator.translate(output, dest="tr"))
        # Use regular expressions to extract individual horoscope sections
        personal = re.search(r'Kişisel: (.+?)</p>', emotions).group(1)                        
        travel = re.search(r'Seyahat: (.+?)</p>', emotions).group(1)
        money = re.search(r'Para: (.+?)</p>', emotions).group(1)
        career = re.search(r'Kariyer: (.+?)</p>', emotions).group(1)
        health = re.search(r'Sağlık: (.+?)</p>', emotions).group(1)
        feelings = re.search(r'Duygular: (.+?)</p>', emotions).group(1)
        start_index = output.find("<p>") + len("<p>")
        end_index = output.find("</p>", start_index)
        love = output[start_index:end_index]
        burc_url = f"https://cdn.shopify.com/s/files/1/1325/0879/articles/headers-zodiac-sign-astrology-personality-positives-negatives-cheat-sheet-{burc}_1500x.png"
        embed = discord.Embed(title=f"{burc.upper()} Burcu Günlük Yorumu", color=0xffd700)
        embed.set_thumbnail(url=ctx.author.avatar)
        embed.add_field(name="Kişisel", value=personal, inline=False)
        embed.add_field(name="Seyahat", value=travel, inline=False)
        embed.add_field(name="Para", value=money, inline=False)
        embed.add_field(name="Kariyer", value=career, inline=False)
        embed.add_field(name="Sağlık", value=health, inline=False)
        embed.add_field(name="Duygular", value=feelings, inline=False)
        embed.add_field(name="Aşk", value=love, inline=False)
        embed.set_image(url=burc_url)
        await ctx.send(embed=embed)
