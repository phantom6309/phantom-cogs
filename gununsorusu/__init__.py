# -*- coding: utf-8 -*-
from .gununsorusu import Gununsorusu

async def setup(bot):
    cog = Gununsorusu(bot)
    await bot.add_cog(cog)

