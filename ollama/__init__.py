from .turkishai import TurkishAI

async def setup(bot):
    await bot.add_cog(TurkishAI(bot))
