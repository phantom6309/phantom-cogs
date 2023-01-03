from .otogif import Otogif


def setup(bot):
    bot.add_cog(Otogif(bot))
