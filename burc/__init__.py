from .burc import Burc
from translate import Translator

def setup(bot):
    bot.add_cog(Burc(bot))
