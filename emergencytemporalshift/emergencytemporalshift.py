import random
import discord
from redbot.core import commands, Config

class TemporalShift(commands.Cog):
    """Random teleport to a message from server history."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=9876543210)
        # Store message references per guild
        self.config.register_guild(messages=[])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Log message IDs as they arrive."""
        if message.guild is None or message.author.bot:
            return
        async with self.config.guild(message.guild).messages() as msgs:
            msgs.append((message.channel.id, message.id))
            # optional cap to prevent infinite growth
            if len(msgs) > 500000:
                msgs.pop(0)

    @commands.command(name="emergencytemporalshift")
    async def emergency_temporal_shift(self, ctx):
        """Teleport to a random message from saved history."""
        msgs = await self.config.guild(ctx.guild).messages()
        if not msgs:
            await ctx.send("No messages stored yet, try again later or run backfill!")
            return

        channel_id, message_id = random.choice(msgs)
        channel = ctx.guild.get_channel(channel_id)
        if channel is None:
            await ctx.send("That channel no longer exists.")
            return

        try:
            msg = await channel.fetch_message(message_id)
            await ctx.send(f"🔮 Temporal Shift activated!\n{msg.jump_url}")
        except discord.NotFound:
            await ctx.send("That message was deleted.")
        except discord.Forbidden:
            await ctx.send("I no longer have access to that channel.")

    @commands.command(name="temporalshift_backfill")
    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    async def temporalshift_backfill(self, ctx):
        """Scan all channels and store their message IDs (can be slow)."""
        await ctx.send("📦 Starting backfill... This may take a while.")

        stored = 0
        async with self.config.guild(ctx.guild).messages() as msgs:
            for channel in ctx.guild.text_channels:
                try:
                    async for msg in channel.history(limit=None, oldest_first=True):
                        msgs.append((msg.channel.id, msg.id))
                        stored += 1
                        # prevent runaway growth, but keep it big
                        if len(msgs) > 500000:
                            msgs.pop(0)
                except discord.Forbidden:
                    continue
                except discord.HTTPException:
                    continue

        await ctx.send(f"✅ Backfill complete! Stored ~{stored} messages.")

def setup(bot):
    bot.add_cog(TemporalShift(bot))
