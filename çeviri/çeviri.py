# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
import googletrans

class Çeviri(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = googletrans.Translator()
    
    

    @commands.command()
    async def çevirikanal(self, ctx, channel: discord.TextChannel):
        self.channel_id = channel.id
        await ctx.send(f"Translate channel set to {channel.mention}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.channel_id:
            src = self.translator.detect(message.content).lang
            dest = 'tr' if src == 'en' else 'en'
            translation = self.translator.translate(message.content, dest=dest)
            await message.channel.send(translation.text)


