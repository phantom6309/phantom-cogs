# -*- coding: utf-8 -*-
from .deemix import Deemix

async def setup(bot):
    bot.add_cog(Deemix(bot))
