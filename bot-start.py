import discord
from discord.ext import commands
import random
import json

# Load quotes from the JSON file
def load_quotes():
    with open('quotes.json', 'r') as f:
        return json.load(f)

# Bot Setup
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='quote', help='Replies with a random quote from the archive')
async def quote(ctx):
    quotes = load_quotes()
    if quotes:
        response = random.choice(quotes)
    else:
        response = 'No quotes found.'
    
    await ctx.send(response)

bot.run(TOKEN)
