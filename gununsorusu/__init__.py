# -*- coding: utf-8 -*-
from .gununsorusu import Gununsorusu

async def setup(bot):
    bot.add_cog(Gununsorusu(bot))
