# -*- coding: utf-8 -*-
from .wordgame import Profile

async def setup(bot):
    bot.add_cog(Profile(bot))
