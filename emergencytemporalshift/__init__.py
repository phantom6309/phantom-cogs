from .emergencytemporalshift import TemporalShift

async def setup(bot):
    cog =TemporalShift(bot)
    await bot.add_cog(cog)
