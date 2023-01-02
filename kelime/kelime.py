# -*- coding: utf-8 -*-
import random
from typing import List
import asyncio
import discord
from redbot.core import Config, commands, tasks
from redbot.core.commands import Cog
from redbot.core.data_manager import bundled_data_path


class WordGame(Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.current_word = ""
        self.word_list = self.load_word_list()
        self.automate_task.start()

    def load_word_list(self) -> List[str]:
        with open(bundled_data_path(self) / "wordlist.txt") as f:
            words = f.readlines()
        return [word.strip() for word in words]

    @commands.command()
    async def startgame(self, ctx):
        self.current_word = random.choice(self.word_list)
        await ctx.send(f"The game has started! The current word is {self.current_word}")

    async def guessword(self, ctx, word: str):
        if not self.current_word:
            await ctx.send("The game has not started yet. Use the `!startgame` command to begin.")
            return

        if word not in self.word_list:
            await ctx.send("That word is not in the list of words.")
            return

        if word[0] != self.current_word[-1]:
            await ctx.send("The word must start with the last letter of the previous word.")
            return

        self.current_word = word
        await ctx.send(f"The current word is now {self.current_word}")

    @tasks.loop(seconds=5.0)
    async def automate_task(self):
        if not self.current_word:
            return

        try:
            message = await self.bot.wait_for("message", check=self.check_message, timeout=30.0)
        except asyncio.TimeoutError:
            return

        ctx = await self.bot.get_context(message)
        await self.guessword(ctx, message.content)

    def check_message(self, message):
        return message.channel == message.channel and message.author != self.bot.user
