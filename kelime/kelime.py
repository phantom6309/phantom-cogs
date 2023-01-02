import asyncio
from collections import defaultdict
from typing import List
from random import randint
import discord
from redbot.core import Config, checks, commands
from redbot.core.commands import Cog
from redbot.core.data_manager import bundled_data_path


class Kelime(Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.current_word = ""
        self.word_list = self.load_word_list()
        self.game_channel = None
        self.scores = defaultdict(int)
        self.winning_score = None
        self.config = Config.get_conf(self, identifier=2022658916, force_registration=True)
        self.config.register_global(scores={})

    def load_word_list(self) -> List[str]:
        with open(bundled_data_path(self) / "wordlist.txt") as f:
            words = f.readlines()
        return [word.strip() for word in words]

    def save_word_list(self):
        with open(bundled_data_path(self) / "word_list.txt", "w") as f:
            for word in self.word_list:
                f.write(word + "\n")

    async def update_scores(self):
        await self.config.scores.set(self.scores)
        await self.config.update()

    @commands.command()
    async def kelimekanal(self, ctx, channel: discord.TextChannel):
        self.game_channel = channel
        await ctx.send(f"The game will now be played in {channel.mention}.")

    @commands.command()
    @checks.is_owner()
    async def kelimeekle(self, ctx, word: str):
        self.word_list.append(word)
        await ctx.send(f"{word} has been added to the list of valid words.")
        self.save_word_list()
    @commands.command()
    async def setscore(self, ctx, score: int):
        self.winning_score = score
        await ctx.send(f"The winning score has been set to {score}.")

    def give_points(self, user: discord.User, word: str):
        self.scores[user.id] += len(word)

    @tasks.loop(minutes=1.0)
    async def game_loop(self):
        if self.game_channel is None:
            return

        self.current_word = self.word_list[
            randint(0, len(self.word_list) - 1)
        ].lower()
        last_letter = self.current_word[-1]
        await self.game_channel.send(
            f"The current word is: {self.current_word}. Guess a word that starts with the letter {last_letter}."
        )
        self.game_loop.reset()

    @game_loop.before_loop
    async def before_game_loop(self):
        await self.bot.wait_until_ready()
    async def check_guess(self, message: discord.Message):
        if message.channel != self.game_channel:
            return
        if message.author.id == self.bot.user.id:
            return

        guess = message.content.lower()
        if guess[0] == self.current_word[-1]:
            if guess in self.word_list:
                self.give_points(message.author, guess)
                await message.channel.send(
                    f"{message.author.mention} guessed the correct word: {guess}! They have been awarded {len(guess)} points."
                )
                await self.update_scores()
                if self.scores[message.author.id] >= self.winning_score:
                    await message.channel.send(
                        f"{message.author.mention} has reached the winning score of {self.winning_score} and has won the game!"
                    )
                    self.scores[message.author.id] = 0
                    self.current_word = ""
                    self.game_loop.cancel()
                else:
                    self.game_loop.reset()
            else:
                await message.channel.send(
                    f"{message.author.mention} guessed the incorrect word: {guess}."
                )
                self.scores[message.author.id] -= 1
                await self.update_scores()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        await self.check_guess(message)
    @commands.command()
    async def kelimepuan(self, ctx):
        sorted_scores = sorted(
            self.scores.items(), key=lambda item: item[1], reverse=True
        )
        message = "Current scores:\n"
        for user_id, score in sorted_scores:
            user = ctx.guild.get_member(user_id)
            if user is not None:
                message += f"{user.display_name}: {score}\n"
        await ctx.send(message)

    @commands.command()
    async def kelimesıfırla(self, ctx):
        self.scores = defaultdict(int)
        self.current_word = ""
        self.game_loop.cancel()
        await ctx.send("The game has been reset.")
        await self.update_scores()
    @commands.command()
    async def kelimebaşla(self, ctx):
        if self.game_channel is None:
            await ctx.send("No game channel has been set. Use `[p]setchannel` to set the game channel.")
            return
        if self.winning_score is None:
            await ctx.send("No winning score has been set. Use `[p]setscore` to set the winning score.")
            return
        self.game_loop.start()
        await ctx.send("The game has been started.")

    @commands.command()
    async def kelimedur(self, ctx):
        self.game_loop.cancel()
        self.current_word = ""
        await ctx.send("The game has been stopped.")
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        scores = await self.config.scores()
        self.scores = defaultdict(int, scores.get(str(guild.id), {}))
        if self.game_channel is None:
            self.game_channel = guild.text_channels[0]

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        scores = await self.config.scores()
        scores[str(guild.id)] = dict(self.scores)
        await self.config.scores.set(scores)
        self.scores = defaultdict(int)
