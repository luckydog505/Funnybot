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
        all_values = sheet.get_all_values()  # Get all values from the sheet
        quotes = []
        current_quote = ""
        for row in all_values:
            if row[0]:
                current_quote += row[0] + "\n"  # Append line to current quote
            else:
                if current_quote:
                    quotes.append(current_quote.strip())  # Add completed quote
                    current_quote = ""
        if current_quote:
            quotes.append(current_quote.strip())  # Add last quote if present
        return quotes
    except gspread.exceptions.SpreadsheetNotFound:
        print("Error: Spreadsheet not found.")
        return []
    except Exception as e:
        print(f"Error loading quotes: {e}")
        return []

# Load quotes for a specific character
def load_character_quotes(character_name):
    quotes = load_quotes()
    character_quotes = []
    for quote in quotes:
        lines = quote.splitlines()
        for line in lines:
            if line.startswith(character_name):
                character_quotes.append(line)
    return character_quotes

# Load a single line quote from the entire archive
def load_single_line_quote():
    quotes = load_quotes()
    single_lines = []
    for quote in quotes:
        lines = quote.splitlines()
        single_lines.extend(lines)
    return single_lines

# Bot Setup
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Load token from .env.local
if not TOKEN:
    raise ValueError("Discord bot token not set in environment variables")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.tree.command(name='quote', description='Replies with a random quote from the archive')
async def quote(interaction: discord.Interaction, character: str = None):
    if character:
        quotes = load_character_quotes(character)
    else:
        quotes = load_single_line_quote()
    
    if quotes:
        response = random.choice(quotes)
        if len(response) > 2000:
            response = response[:1997] + "..."  # Truncate response if it exceeds 2000 characters
    else:
        response = 'No quotes found.'
    
    if response.strip():
        await interaction.response.send_message(response)
    else:
        await interaction.response.send_message('No quotes found.')

@bot.event
async def setup_hook():
    await bot.tree.sync()

bot.run(TOKEN)
