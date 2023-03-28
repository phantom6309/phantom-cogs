# -*- coding: utf-8 -*-
from .pinboard import Pinboard

async def setup(bot):
    bot.add_cog(Pinboard(bot))
