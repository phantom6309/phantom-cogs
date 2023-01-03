from .otogif import Otogif


def setup(bot):
    n = Otogif()
    bot.add_cog(n)
