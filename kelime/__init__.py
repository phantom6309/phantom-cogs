# -*- coding: utf-8 -*-
from .kelime import Kelime

def setup(bot):
    bot.add_cog(Kelime(bot))
    bot = Kelime(bot)
