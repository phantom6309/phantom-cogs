from .roleplay import Roleplay


async def setup(bot):
    cog = Roleplay(bot)
    await bot.add_cog(cog)
