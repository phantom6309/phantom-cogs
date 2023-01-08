# -*- coding: utf-8 -*-
import sqlite3
from collections import defaultdict
from random import randint
import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')
import random

class Kelime:
    """Son kelimenin son harfi ile kelime uydurma oyunu."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=545846965)
        default_guild = {"scores": {}}
        self.config.register_guild(**default_guild)
        self.guild_data = {}
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

    async def give_points(self, ctx, user: discord.User, word: str, message):
        guild_data = self.guild_data[ctx.guild.id]
        game_channel = guild_data["game_channel"]
        used_words = guild_data["used_words"]
        scores = guild_data["scores"]
        previous_user = guild_data["previous_user"]
        current_word = guild_data["current_word"]
        # Compare the user who played the previous word to the current user
        if previous_user == user:
            await game_channel.send(f"Lütfen bekleyin, sıradaki oyuncu oynasın.")
            await game_channel.send(f"Son kelime: {current_word}")
            return
        # Update the previous_user variable
        previous_user = user
        if word in used_words:
            scores[user.id] -= len(word)
            await game_channel.send(f"{word} kelimesi zaten kullanılmış.Yedin eksiyi.")
            emoji2 = '\N{THUMBS DOWN SIGN}'
            await message.add_reaction(emoji2)
            await game_channel.send(f"Son kelime: {current_word}")
        if word[-1] == "ğ":
        # Select a random word from the continue_words list
         new_word = self.word_list[randint(
                0, len(self.word_list) - 1)]
        # Add the new word to the used words list
        used_words.append(new_word)
        # Set the current word to the new word
        current_word = new_word
        await game_channel.send(f"{word} kelimesiyle biten kelime oynayamazsınız. Sıradaki kelime: {current_word}")

        if word in self.word_list and word not in used_words:
         used_words.append(word)
         current_word = word
         scores[user.id] += len(word)
         emoji = '\N{THUMBS UP SIGN}'
         await message.add_reaction(emoji)
         await game_channel.send(f"Son kelime: {current_word}")

    async def remove_points(self, ctx, user: discord.User, word: str, message):
        guild_data = self.guild_data[ctx.guild.id]
        game_channel = guild_data["game_channel"]
        scores = guild_data["scores"]
        scores[user.id] -= len(word)
        emoji2 = '\N{THUMBS DOWN SIGN}'
        await message.add_reaction(emoji2)
        await game_channel.send(f"Son kelime: {current_word}")
        if word not in self.word_list:
            await game_channel.send(
                f"{word} kelimesi geçerli değil. Lütfen sözlükte bulunan bir kelime oynayın."
            )
    async def show_scores(self, ctx):
        guild_data = self.guild_data[ctx.guild.id]
        game_channel = guild_data["game_channel"]
        scores = guild_data["scores"]
        if not scores:
            await game_channel.send("Henüz puan yok.")
            return
        sorted_scores = sorted(
            scores.items(), key=lambda x: x[1], reverse=True
        )
        score_text = "\n".join(
            [f"{self.bot.get_user(user_id)}: {score}" for user_id, score in sorted_scores]
        )
        await game_channel.send(f"Puanlar:\n{score_text}")
        async def end_game(self, ctx):
        guild_data = self.guild_data[ctx.guild.id]
        game_channel = guild_data["game_channel"]
        scores = guild_data["scores"]
        winning_score = guild_data["winning_score"]
        if not scores:
            await game_channel.send("Henüz puan yok.")
            return
        sorted_scores = sorted(
            scores.items(), key=lambda x: x[1], reverse=True
        )
        winner = self.bot.get_user(sorted_scores[0][0])
        await game_channel.send(f"Oyun bitti! Kazanan: {winner}")
        for user_id, score in sorted_scores:
            if score >= winning_score:
                self.cursor.execute(
                    "SELECT score FROM scores WHERE user_id = ?", (user_id,)
                )
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute(
                        "UPDATE scores SET score = ? WHERE user_id = ?",
                        (result[0] + score, user_id),
                    )
                else:
                    self.cursor.execute(
                        "INSERT INTO scores (user_id, score) VALUES (?, ?)",
                        (user_id, score),
                    )
        self.conn.commit()
        self.guild_data[ctx.guild.id] = {
            "game_channel": game_channel,
            "current_word": "",
            "previous_user":
            
    @commands.command(name="basla")
    @commands.guild_only()
    async def start_game(self, ctx, winning_score: int):
        self.guild_data[ctx.guild.id] = {
            "game_channel": ctx.channel,
            "current_word": "",
            "previous_user": None,
            "winning_score": winning_score,
            "used_words": [],
            "scores": defaultdict(int),
        }
        await ctx.send(f"Oyun başladı! Kazanmak için {winning_score} puana ihtiyacınız var.")

    @commands.command(name="bitir")
    @commands.guild_only()
    async def end_game(self, ctx):
        await self.end_game(ctx)

    @commands.command(name="puanlar")
    @commands.guild_only()
    async def show_scores(self, ctx):
        await self.show_scores(ctx)

    @commands.command(name="oyna", aliases=["o"])
    @commands.guild_only()
    async def play_word(self, ctx, *, word: str):
        await self
