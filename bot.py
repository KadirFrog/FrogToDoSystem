import discord
from discord.ext import commands
import discord_credentials_manager
from time_manager import get_time
import func

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

TOKEN = discord_credentials_manager.get_bot_token()

SERVER_ID = discord_credentials_manager.get_server_id()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="hi", brief="test command which makes the bot say hello.")
async def test(ctx):
    await ctx.send(f"Hello, {ctx.author.display_name}!")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name="new-user", brief="Creates a new user to add tasks to.")
async def create_user(ctx, username):
    await ctx.send(await func.create_user(username, ctx.author.display_name))

bot.run(TOKEN)
