
import discord
from discord.ext import commands

class Pinboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_emoji = None
        self.copy_channel_id = 123456789 # Replace with the ID of the channel you want to copy messages to

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if self.reaction_emoji and payload.emoji == self.reaction_emoji:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if message.author != self.bot.user: # Ignore messages sent by the bot itself
                copy_channel = self.bot.get_channel(self.copy_channel_id)
                await copy_channel.send(f'**{message.author}**: {message.content}')

    @commands.group()
    async def pinboard(self, ctx: commands.Context) -> None:
        """Receive a tarot reading"""
        pass

    @pinboard.command(name="kanal")
    async def _kanal(self, ctx, channel: discord.TextChannel):
        self.copy_channel_id = channel.id
        await ctx.send(f'Copy channel set to {channel.mention}')

    @pinboard.command(name="emoji")
    async def emoji(self, ctx, emoji: str):
        self.reaction_emoji = emoji
        await ctx.send(f'Reaction emoji set to {emoji}')

def setup(bot):
    bot.add_cog(CopyMessages(bot))
