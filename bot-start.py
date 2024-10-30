import discord
from discord.ext import commands
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)  # Your credentials JSON file
client = gspread.authorize(creds)

# Load quotes from Google Sheets
def load_quotes():
    sheet = client.open("Quotes Archive").sheet1  # Replace with your Google Sheet name
    quotes = sheet.col_values(1)  # Assuming all quotes are in the first column
    return quotes

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
