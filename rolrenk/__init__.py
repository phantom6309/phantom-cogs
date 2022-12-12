# -*- coding: utf-8 -*-
from .rolerenk import Rolerenk

async def setup(bot):
    bot.add_cog(Rolerenk(bot))
