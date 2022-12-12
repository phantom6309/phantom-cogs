# -*- coding: utf-8 -*-
import asyncio
import logging
import re
from collections import namedtuple
from typing import Optional, Union

import discord
from redbot.core import checks, Config, commands, bot

log = logging.getLogger("red.cbd-cogs.bio")

__all__ = ["UNIQUE_ID", "Bio"]

UNIQUE_ID = 0x62696F68617A61726400


class Rolrenk(commands.Cog):
    """başkalarının renklerine bakın"""
    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=UNIQUE_ID, force_registration=True)


    @commands.group(autohelp=False)
    @commands.guild_only()
    async def rolecolor(self, ctx, role: discord.Role):
        color = role.color
        await ctx.send(f"The color for the {role.name} role is {color}")

