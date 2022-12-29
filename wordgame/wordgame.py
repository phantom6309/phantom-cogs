import json
import random
import discord
from redbot.core import checks, commands, bot
from redbot.core.data_manager import bundled_data_path

# Load the list of words from the wordlist.txt file
word_list = bundled_data_path(self) / "wordlist.txt" 

# Load the scores from the scores.json file, or create an empty dictionary if the file doesn't exist
try:
    with open('scores.json') as f:
        scores = json.load(f)
except FileNotFoundError:
    scores = {}
class Wordgame(commands.Cog):
    """başkalarının renklerine bakın"""
    def __init__(self, bot: bot.Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
# Initialize the bot with a command prefix of '!'
bot = commands.Bot(command_prefix='!')

# Initialize the current game state
current_game = None
current_word = None

# A function to start a new game
def start_game():
    global current_game
    global current_word
    
    # Choose a random word from the word list
    current_word = random.choice(word_list)
    
    # Create a new game object with the current word
    current_game = {
        'word': current_word,
        'players': {}
    }

# A function to end the current game and reset the game state
def end_game():
    global current_game
    global current_word
    
    # Save the scores for each player in the game to the scores dictionary
    for player, score in current_game['players'].items():
        if player in scores:
            scores[player] += score
        else:
            scores[player] = score
    
    # Save the updated scores to the scores.json file
    with open('scores.json', 'w') as f:
        json.dump(scores, f)
    
    # Reset the game state
    current_game = None
    current_word = None

# A function to get the leaderboard as a formatted string
def get_leaderboard():
    # Sort the scores in descending order
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Format the leaderboard as a string
    leaderboard_str = 'Leaderboard:\n'
    for i, (player, score) in enumerate(sorted_scores):
        leaderboard_str += f'{i+1}. {player}: {score} points\n'
    
    return leaderboard_str
# The command to start a new game
@bot.command()
async def wordgame_start(ctx):
    global current_game
    
    # If there is already a game in progress, end the current game first
    if current_game is not None:
        end_game()
    
    # Start a new game
    start_game()
    
    # Announce the start of the game and the first word
    await ctx.send(f'A new word game has started! The first word is "{current_word}".')

# A function to process a word submission
def process_submission(author, word):
    global current_game
    global current_word
    
    # Check if there is a game in progress
    if current_game is None:
        return
    
    # Check if the word is in the word list
    if word not in word_list:
        return
    
    # Check if the word starts with the correct letter
    if word[0] != current_word[-1]:
        return
    
    # Add the player to the game if they haven't played before
    if author not in current_game['players']:
        current_game['players'][author] = 0
    
    # Increment the player's score by the length of the word
    current_game['players'][author] += len(word)
    
    # Update the current word
    current_word = word
# An event handler for message events
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Process the submission if the message starts with the current word
    if message.content.startswith(current_word):
        process_submission(message.author, message.content.split()[0])
    
# The command to show the leaderboard
@bot.command()
async def wordgame_leaderboard(ctx):
    # Get the leaderboard as a string
    leaderboard_str = get_leaderboard()
    
    # Send the leaderboard to the channel
    await ctx.send(leaderboard_str)
