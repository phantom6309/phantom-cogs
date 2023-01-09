# -*- coding: utf-8 -*-
from .tunga import Tunga

async def setup(bot):
    bot.add_cog(Tunga(bot))
