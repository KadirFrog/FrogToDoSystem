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


@bot.command(name="new", brief="Creates a new task for someone.")
async def add_task(ctx, task_name, deadline, for_whom):
    task_creation_date = get_time()
    task_author = ctx.author.display_name
    await ctx.send(await func.add_task(task_name, deadline, task_author, task_creation_date, for_whom))


@bot.command(name="description", brief="Adds a description to all tasks of all users with the name given.")
async def add_description(ctx, arg1, *, arg2):
    description = arg2
    task_name = arg1
    await ctx.send(await func.add_description_to_task(task_name, description, ctx.author.display_name))


@bot.command(name="delete-user", brief="Deletes a user from system with its corresponding task-data.")
async def del_user(ctx, user_name):
    await ctx.send(await func.delete_user(user_name, ctx.author.display_name))


@bot.command(name="list", brief="Lists all tasks of a user.")
async def list_taks(ctx, user_name):
    await ctx.send(await func.show_tasks(user_name, ctx.author.display_name))


@bot.command(name="done",
             brief="Sets a command as 'done' removing it from every user and logging it to the 'done-file'.")
async def set_task_done(ctx, task_name):
    try:
        await ctx.send(await func.task_done(task_name, ctx.author.display_name))
    except Exception as e:
        await ctx.send(f"Task not found: {e}")
        await func.error_log(str(e), ctx.author.display_name)


@bot.command(name="recent", brief="Shows the recently done tasks.")
async def recently_done(ctx, i):
    print(i)
    try:
        i = int(i)
        await ctx.send(await func.recently_done(ctx.author.display_name, i))
        return
    except:
        await ctx.send("Unvalid input: " + i)
        return


bot.run(TOKEN)
