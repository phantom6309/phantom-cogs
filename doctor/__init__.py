from .doctor import Doctor


def setup(bot):
    n = Doctor()
    bot.add_cog(n)
