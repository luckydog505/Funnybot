import discord
from discord.ext import commands
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

# Load environment variables from .env.local
load_dotenv(".env.local")

# Set up Google Sheets API
def setup_google_sheets():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)  # Your credentials JSON file
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Error setting up Google Sheets API: {e}")
        return None

# Load quotes from Google Sheets
def load_quotes():
    try:
        client = setup_google_sheets()
        if client is None:
            return []

        sheet = client.open("Discord Quotes").sheet1  # Replace with your Google Sheet name
        quotes = sheet.col_values(1)  # Assuming all quotes are in the first column
        return quotes
    except gspread.exceptions.SpreadsheetNotFound:
        print("Error: Spreadsheet not found.")
        return []
    except Exception as e:
        print(f"Error loading quotes: {e}")
        return []

# Bot Setup
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Load token from .env.local
if not TOKEN:
    raise ValueError("Discord bot token not set in environment variables")

intents = discord.Intents.default()
intents.message_content = True  # Enables your bot to read message content

bot = commands.Bot(command_prefix='!', intents=intents)

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
