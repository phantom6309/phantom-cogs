from .burc import Burc

async def setup(bot):
    cog = Burc(bot)
    await bot.add_cog(cog)
