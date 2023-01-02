import json
import os
from collections import defaultdict
from random import randint

import discord
from redbot.core import Config, commands
from redbot.core.data_manager import bundled_data_path
from redbot.core.commands import Cog

class Kelime(commands.Cog):
    """A simple word game where players must guess words that start with the last letter of the previous word."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        default_global = {"scores": {}}
        self.game_channel = None
        self.current_word = ""
        self.winning_score = None
        self.word_list = self.load_word_list()
        self.scores = defaultdict(int)
        try:
         with open("scores.json") as f:
            self.scores = json.load(f)
        except FileNotFoundError:
         self.update_scores()

    def load_word_list(self):
        word_list_path = bundled_data_path(self) / "wordlist.txt"
        with open(word_list_path) as f:
            return [line.strip() for line in f]
    
    

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
     if not os.path.exists("scores.json"):
        with open("scores.json", "w") as f:
            json.dump({}, f)
     with open("scores.json", "w") as f:
        json.dump(self.scores, f)

    @commands.command()
    async def scores(self, ctx):
     with open("scores.json") as f:
        scores = json.load(f)
     sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
     message = "Top scores:\n"
     for i, (player_id, score) in enumerate(sorted_scores):
        player = self.bot.get_user(int(player_id))
        if player is not None:
            message += f"{i + 1}. {player} - {score}\n"
        else:
            message += f"{i + 1}. Unknown player ({player_id}) - {score}\n"

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

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.game_channel is not None and message.channel == self.game_channel and message.author != self.bot.user:
            word = message.content.strip()
            if word[0] == self.current_word[-1] and word in self.word_list:
                self.current_word = word
                if word in self.word_list:
                 self.scores[int(message.author.id)] += len(word)
                else:
                 self.scores[int(message.author.id)] -= 1
                if self.winning_score is not None and self.scores[message.author.id] >= self.winning_score:
                    await message.channel.send(f"{message.author.mention} has won the game!")
                    self.game_channel = None
                    self.current_word = ""
                    self.winning_score = None
                    self.scores = defaultdict(int)
                else:
                    await message.channel.send("Correct!")
            

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