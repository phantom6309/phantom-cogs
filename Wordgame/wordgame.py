import json
import random
import os

import discord
from redbot.core import checks, Config, commands, bot

class WordGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word_list = []
        self.points = {}
        self.current_word = None
        self.previous_word = None

        # Load the word list from the wordlist.json file
        with open('wordlist.json', 'r') as f:
            self.word_list = json.load(f)

        # Load the points from the points.json file, if it exists
        if os.path.exists('points.json'):
            with open('points.json', 'r') as f:
                self.points = json.load(f)

    @commands.command(name='wordgame_start')
    async def start(self, ctx):
        # Choose a random word from the word list
        self.current_word = random.choice(self.word_list)

        # Send the word to the channel
        await ctx.send(f'The word is: {self.current_word}')

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.bot.user:
            return

        # Check if the message starts with the last character of the current word
        if message.content[0] == self.current_word[-1]:
            # Check if the word is in the word list
            if message.content not in self.word_list:
                await message.channel.send('That word is not in the list!')
                return

            # Update the points for the user
            if message.author.id in self.points:
                self.points[message.author.id] += len(message.content)
            else:
                self.points[message.author.id] = len(message.content)

            # Save the points to the points.json file
            with open('points.json', 'w') as f:
                json.dump(self.points, f)

            # Set the previous word to the current word
            self.previous_word = self.current_word

            # Choose a new current word
            self.current_word = random.choice(self.word_list)

            await message.channel.send(f'Correct! The new word is: {self.current_word} You now have {self.points[message.author.id]} points.')

