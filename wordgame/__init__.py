# -*- coding: utf-8 -*-
from .wordgame import Wordgame
import json
async def setup(bot):
    bot.add_cog(Wordgame(bot))
    with open('wordlist.json', 'r') as f:
      word_list = json.load(f)

