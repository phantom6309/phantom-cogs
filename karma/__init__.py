from .karma import Karma

async def setup(bot):

    cog = Karma(bot)

    await bot.add_cog(cog)
