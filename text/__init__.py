from .hikaye import Hikaye


def setup(bot):
    bot.add_cog(Hikaye(bot))
