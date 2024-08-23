from .trakt import Trakt

async def setup(bot):

    cog = Trakt(bot)

    await bot.add_cog(cog)
