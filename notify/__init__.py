from .notify import Notify

async def setup(bot):

    cog = Notify(bot)

    await bot.add_cog(cog)
