# -*- coding: utf-8 -*-
from .tarif import Tarif

async def setup(bot):
    bot.add_cog(Tarif(bot))
