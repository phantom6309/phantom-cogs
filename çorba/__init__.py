from .corba import Corba

async def setup(bot):

    cog = Corba(bot)

    await bot.add_cog(cog)
