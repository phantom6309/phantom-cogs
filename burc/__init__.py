from .burc import Burc

def setup(bot):
    bot.add_cog(Burc(bot))
    bot = Burc(bot)
