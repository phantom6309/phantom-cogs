from .sinema import Sinema

async def setup(bot):

    cog = Sinema(bot)

    await bot.add_cog(cog)
