import discord
from discord.ext import commands
import discord_credentials_manager
from time_manager import get_time

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

TOKEN = discord_credentials_manager.get_bot_token()

SERVER_ID = discord_credentials_manager.get_server_id()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="hi", brief="test command which makes the bot say hello")
async def hello(ctx):
    await ctx.send("Hello!")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

bot.run(TOKEN)
