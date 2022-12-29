# -*- coding: utf-8 -*-
from .wordgame import Wordgame
import json
from redbot.core import data_manager

async def setup(bot):
    bot.add_cog(Wordgame(bot))
    

