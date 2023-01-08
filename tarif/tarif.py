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
        test = scraper.yields()
        malzemeler = scraper.ingredients()
        photo = scraper.image()
        test2 = scraper.host()
        besindeğer = scraper.nutrients()
        yapılış = scraper.instructions()
        await ctx.send(f'yemek ismi {yemekismi}')
        await ctx.send(f'yapılış {yapılış}')
        await ctx.send(f'hazırlama süresi {hazırlamasüresi}')
        await ctx.send(f'test {test}')
        await ctx.send(f'malzemeler {malzemeler}')
        await ctx.send(f'test 2 {test2}')
        await ctx.send(f'besin değeri {besindeğer}')
        await ctx.send(f'yapılış {yapılış}')


