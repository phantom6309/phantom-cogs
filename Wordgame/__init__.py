# -*- coding: utf-8 -*-
from .wordgame import Wordgame

async def setup(bot):
    bot.add_cog(Wordgame(bot))
