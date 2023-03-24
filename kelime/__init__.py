# -*- coding: utf-8 -*-
from .kelime import Kelime

async def setup(bot):
    cog = Kelime(bot)
    await bot.add_cog(cog)
