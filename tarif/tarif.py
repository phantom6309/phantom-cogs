# -*- coding: utf-8 -*-
import discord
from redbot.core import checks, commands, bot
from recipe_scrapers import scrape_me
from math import ceil


class Tarif(commands.Cog):
    """başkalarının renklerine bakın"""

    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @commands.command()
    async def tarif(self, ctx, yemek):
        lower_map = {
            ord(u'ö'): u'o',
            ord(u'ı'): u'i',
            ord(u'ş'): u's',
            ord(u' '): u'-',
            ord(u'ü'): u'u',
        }
        yemek = yemek.translate(lower_map)
        url = f"https://yemek.com/tarif/{yemek}"
        scraper = scrape_me(url)
        yemekismi = scraper.title()
        hazırlamasüresi = scraper.total_time()
        kaçkişilik = scraper.yields()
        malzemeler = scraper.ingredients()
        photo = scraper.image()
        besindeğer = scraper.nutrients()
        yapılış = scraper.instructions()
        embed = discord.Embed(title=yemekismi)
        embed.add_field(name="Hazırlama süresi", value=hazırlamasüresi)
        embed.add_field(name="Kaç Kişilik", value=kaçkişilik)
        embed.add_field(name="Malzemeler", value=malzemeler)
        embed.add_field(name="Besin Değeri", value=besindeğer)
        embed.set_image(url=photo)
        await ctx.send(embed=embed)
        for i in range(ceil(len(yapılış) / 4096)):
            embed2 = discord.Embed(title='Hazırlanışı')
            embed2.description = (yapılış[(4096*i):(4096*(i+1))])
            await ctx.send(embed=embed2)
