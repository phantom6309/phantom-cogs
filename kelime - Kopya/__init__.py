# -*- coding: utf-8 -*-
from .kelime import Kelime

async def setup(bot):
    bot.add_cog(Kelime(bot))
