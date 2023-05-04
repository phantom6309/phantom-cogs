# -*- coding: utf-8 -*-
from .spotidown import Spotidown

async def setup(bot):
    cog = Spotidown(bot)
    await bot.add_cog(cog)
