# -*- coding: utf-8 -*-
from .pinboard import Pinboard

async def setup(bot):
    cog = Pinboard(bot)
    await bot.add_cog(cog)
