#!/usr/bin/python3
import discord
from discord import Intents
import random
import time
import os
from scrapper import advscrape
from scrapper import scrape
from discord.ext import commands
from cogs.usefullTools.dbIntegration import *
intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="cyb!", case_insensitive=True, intents=intents)
bot.remove_command('help')
working_directory = os.getcwd()



try:
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			bot.load_extension(f"cogs.{filename[:-3]}")
except Exception as e:
	print("Cogs error: Cannot load cogs")
	print("\033[5;37;40m\033[1;33;40mWARNING\033[1;33;40m\033[0;37;40m", end=' ')
	print("Functionality limited!\n")
	print(f"exception thrown:\n{e}")

sad_words = ["sad","upset","depressed","depressing","anxiety","anxious","hopeless","failed","fail","failure","lost","unhappy","angry","miserable"]
funny_videos = ["https://www.youtube.com/watch?v=ByH9LuSILxU", "https://www.youtube.com/watch?v=vLDcCvCJ8bM","https://www.youtube.com/watch?v=pOmu0LtcI6Y"]
hope_quotes = ["Hope can be a powerful force. Maybe there's no actual magic in it, but when you know what you hope for most and hold it like a light within you, you can make things happen, almost like magic. - Laini Taylor", "When things go wrong, don't go with them. - Elvis Presley", "The bravest thing I ever did was continuing my life when I wanted to die. - Juliette Lewis", "Even in the grave, all is not lost. - Edgar Allan Poe", "One should . . . be able to see things as hopeless and yet be determined to make them otherwise. - F.Scott Fitzgerald", "Don't lose hope. You never know what tomorrow might change. - Laura Chouette", "Sad is not the land with no hero. Sad is the land that needs a hero. - Bertolt Brecht", "Sometimes its hard to see the light at the end of a tunnel. Sometimes you don't even know its there - Campbell Thompson", "When you pray and hope for a change. Don't expect a change to come. Expect the opportunity for a change to come. - Jonathon Anthony Burkett","Never be defined by what has happened to you in the past, it was just a life lesson, not a life sentence. ~ Donald Pillai" , "No matter what happens, as long as you think positively, hopelessness can never touch you! - Mehmet Murat ildan"]
failure_quotes = ["Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill", "There is only one thing that makes a dream impossible to achieve: the fear of failure. - Paulo Coelho", "Failure is the condiment that gives success its flavor. - Truman Capote", "It is hard to fail, but it is worse never to have tried to succeed. - Theodore Roosevelt", "All of old. Nothing else ever. Ever tried. Ever failed. No matter. Try again. Fail again. Fail better. - Samuel Beckett", "Do not let arrogance go to your head and despair to your heart; do not let compliments go to your head and criticisms to your heart; do not let success go to your head and failure to your heart. - Roy T. Bennett", "Only those who dare to fail greatly can ever achieve greatly. - Robert F. Kennedy", "You may be disappointed if you fail, but you are doomed if you don’t try. - Beverly Sills", "You make mistakes, mistakes don't make you - Maxwell Maltz", "Sometimes, when we want something so badly, we fear failure more than we fear being without that thing. - Matthew J. Kirby", "When we give ourselves permission to fail..we at the same time, give ourselves permission to excel. - Eloise Ristad","How much you can learn when you fail determines how far you will go into achieving your goals. - Roy Bennett","I have failed many times, and that's why I am a success. - Michael Jordon", "The man who has done his level best…is a success, even though the world write him down a failure. - B. Forbes", "Failure is the sourness that makes success All the more sweeter. - Joshua Wisenbaker", "The moment you believe you will fail, you have already lost the battle. - Bianca Frazier"]

# Basic stuff

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('with baby shark do do do'))
	print("+[ONLINE] Cyberon is online")

@bot.event
async def on_guild_join(guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("```Hello!I'm Cyberon, Thank you for inviting me!\nCommand Prefix: cyb!\nFor help in commands type: cyb! help```")
                await channel.send("To start configuration of your server use `cyb!help config` command.")
                break

@bot.event
async def on_member_join(member):
	try:
		print(f'+[NEW_MEMBER]    {member} has joined the server: {member.guild.name}')
		
		channel = None
		if fetch_join_log_channel(int(member.guild.id)) is not None:
			channel = bot.get_channel(fetch_join_log_channel(int(member.guild.id))["channel_id"])

		if channel is not None:
			embed = discord.Embed(
					title = 'Member joined the server',
					description=f'Member **{member.name}** joined the server!',
					colour=0x008000
				)
			members = await member.guild.fetch_members().flatten()

			bot_count = 0
			for people in members:
				if people.bot is True:
					bot_count += 1

			embed.set_thumbnail(url=member.avatar_url)
			embed.add_field(name='Number of members', value=len(members) - bot_count)
			embed.add_field(name='Number of bots', value=bot_count)
			embed.set_footer(text=f'id: {member.id}')
			await channel.send(embed=embed)
		else:
			pass
	except Exception as e:
		raise Exception



@bot.event
async def on_member_remove(member):
	try:
		print(f'+[REMOVE_MEMBER]   {member} has left the server: {member.guild.name}')

		delete_warns(member.guild.id, member.id)

		channel = None
		if fetch_leave_log_channel(int(member.guild.id)):
			channel = bot.get_channel(fetch_leave_log_channel(int(member.guild.id))["channel_id"])


		if channel is not None:
			embed = discord.Embed(
				title = 'Member left the server',
				description=f'Member **{member.name}** has left the server!',
				colour=0xFF0000
			)
			try:
				members = await member.guild.fetch_members().flatten()

				bot_count = 0
				for people in members:
					if people.bot is True:
						bot_count += 1

				embed.set_thumbnail(url=member.avatar_url)
				embed.add_field(name='Number of members', value=len(members) - bot_count)
				embed.add_field(name='Number of bots', value=bot_count)
				embed.set_footer(text=f'id: {member.id}')
				await channel.send(embed=embed)
			except:
				pass
		else:
			pass
	except Exception as e:
		raise Exception

@bot.event
async def on_guild_channel_delete(channel):

	join_channel = None
	if fetch_join_log_channel(int(channel.guild.id)) is not None:
		join_channel = fetch_join_log_channel(int(channel.guild.id))["channel_id"]

		if channel.id == join_channel:
			delete_join_log_channel(int(channel.guild.id))

	leave_channel = None
	if fetch_leave_log_channel(int(channel.guild.id)) is not None:
		leave_channel = fetch_leave_log_channel(int(channel.guild.id))["channel_id"]

		if channel.id == leave_channel:
			delete_leave_log_channel(int(channel.guild.id))

	log_channel = None
	if fetch_mod_log_channel(int(channel.guild.id)) is not None:
		mod_channel = fetch_mod_log_channel(int(channel.guild.id))["channel_id"]

		if channel.id == mod_channel:
			delete_mod_log_channel(int(channel.guild.id))

@bot.event
async def on_guild_remove(guild):

	clear_server_data(guild.id)

@bot.event
async def on_bulk_message_delete(messages):


	message_channel = fetch_message_edit_log_channel(int(messages[0].guild.id))
	if message_channel is not None:

		message_channel = fetch_message_edit_log_channel(int(messages[0].guild.id))["channel_id"]
		message_channel = bot.get_channel(message_channel)

		embed = discord.Embed(
				title='Bulk message delete',
				description=f'{len(messages)} messages deleted in {messages[0].channel.mention}',
				color=0xff0000
		)

		if message_channel.id != messages[0].channel.id:
			await message_channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
	
	message_channel = fetch_message_edit_log_channel(int(message.guild.id))
	if message_channel is not None:

		message_channel = fetch_message_edit_log_channel(int(message.guild.id))["channel_id"]
		message_channel = bot.get_channel(message_channel)

		embed = discord.Embed(
				title='Message deleted',
				description=f'Message deleted in {message.channel.mention}\nContents:\n```\n{message.content}\n```\n'
							f'Author of the message:\n{message.author.mention}',
				color=0xff0000
		)

		if message_channel.id != message.channel.id:
			await message_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):

	if not after.author.bot:
		if before.content != after.content:

			message_channel = fetch_message_edit_log_channel(int(before.guild.id))
			if message_channel is not None:

				message_channel = fetch_message_edit_log_channel(int(before.guild.id))["channel_id"]
				message_channel = bot.get_channel(message_channel)

				embed = discord.Embed(
						title='Message edited',
						description=f'Message edited in {before.channel.mention}\nbefore:\n```\n{before.content}\n```\n\nAfter:\n```\n{after.content}\n```\n'
									f'Author of the message:\n{after.author.mention}\n'
									f'[jump](https://discordapp.com/channels/{after.guild.id}/{after.channel.id}/{after.id}) to the message',
						color=0xff0000
				)

				if message_channel.id != before.channel.id:
					await message_channel.send(embed=embed)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if sad_words[2] in message.content or sad_words[3] in message.content:
		await message.channel.send("You're not alone. This bot has a heart. Type in cyb!calm or cyb!confort I'll be there for you")
		e = discord.Embed(title="There there")
		e.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/0e44ab3f-a9dc-4693-86b5-cba1ff8a9ef8/d863gzq-71e41b18-1df5-4d2b-b09b-b1d20179f67e.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvMGU0NGFiM2YtYTlkYy00NjkzLTg2YjUtY2JhMWZmOGE5ZWY4XC9kODYzZ3pxLTcxZTQxYjE4LTFkZjUtNGQyYi1iMDliLWIxZDIwMTc5ZjY3ZS5naWYifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.HIyNCC7QhFON8w6dlUl2sg4u87zg6_cenA_xO4jrSkQ")
		await message.channel.send(embed=e)
		await message.channel.send("Please allow me to distract you with cute and funny cat videos. Hope it makes you feel better.")
		await message.channel.send(random.choice(funny_videos))
	if sad_words[4] in message.content or sad_words[5] in message.content:
		await message.channel.send(random.choice(hope_quotes))
	if sad_words[6] in message.content or sad_words[7] in message.content:
		await message.channel.send(random.choice(failure_quotes))
	

@bot.command()
async def search(ctx, *message):
    query = (" ").join(message)
    print(message)
    URL = "https://www.google.com/search?q=" + query
    item, link = scrape(URL)
    await ctx.send(item.text)
    await ctx.send(link)

@bot.command()
async def advsearch(ctx, *message):
    query = (" ").join(message)
    print(message)
    URL = "https://www.google.com/search?q=" + query
    item = advscrape(URL)
    await ctx.send(item.text)

# Ping

@bot.command()
async def ping(ctx):
	await ctx.send(f'Ping: {round(bot.latency * 1000)}ms')

# If the user enters something bonkers

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):

		await ctx.send(f"command not found\nPlease use `cyb!help` to see all commands")


TOKEN = os.getenv("BOT_TOKEN")
try:
	if TOKEN is None:
		try:
			with open('./token.0', 'r', encoding='utf-8') as file_handle:
				TOKEN = file_handle.read()
				if TOKEN is not None:
					print('Using token found in token file..')
					bot.run(TOKEN)
				else:
					print("Token error: Token not found")
		except FileNotFoundError:
			print("No token file or environment variable\nQuitting")
	else:
		print('Using token found in Environment variable....')
		bot.run(TOKEN)
except discord.errors.LoginFailure:
	print("\033[1;31;40mFATAL ERROR\033[0m 1;31;40m\nToken is malformed; invalid token")