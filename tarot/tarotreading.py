import re
import random
from random import choice, sample
from typing import Optional
from dataclasses import dataclass

import discord
from redbot.core import commands

from . import tarot_cards


@dataclass
class TarotCard:
    id: int
    card_meaning: str
    card_name: str
    card_url: str
    card_img: str


TAROT_CARDS = {num: TarotCard(id=num, **data) for num, data in tarot_cards.card_list.items()}
TAROT_RE = re.compile(r"|".join(t.card_name for _id, t in TAROT_CARDS.items()), flags=re.I)


class TarotConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> Optional[TarotCard]:
        if find := TAROT_RE.match(argument):
            card_name = find.group(0)
            for card in TAROT_CARDS.values():
                if card_name.lower() == card.card_name.lower():
                    return card
        else:
            try:
                return TAROT_CARDS[str(argument)]
            except KeyError:
                raise commands.BadArgument("`{argument}` is not an available Tarot card.")
        return None


class TarotReading(commands.Cog):
    """
    Post information about tarot cards and readings
    """

    __author__ = ["TrustyJAID"]
    __version__ = "1.1.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    def get_colour(self) -> int:
        colour = "".join([choice("0123456789ABCDEF") for x in range(6)])
        return int(colour, 16)

    @commands.group()
    async def tarot(self, ctx: commands.Context) -> None:
        """Tarot okuması alın"""
        pass

    @tarot.command(name="hayat")
    async def _hayat(self, ctx: commands.Context, user: Optional[discord.Member] = None) -> None:
        """
        Tüm hayatınız için yorum alın.
        """
        card_meaning = ["Past", "Present", "Future", "Potential", "Reason"]
        if user is None:
            user = ctx.message.author
        userseed = user.id

        random.seed(int(userseed))
        cards = []
        cards = sample((range(1, 78)), 5)

        embed = discord.Embed(
            title="Tarot falı {}".format(user.display_name),
            colour=discord.Colour(value=self.get_colour()),
        )
        embed.set_thumbnail(url=TAROT_CARDS[str(cards[-1])].card_img)
        embed.timestamp = ctx.message.created_at
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        number = 0
        for card in cards:
            embed.add_field(
                name="{0}: {1}".format(card_meaning[number], TAROT_CARDS[str(card)].card_name),
                value=TAROT_CARDS[str(card)].card_meaning,
            )
            number += 1
        await ctx.send(embed=embed)

    @tarot.command(name="fal")
    async def _fal(self, ctx: commands.Context, user: Optional[discord.Member] = None) -> None:
        """
        Hayatınızın şuan ki kısmı için yorum alın.
        """
        card_meaning = ["Geçmiş", "Şimdi", "Gelecek", "Potansiyel", "Sebep"]
        if user is None:
            user = ctx.message.author

        cards = []
        cards = sample((range(1, 78)), 5)

        embed = discord.Embed(
            title="Tarot falı {}".format(user.display_name),
            colour=discord.Colour(value=self.get_colour()),
        )
        embed.set_thumbnail(url=TAROT_CARDS[str(cards[-1])].card_img)
        embed.timestamp = ctx.message.created_at
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        number = 0
        for card in cards:
            embed.add_field(
                name="{0}: {1}".format(card_meaning[number], TAROT_CARDS[str(card)].card_name),
                value=TAROT_CARDS[str(card)].card_meaning,
            )
            number += 1
        await ctx.send(embed=embed)

    
