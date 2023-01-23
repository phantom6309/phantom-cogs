from .çeviri import Çeviri

def setup(bot):
    bot.add_cog(Çeviri(bot))
    bot = Çeviri(bot)
    
    
