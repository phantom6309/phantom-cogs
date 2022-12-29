# -*- coding: utf-8 -*-
from .wordgame import Wordgame
import json
from redbot.core import data_manager

def setup(bot):
    n = Wordgame(bot)
    data_manager.bundled_data_path(n)
    bot.add_cog(n)
    

