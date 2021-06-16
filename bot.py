import os
import platform
import random
import sys
import logging
from dotenv import load_dotenv
load_dotenv('.env')
import discord
import yaml
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, CommandInvokeError, MissingRole, Bot
from discord.ext import commands, tasks

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

intents = discord.Intents.default()

bot = Bot(command_prefix='cyb!', intents=intents, case_insensitive=True)

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()

bot.TOKEN = os.getenv("TOKEN")

# Setup the game status task of the bot
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["with you!", "cyb! help"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=config["error"]
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=config["error"]
        )
        await ctx.send(embed=embed)
    raise error

@bot.event  # Stops Certain errors from being thrown in the console (Don't remove as it'll cause command error messages to not send! - Only remove if adding features and needed for testing (Don't forget to re-add)!)
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        logging.error('Command Not Found')
        return
    if isinstance(error, MissingRequiredArgument):
        logging.error('Argument Error - Missing Arguments')
        return
    if isinstance(error, CommandInvokeError):
        logging.error('Command Invoke Error')
        return
    if isinstance(error, MissingRole):
        logging.error('A user has missing roles!')
        return
    if isinstance(error, PermissionError):
        logging.error('A user has missing permissions!')
    if isinstance(error, KeyError):
        logging.error('Key Error')
        return
    if isinstance(error, TypeError):
        logging.error('Type Error - Probably caused as server was being registered while anti-spam or double-xp tried triggering')

    raise error
# Run the bot with the token
bot.run(str(bot.TOKEN))
