import discord
import sqlite3
from collections import defaultdict
from random import randint

from redbot.core import Config, commands
from redbot.core.data_manager import bundled_data_path
from redbot.core.commands import Cog


class Kelime(commands.Cog):
    """A simple word game where players must guess words that start with the last letter of the previous word."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=545846965)
        default_global = {"scores": {}}
        self.config.register_global(**default_global)
        self.game_channel = None
        self.current_word = ""
        self.winning_score = None
        self.word_list = self.load_word_list()
        self.conn = sqlite3.connect("scores.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS scores (user_id INTEGER PRIMARY KEY, score INTEGER)"
        )
        self.conn.commit()
        self.scores = defaultdict(int)

    def load_word_list(self):
        word_list_path = bundled_data_path(self) / "wordlist.txt"
        with open(word_list_path) as f:
            return [line.strip() for line in f]

    async def give_points(self, user: discord.User, word: str):
        if word in self.word_list:
            self.scores[user.id] += len(word)
        else:
            self.scores[user.id] -= 1

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
        self.cursor.execute("DELETE FROM scores")
        for user_id, score in self.scores.items():
            self.cursor.execute("INSERT INTO scores VALUES (?, ?)", (user_id, score))
        self.conn.commit()


    @commands.command()
    async def scores(self, ctx):
        self.cursor.execute("SELECT * FROM scores ORDER BY score DESC")
        scores = self.cursor.fetchall()
        message = "Top scores:\n"
        for i, (player_id, score) in enumerate(scores):
            player = self.bot.get_user(player_id)
            if player is not None:
                message += f"{i + 1}. {player} - {score}\n"
            else:
                message += f"{i + 1}. Unknown player ({player_id}) - {score}\n"
        await ctx.send(message)
    
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
                await self.give_points(message.author, word)
                if self.winning_score is not None:
                    user_score = self.scores[message.author.id]
                    if user_score >= self.winning_score:
                        await message.channel.send(
                            f"{message.author} wins with a score of {user_score}!"
                        )
                        await self.update_scores()
                        self.game_channel = None
                        self.current_word = ""
                        self.winning_score = None
                        self.scores = defaultdict(int)
                else:
                    await message.channel.send(f"{message.author} played {word}")
            else:
                await self.give_points(message.author, word)
   
    @commands.command()
    async def stopgame(self, ctx):
        if self.game_channel is not None:
            self.game_channel = None
            self.current_word = ""
            self.winning_score = None
            self.scores = defaultdict(int)
            await ctx.send("The game has been stopped.")
        else:
            await ctx.send("There is no game currently in progress.")

    @commands.command()
    async def currentword(self, ctx):
        if self.current_word:
            await ctx.send(f"The current word is: {self.current_word}")
        else:
            await ctx.send("There is no game currently in progress.")

    @commands.command()
    async def currentscore(self, ctx, user: discord.User = None):
        if self.current_word:
            if user is not None:
                score = self.scores[user.id]
                await ctx.send(f"{user}'s current score is {score}.")
            else:
                await ctx.send(f"Your current score is {self.scores[ctx.author.id]}.")
        else:
            await ctx.send("There is no game currently in progress.")
    
    @commands.command()
    async def wordcount(self, ctx):
        word_count = len(self.word_list)
        await ctx.send(f"The word list currently has {word_count} words.")

