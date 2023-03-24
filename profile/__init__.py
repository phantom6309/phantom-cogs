# -*- coding: utf-8 -*-
from .profile import Profile

async def setup(bot):
    cog = Profile(bot)
    await bot.add_cog(cog)
