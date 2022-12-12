# -*- coding: utf-8 -*-
from .rolerenk import Rolrenk

async def setup(bot):
    bot.add_cog(Rolrenk(bot))
