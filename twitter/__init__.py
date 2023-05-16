from .twitter import Twitter

async def setup(bot):

    cog = Twitter(bot)

    await bot.add_cog(cog)
