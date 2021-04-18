
import discord, asyncio, os, platform, sys
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv('.env')
if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config

intents = discord.Intents.all()

bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents)

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
	bot.loop.create_task(status_task())
	print(f"Logged in as {bot.user.name}")
	print(f"Discord.py API version: {discord.__version__}")
	print(f"Python version: {platform.python_version()}")
	print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
	print("-------------------")

# Setup the game status task of the bot
async def status_task():
	while True:
		await bot.change_presence(activity=discord.Game("with you!"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("with freedom!"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game(f"{config.BOT_PREFIX} help"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("with magic!"))
		await asyncio.sleep(60)

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

# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
	# Ignores if a command is being executed by a bot or by the bot itself
	if message.author == bot.user or message.author.bot:
		return
	# Ignores if a command is being executed by a blacklisted user
	if message.author.id in config.BLACKLIST:
		return
	await bot.process_commands(message)

# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
	fullCommandName = ctx.command.qualified_name
	split = fullCommandName.split(" ")
	executedCommand = str(split[0])
	print(f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
	if isinstance(error, commands.CommandOnCooldown):
		embed = discord.Embed(
			title="Error!",
			description="This command is on a %.2fs cool down" % error.retry_after,
			color=config.error
		)
		await context.send(embed=embed)
	raise error

# Run the bot with the token
bot.run(os.getenv('TOKEN'))
