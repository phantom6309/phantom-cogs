# -*- coding: utf-8 -*-
from .spotidown import Spotidown

async def setup(bot):
    bot.add_cog(Spotidown(bot))
