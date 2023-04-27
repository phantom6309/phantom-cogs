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
        soup = BeautifulSoup(page.content, "html.parser")
        burc_yorumu = soup.find("div", class_="parah_{burc}_horocope")
        return burc_yorumu

    @commands.command()
    async def astro(self, ctx, burc:str):
        member = ctx.author
        burc = burc.lower()
        soup = await self.get_burc_yorum(burc)
        burc_url = f"https://i.elle.com.tr/elle-test-images/elle_{burc}.jpg"
        embed = discord.Embed(title=f"{member.display_name}'nin günlük falı", color=0x00ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f"{burc.capitalize()}", value=burc_yorumu)
        embed.set_image(url=burc_url)
        await ctx.send(embed=embed)
        await ctx.send(soup)
