# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from bs4 import BeautifulSoup
import requests
class Burc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.burclar = {
            "koc": "1", "boga": "2", "ikizler": "3",
            "yengec": "4", "aslan": "5", "basak": "6",
            "terazi": "7", "akrep": "8", "yay": "9",
            "oglak": "10", "kova": "11", "balik": "12"
        }

    async def get_burc_yorum(self, burc):
        url = f"https://www.elle.com.tr/astroloji/{burc}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        burc_yorumu = soup.find("div", class_="body-el-text standard-body-el-text").get_text().strip()
        return burc_yorumu

    @commands.command(name="burç")
    async def burç(self, ctx, burc:str):
        member = ctx.author
        burc = burc.lower()
        if burc not in self.burclar:
            await ctx.send("türkçe karakter kullanmayınız!")
            return
        burc_yorumu = await self.get_burc_yorum(burc)
        burc_url = f"https://i.elle.com.tr/elle-test-images/elle_{burc}.jpg"
        embed = discord.Embed(title=f"{member.display_name}'nin günlük falı", color=0x00ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f"{burc.capitalize()}", value=burc_yorumu)
        embed.set_image(url=burc_url)
        await ctx.send(embed=embed)
