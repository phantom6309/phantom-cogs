from .insta import Insta

async def setup(bot):

    cog = Insta(bot)

    await bot.add_cog(cog)
