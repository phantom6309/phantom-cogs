import asyncio
import logging
import random
from typing import List, Literal, Optional

import discord
from redbot.core import commands
from redbot.core.bot import Red

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

log = logging.getLogger("red.sravan.gtn")


class GuessTheNumber(commands.Cog):
    """
    A simple gtn game.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot

    __author__ = ["sravan"]
    __version__ = "1.1.2"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthors: {', '.join(self.__author__)}\nCog Version: {self.__version__}"

    @commands.command()
    @commands.guild_only()
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def gtn(self, ctx: commands.Context):
        """
        Start a gtn event.
        """
        user: discord.Member = ctx.author
        number = random.randint(1, 10)
        await ctx.send(f"A random number between 1 and 1000 has been selected. Guess the number!")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        started = True
        while started:
            guess = await self.bot.wait_for("message", check=check)
            if guess.content.isdigit():
                try:
                    guessed_number = int(guess.content)
                except ValueError:
                    continue
                if guessed_number == number:
                    winem = discord.Embed()
                    winem.set_author(
                        name=f"{guess.author.display_name} has won the gtn event",
                        icon_url=guess.author.avatar.url,
                    )
                    winem.color = await ctx.embed_colour()
                    winem.add_field(name="Number guessed", value=f"> {guess.content}")
                    winem.set_footer(text="Thanks for playing!")
                    winem.set_thumbnail(url=ctx.guild.icon.url)
                    await guess.reply(embed=winem, content=ctx.author.mention)
                    started = False
                elif guessed_number < number:
                    await guess.add_reaction("🔽")  # Down arrow
                elif guessed_number > number:
                    await guess.add_reaction("🔼")  # Up arrow

            if guess.content.lower() == "cancel" and guess.author.id == ctx.author.id:
                await ctx.send(f"{user.mention} has cancelled the gtn event.")
                started = False
                break

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

