import random
import discord
from redbot.core import commands

class TemporalShift(commands.Cog):
    """Jump to a random message in your server's full history (slow)."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="emergencytemporalshift")
    async def emergency_temporal_shift(self, ctx):
        """Send a link to a random message from the full history (can be slow!)."""
        messages = []
        for channel in ctx.guild.text_channels:
            try:
                async for msg in channel.history(limit=None):  # no limit → fetch all
                    messages.append(msg)
            except discord.Forbidden:
                continue
            except discord.HTTPException:
                await ctx.send(f"⚠️ Could not fully fetch history for #{channel}.")
                continue

        if not messages:
            await ctx.send("I couldn’t find any messages I can access.")
            return

        chosen = random.choice(messages)
        await ctx.send(f"🔮 Full Temporal Shift activated!\n{chosen.jump_url}")

def setup(bot):
    bot.add_cog(TemporalShift(bot))
