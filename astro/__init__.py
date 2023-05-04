from .astro import Astro

async def setup(bot):
    cog = Astro(bot)
    await bot.add_cog(cog)
