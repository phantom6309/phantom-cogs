import json
import os
from collections import defaultdict
from random import randint

import discord
from redbot.core import Config, commands
from redbot.core.data_manager import bundled_data_path


class Kelime(commands.Cog):
    """A simple word game where players must guess words that start with the last letter of the previous word."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1049711010310997110)
        default_global = {"scores": {}}
        self.config.register_global(**default_global)
        self.game_channel = None
        self.current_word = ""
        self.winning_score = None
        self.word_list = self.load_word_list()
        self.scores = defaultdict(int)

    def load_word_list(self):
        word_list_path = bundled_data_path(self) / "wordlist.txt"
        with open(word_list_path) as f:
            return [line.strip() for line in f]

    def give_points(self, user: discord.User, word: str):
        self.scores[user.id] += len(word)
    @commands.command()
    async def setchannel(self, ctx, channel: discord.TextChannel):
        self.game_channel = channel
        await ctx.send(f"The game channel has been set to {channel.mention}.")

    @commands.command()
    async def setscore(self, ctx, score: int):
        self.winning_score = score
        await ctx.send(f"The winning score has been set to {score}.")

    @commands.command()
    async def wordlist(self, ctx, *, word: str):
        self.word_list.append(word.lower())
        await ctx.send(f"{word} has been added to the word list.")
    async def update_scores(self):
        scores = {str(k): v for k, v in self.scores.items()}
        await self.config.scores.set(scores)

    @commands.command()
    async def scores(self, ctx):
        scores = await self.config.scores()
        scores = {int(k): v for k, v in scores.items()}
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        message = "Top scores:\n"
        for i, (player_id, score) in enumerate(sorted_scores):
            player = self.bot.get_user(player_id)
            if player is not None:
                message += f"{i + 1}. {player} - {score}\n"
            else:
                message += f"{i + 1}. Unknown player ({player_id}) - {score}\n"
        await ctx.send(message)
    async def on_message(self, message: discord.Message):
        if message.channel == self.game_channel and message.author != self.bot.user:
            word = message.content.lower()
            if word[0] == self.current_word[-1] and word in self.word_list:
                self.current_word = word
                self.give_points(message.author, word)
                if self.scores[message.author.id] >= self.winning_score:
                    await message.channel.send(f"{message.author.mention} has won the game!")
                    self.game_channel = None
                    self.current_word = ""
                    self.winning_score = None
                    self.scores = defaultdict(int)
                else:
                    await message.channel.send("Correct! The next word is:")
            else:
                self.give_points(message.author, word)
    @commands.command()
    async def startgame(self, ctx):
        if self.game_channel is None:
            self.game_channel = ctx.channel
            self.current_word = self.word_list[randint(0, len(self.word_list) - 1)]
            self.winning_score = None
            self.scores = defaultdict(int)
            await ctx.send(f"A new game has been started in {ctx.channel.mention}!")
            await ctx.send(f"The first word is: {self.current_word}")
        else:
            await ctx.send("A game is already in progress.")
    
    @commands.command()
    async def endgame(self, ctx):
        if self.game_channel is not None:
            self.game_channel = None
            self.current_word = ""
            self.winning_score = None
            self.scores = defaultdict(int)
            await ctx.send("The game has been ended.")
        else:
            await ctx.send("There is no game in progress.")
    
    def give_points(self, player, word):
        if word[0] == self.current_word[-1]:
            self.scores[player.id] += len(word)
        else:
            self.scores[player.id] -= 1
        self.update_scores()

 

