import asyncio
import pathlib
import yaml
from collections import Counter
from typing import Any, Dict, List, Literal, Union
import math
import discord
import random
from redbot.core.utils import AsyncIter
from redbot.core import Config, commands, checks
from redbot.core.bot import Red
from redbot.core.data_manager import cog_data_path
from redbot.core.i18n import Translator, cog_i18n
from .log import LOG
_ = Translator("WordGame", __file__)


class Wordgame:
    """Play a word game with friends!"""

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, identifier=0xB3C0E454, force_registration=True)

        self.config.register_member(points=0, games=0)

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        if requester != "discord_deleted_user":
            return

        all_members = await self.config.all_members()

        async for guild_id, guild_data in AsyncIter(all_members.items(), steps=100):
            if user_id in guild_data:
                await self.config.member_from_ids(guild_id, user_id).clear()
def get_word_list() -> List[str]:
    filepath = cog_data_path(raw_name="WordGame") / "wordlist.yaml"
    if not filepath.is_file():
        return []

    with filepath.open("r", encoding="utf-8") as fp:
        try:
            data = yaml.safe_load(fp)
        except yaml.YAMLError as exc:
            LOG.exception("Error while parsing word list:", exc_info=exc)
            return []

    return data
@commands.command()
@commands.guild_only()
async def wordgame(self, ctx: commands.Context):
    """Start a game of word game."""
    word_list = get_word_list()
    if not word_list:
        await ctx.send(_("No word list found!"))
        return

    previous_word = None
    current_word = None
    while True:
        if not current_word:
            current_word = random.choice(word_list)
            await ctx.send(f"The first word is: {current_word}")

        def check(m):
            return (
                m.author == ctx.author
                and m.channel == ctx.channel
                and m.content.lower() in word_list
                and m.content.lower()[0] == current_word[-1]
            )

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send(_("Time's up! The game has ended."))
            return

        previous_word = current_word
        current_word = msg.content.lower()
        await ctx.send(f"The next word is: {current_word}")
        await self.config.member(ctx.author).points.set(
            self.config.member(ctx.author).points() + len(current_word)
        )
@commands.command()
@commands.guild_only()
async def leaderboard(self, ctx: commands.Context):
    """Show the leaderboard for the word game."""
    leaderboard_data = await self.config.all_members()
    sorted_leaderboard = sorted(
        leaderboard_data.items(), key=lambda x: x[1]["points"], reverse=True
    )
    leaderboard_str = "\n".join(
        [
            f"{i+1}. {self.bot.get_user(int(user_id)).name}: {data['points']} points"
            for i, (user_id, data) in enumerate(sorted_leaderboard)
        ]
    )
    await ctx.send(f"```{leaderboard_str}```")
