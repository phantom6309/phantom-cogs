import discord
from redbot.core import commands, Config

class ReactionNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)  # Change the identifier to a unique value
        default_global = {}
        self.config.register_global(**default_global)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Fetch the message object using the message ID from the payload
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        # Check if the author has opted-in for notifications
        notify_users = await self.config.all()
        if str(message.author.id) in notify_users:
            # Notify the author of the message if it's not a bot
            if not message.author.bot:
                # Get the user who added the reaction
                user = await self.bot.fetch_user(payload.user_id)
                # Get the emoji used in the reaction
                emoji = payload.emoji
                # Send a notification including the emoji information
                await message.author.send(f"{user.name} reacted to your message with the emoji {emoji}: {message.content}")

    @commands.command()
    async def notify(self, ctx):
        notify_users = await self.config.all()
        user_id = str(ctx.author.id)
        if user_id in notify_users:
            await self.config.clear_raw(user_id)
            await ctx.send("You will no longer receive reaction notifications.")
        else:
            await self.config.set_raw(user_id, value={})
            await ctx.send("You will now receive reaction notifications.")

