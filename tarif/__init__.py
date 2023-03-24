# -*- coding: utf-8 -*-
from .tarif import Tarif

async def setup(bot):
    cog = Tarif(bot)
    await bot.add_cog(cog)
