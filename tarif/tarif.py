# -*- coding: utf-8 -*-
import discord
from redbot.core import checks, commands, bot
from recipe_scrapers import scrape_me


class Tarif(commands.Cog):
    """başkalarının renklerine bakın"""

    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @commands.command()
    async def tarif(self, ctx, yemek):
        url = f"https://yemek.com/tarif/{yemek}"
        scraper = scrape_me(url)
        yemekismi = scraper.title()
        hazırlamasüresi = scraper.total_time()
        kaçkişilik = scraper.yields()
        malzemeler = scraper.ingredients()
        photo = scraper.image()
        besindeğer = scraper.nutrients()
        yapılış = scraper.instructions()
        embed = discord.Embed(title={yemekismi})
        embed.add_field(name="hazırlama süresi", value=hazırlamasüresi)
        embed.add_field(name="kaç kişilik", value=kaçkişilik)
        embed.add_field(name="malzemeler", value=malzemeler)
        embed.add_field(name="besindeğer", value=besindeğer)
        embed.add_field(name="yapılış", value=yapılış)
        embed.set_image(photo)
        await ctx.send(embed=embed)
