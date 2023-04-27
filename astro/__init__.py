from .astro import Astro

def setup(bot):
    bot.add_cog(Astro(bot))
