# -*- coding: utf-8 -*-
from .instagram import Instagram

async def setup(bot):
    bot.add_cog(Instagram(bot))
