# -*- coding: utf-8 -*-
import discord
from redbot.core import commands, bot
from tunga.preprocessing import normalization



class Tunga(commands.Cog):
    """başkalarının renklerine bakın"""

    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @commands.command()
    async def tunga(self, ctx, *, cümle):
         düzgün = normalization.correct_typo(cümle)
         embed = discord.Embed(title=Tunga düzeltme)
         embed.add_field(name="Düzeltilmiş", value=düzgün)
         await ctx.send(embed=embed)
