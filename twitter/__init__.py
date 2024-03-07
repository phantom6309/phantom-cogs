from .çorba import Çorba

async def setup(bot):

    cog = Çorba(bot)

    await bot.add_cog(cog)
