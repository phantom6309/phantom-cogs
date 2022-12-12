# -*- coding: utf-8 -*-
from .rolrenk import Rolrenk

async def setup(bot):
    bot.add_cog(Rolrenk(bot))
