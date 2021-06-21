import discord
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from aiohttp import request
from discord.ext.commands import MemberConverter
import aiohttp
import asyncio
import wikipedia
from howdoi import howdoi
import base64
import random
import urllib.parse
from cogs.usefullTools.dbIntegration import *

from googletrans import Translator

from platform import python_version
import psutil
from psutil import Process, virtual_memory
from datetime import datetime, timedelta
from time import time


class GeneralCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot



	# Avatar fetcher

	@commands.command(aliases=['av'])
	@cooldown(1, 5, BucketType.channel)
	async def avatar(self, ctx, member, override=None):

		if member[0] == '<' and member[1] == '@':
			converter = MemberConverter()
			member = await converter.convert(ctx, member)
		elif member.isdigit():
			member = int(member)
		members = await ctx.guild.fetch_members().flatten()
		multiple_member_array = []

		if isinstance(member, discord.Member):
			for members_list in members:
				if member.name.lower() in members_list.name.lower():
					multiple_member_array.append(members_list)
		elif isinstance(member, int):
			for member_list in members:
				if member_list.id == member:
					multiple_member_array.append(member_list)
		else:
			for members_list in members:
				if member.lower() in members_list.name.lower():
					multiple_member_array.append(members_list)
		if member is discord.Member:
			if member.isdigit() and member.lower() == 'me' and override == 'override':
				embed = discord.Embed(colour=0x0000ff)
				embed.set_image(url=f'{ctx.author.avatar_url}')
				await ctx.send(embed=embed)

		elif len(multiple_member_array) == 1:

			if multiple_member_array[0].name == multiple_member_array[0].display_name:
				embed = discord.Embed(title=f'{multiple_member_array[0]}',colour=0x0000ff)

			else:
				embed = discord.Embed(title=f'{multiple_member_array[0]}({multiple_member_array[0].display_name})',colour=0x0000ff)

			embed.set_image(url=f'{multiple_member_array[0].avatar_url}')
			await ctx.send(embed=embed)

		elif len(multiple_member_array) > 1:

			multiple_member_array_duplicate_array = []
			for multiple_member_array_duplicate in multiple_member_array:
				if len(multiple_member_array_duplicate_array) < 10:
					multiple_member_array_duplicate_array.append(multiple_member_array_duplicate.name)
				else:
					break

			embed = discord.Embed(
					title=f'Search for {member}\nFound multiple results (Max 10)',
					description=f'\n'.join(multiple_member_array_duplicate_array),
					colour=0x808080
				)
			await ctx.send(embed=embed)

		else:
			await ctx.send(f'The member `{member}` does not exist!')
	


	# Avatar fetcher: Error handling

	@avatar.error
	async def avatar_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			embed = discord.Embed(colour=0x0000ff)
			embed.set_image(url=f'{ctx.author.avatar_url}')
			await ctx.send(embed=embed)
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error
    
	# Userinfo

	@commands.command(aliases=['ui'])
	@cooldown(1, 5, BucketType.channel)
	async def userinfo(self, ctx, member):

		if member[0] == '<' and member[1] == '@':
			converter = MemberConverter()
			member = await converter.convert(ctx, member)
		elif member.isdigit():
			member = int(member)

		members = await ctx.guild.fetch_members().flatten()
		multiple_member_array = []


		if isinstance(member, discord.Member):
			for members_list in members:
				if member.name.lower() in members_list.name.lower():
					multiple_member_array.append(members_list)
		elif isinstance(member, int):
			for member_list in members:
				if member_list.id == member:
					multiple_member_array.append(member_list)
		else:
			for members_list in members:
				if member.lower() in members_list.name.lower():
					multiple_member_array.append(members_list)
		if len(multiple_member_array) == 1:

			roles = [role for role in multiple_member_array[0].roles]
			embed = discord.Embed(
				colour = 0x0000ff,
			)
			embed.set_author(name=f'User Info - {multiple_member_array[0]}')
			embed.set_thumbnail(url=multiple_member_array[0].avatar_url)
			embed.set_footer(text='made by cyberon with ❤')

			embed.add_field(name='ID:', value=multiple_member_array[0].id)
			embed.add_field(name='Member Name:', value=multiple_member_array[0])
			embed.add_field(name='Member Nickname:', value=multiple_member_array[0].display_name)

			embed.add_field(name='Created at: ', value=multiple_member_array[0].created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
			embed.add_field(name='Joined at:', value=multiple_member_array[0].joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

			if len(roles) == 1:
				embed.add_field(name=f'Roles ({len(roles) - 1})', value='**NIL**')
			else:
				embed.add_field(
				    name=f'Roles ({len(roles) - 1})',
				    value=' '.join(
				        role.mention for role in roles if role.name != '@everyone'),
				)

			embed.add_field(name='Bot?', value=multiple_member_array[0].bot)

			await ctx.send(embed=embed)


		elif len(multiple_member_array) > 1:

			multiple_member_array_duplicate_array = []
			for multiple_member_array_duplicate in multiple_member_array:
				if len(multiple_member_array_duplicate_array) < 10:
					multiple_member_array_duplicate_array.append(multiple_member_array_duplicate.name)
				else:
					break

			embed = discord.Embed(
					title=f'Search for {member}\nFound multiple results (Max 10)',
					description=f'\n'.join(multiple_member_array_duplicate_array),
					colour=0x808080
				)
			await ctx.send(embed=embed)

		else:
			await ctx.send(f'The member `{member}` does not exist!')


	# Userinfo: Error handling

	@userinfo.error
	async def userinfo_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('```\n$userinfo {member_name}\n          ^^^^^^^^^^^^^\nMissing Required Argument member_name\n```')
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, discord.errors.Forbidden):
			await ctx.send('I am Forbidden from doing this command, please check if `server members intent` is enabled')
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback')
			raise error


	# Server info

	@commands.command(aliases=['si'])
	@cooldown(1, 4, BucketType.channel)
	async def serverinfo(self, ctx):

		members = await ctx.guild.fetch_members().flatten()

		count = sum(1 for people in members if people.bot)

		embed = discord.Embed(
			title = f'{ctx.guild.name} info',
			colour = 0x0000ff
		)
		embed.set_thumbnail(url=ctx.guild.icon_url)

		embed.add_field(name='Owner name:', value=f'<@{ctx.guild.owner_id}>')
		embed.add_field(name='Server ID:', value=ctx.guild.id)

		embed.add_field(name='Server region:', value=ctx.guild.region)
		embed.add_field(name='Members:', value=ctx.guild.member_count)
		embed.add_field(name='bots:', value=count)
		embed.add_field(name='Humans:', value=ctx.guild.member_count - count)

		embed.add_field(name='Number of roles:', value=len(ctx.guild.roles))
		embed.add_field(name='Number of boosts:', value=ctx.guild.premium_subscription_count)

		embed.add_field(name='Text Channels:', value=len(ctx.guild.text_channels))
		embed.add_field(name='Voice Channels:', value=len(ctx.guild.voice_channels))
		embed.add_field(name='Categories:', value=len(ctx.guild.categories))

		embed.add_field(name='Created On:', value=ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))

		await ctx.send(embed=embed)


	# Serverinfo: Error handling

	@serverinfo.error
	async def serverinfo_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f"An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon.")

		raise error


	# Servercount

	@commands.command(name='servercount', aliases=['sc'])
	@cooldown(1, 1, BucketType.channel)
	async def servercount(self, ctx):
		
		member_count = sum(guild.member_count for guild in self.bot.guilds)
		await ctx.send(f'Present in `{len(self.bot.guilds)}` servers, moderating `{member_count}` members')

	
	# Servercount: cooldown

	@servercount.error
	async def sc_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error


	# Wikipedia support

	@commands.command(name='wikipedia', aliases=['whatis', 'wiki'])
	@cooldown(1, 2,BucketType.channel)
	async def wiki(self, ctx, *, query=None):
		if query is not None:
			try:
				r = wikipedia.page(query)
			except wikipedia.exceptions.DisambiguationError as e:
				await ctx.send(f"```\n{e}\n```\nPlease be more accurate with your query")
				return
			except wikipedia.exceptions.PageError as e:
				await ctx.send(e)
				return
			except wikipedia.exceptions.HTTPTimeoutError:
				await ctx.send("Timeout, please try again later")
				return
			embed = discord.Embed(
				title = r.title,
				description = r.summary[0 : 2000],
				colour = 0x808080
			)
			async with ctx.typing():
				await asyncio.sleep(2)
			await ctx.send(embed=embed)
		else:
			await ctx.send(f"Your query is empty {ctx.author.mention}!\nEnter something!")


	# Wikipedia: Error handling

	@wiki.error
	async def wiki_error(self, ctx, error):
		if isinstance(error, wikipedia.exceptions.DisambiguationError):
			await ctx.send(f'There are many articles that match your query, please be more specific {ctx.author.mention}')
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error has occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error


	# Howdoi stackoverflow API

	@commands.command(name='howdoi')
	@cooldown(1, 2, BucketType.channel)
	async def howdoi(self, ctx, *, query=None):
		if query is not None:
			parser = howdoi.get_parser()
			arguments = vars(parser.parse_args(query.split(' ')))

			embed = discord.Embed(
				title = f'how to {query}',
				description = howdoi.howdoi(arguments)
			)
			async with ctx.typing():
				await asyncio.sleep(2)
			await ctx.channel.send(embed=embed)
		else:
			await ctx.send(f'Your query is empty, please ask a question {ctx.author.mention}')


	# Howdoi: Error Handling

	@howdoi.error
	async def howdoi_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback')
			raise error


	# Morse code cypher

	@commands.command(name='cypher', aliases=['morse'])
	@cooldown(1, 2, BucketType.channel)
	async def cypher(self, ctx, *, message):
		
		MORSE_DICT = { 'A':'.-', 'B':'-...', 
					'C':'-.-.', 'D':'-..', 'E':'.', 
					'F':'..-.', 'G':'--.', 'H':'....', 
					'I':'..', 'J':'.---', 'K':'-.-', 
					'L':'.-..', 'M':'--', 'N':'-.', 
					'O':'---', 'P':'.--.', 'Q':'--.-', 
					'R':'.-.', 'S':'...', 'T':'-', 
					'U':'..-', 'V':'...-', 'W':'.--', 
					'X':'-..-', 'Y':'-.--', 'Z':'--..', 
					'1':'.----', '2':'..---', '3':'...--', 
					'4':'....-', '5':'.....', '6':'-....', 
					'7':'--...', '8':'---..', '9':'----.', 
					'0':'-----', ', ':'--..--', '.':'.-.-.-', 
					'?':'..--..', '/':'-..-.', '-':'-....-', 
					'(':'-.--.', ')':'-.--.-'}

		cipher = ''.join(MORSE_DICT[letter] + ' ' if letter != ' ' else ' '
		                 for letter in message.upper())

		await ctx.send(f'Here is your cyphered text:\n```\n{cipher}\n```')


	# Morse code cypher: Error handling

	@cypher.error
	async def cypher_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, commands.BadArgument):
			await ctx.send('What do you want to cypher?')
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error


	# Base64 encoding

	@commands.command(name='base64')
	@cooldown(1, 2, BucketType.channel)
	async def base64(self, ctx, message, iterations=1):

		if iterations <= 20:
			message_bytecode = message.encode('ascii')

			for _ in range(iterations):
				message_bytecode = base64.b64encode(message_bytecode)
				base64_message = message_bytecode.decode('ascii')

			await ctx.send(f'Here is the base64 encoded version encoded {iterations} time(s):\n```\n{base64_message}\n```')
		else:
			await ctx.send(f"Maximum number of iterations possible are 20, **{iterations}** number of ierations not allowed")
		


	# Base64 encoding: Error handling

	@base64.error
	async def base64_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('What are the arguments')
		elif isinstance(error, commands.BadArgument):
			await ctx.send("Please enter your text to be encode in quotes")
		elif isinstance(error, base64.binascii.Error):
			await ctx.send("Please enter a valid base64 encoded message to decrypt {ctx.author.display_name}")
		elif isinstance(error, commands.ExpectedClosingQuoteError):
			await ctx.send("You didnt close the quotes!")
		elif isinstance(error, commands.InvalidEndOfQuotedStringError):
			await ctx.send("Too many quotes!")
		elif isinstance(error, commands.UnexpectedQuoteError):
			await ctx.send("Unexpected quote in non-quoted string")
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error


	# Base64 decoding

	@commands.command(name='dbase64')
	@cooldown(1, 2, BucketType.channel)
	async def base64_decode(self, ctx, message):

		message_bytecode = message.encode('ascii')

		decode_bytecode = base64.b64decode(message_bytecode)
		base64_message = decode_bytecode.decode('ascii')

		await ctx.send(f'Here is the base64 decoded version:\n```\n{base64_message}\n```')
		


	# Base64 decoding: Error handling

	@base64_decode.error
	async def base64_decode_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('What are the arguments')
		elif isinstance(error, commands.BadArgument):
			await ctx.send("Please enter your text to be encode in quotes")
		elif isinstance(error, (base64.binascii.Error, binascii.Error)):
			await ctx.send("Please enter a valid base64 encoded message to decrypt {ctx.author.display_name}")
		elif isinstance(error, UnicodeDecodeError):
			await ctx.send("Please enter a valid base64 encoded message to decrypt {ctx.author.display_name}")
		elif isinstance(error, commands.ExpectedClosingQuoteError):
			await ctx.send("You didnt close the quotes!")
		elif isinstance(error, commands.InvalidEndOfQuotedStringError):
			await ctx.send("Too many quotes!")
		elif isinstance(error, commands.UnexpectedQuoteError):
			await ctx.send("Unexpected quote in non-quoted string")
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error


	# QR Code generator

	@commands.command(name='qrcode')
	@cooldown(1, 5, BucketType.channel)
	async def qr_code_generator(self, ctx, *, message=None):
		if message is not None:
			embed = discord.Embed(
				title = 'Here is your encoded text',
				colour = 0x01a901
			)

			query = urllib.parse.quote(message, safe='')

			url = f'http://api.qrserver.com/v1/create-qr-code/?data={query}'

			embed.set_image(url=url)
			await ctx.send(embed=embed)
		else:
			await ctx.send("Please enter a message to qrcode encode it")


	# QR Code generator: Error handling

	@qr_code_generator.error
	async def qr_code_generator_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error


	# QR Code reader

	@commands.command(name='qrdecode')
	@cooldown(1, 5, BucketType.channel)
	async def qr_code_decode(self, ctx, message):

		encoded_url = urllib.parse.quote(message, safe='')
		

		url = f'http://api.qrserver.com/v1/read-qr-code/?fileurl={encoded_url}&format=json'

		async with request("GET", url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				symbol = data[0]["symbol"]

				if symbol[0]["data"] is not None:
					await ctx.send(f'Here is the decoded qr code:\n```\n{symbol[0]["data"]}\n```')
				else:
					await ctx.send(f'An error occured: **{symbol[0]["error"]}**')


	# QR Code reader: Error handling

	@qr_code_generator.error
	async def qr_code_generator_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error
	
	@commands.command(name="hack-show")
	async def hack_show(self, ctx):
		await ctx.send("**Cyberon loves hackathons, find good hackathons here!**\nhttps://devpost.com/hackathons\nhttps://www.hackathon.io/events\nhttps://confs.tech/#\nhttps://mlh.io/seasons/2021/events\nhttp://www.hackalist.org/\nhttps://devfolio.co/\nhttps://angelhack.com/\nhttps://gitcoin.co/hackathons\nhttps://hackathons.hackclub.com/\nhttps://www.incubateind.com/\nhttps://skillenza.com/")
		
	@commands.command(name="at")
	async def aesthetify(self, ctx: commands.Context, *, a_text):
		ascii_to_wide = {i: chr(i + 0xFEE0) for i in range(0x21, 0x7F)}
		ascii_to_wide.update({0x20: "\u3000", 0x2D: "\u2212"})
		await ctx.message.delete()
		await ctx.send(f"{a_text.translate(ascii_to_wide)}")

	@commands.command(hidden=True)
	@commands.guild_only()
	async def hug(self, ctx, user: discord.Member, intensity: int = 1):
		name = (user.display_name)
		if intensity <= 0:
			msg = "(っ˘̩╭╮˘̩)っ" + name
		elif intensity <= 3:
			msg = "(っ´▽｀)っ" + name
		elif intensity <= 6:
			msg = "╰(*´︶`*)╯" + name
		elif intensity <= 9:
			msg = "(つ≧▽≦)つ" + name
		elif intensity >= 10:
			msg = "(づ￣ ³￣)づ{} ⊂(´・ω・｀⊂)".format(name)
		else:
			raise RuntimeError
		await ctx.send(msg)
	@commands.command(name="botstats")
	async def about(self, ctx):
		embed = discord.Embed(
			title=":information_source: About cyberon",
			description="I'm a bot with a mission, mission impawssible. Call the halp"
            " command via `cyb!help` to receive a message with a full list of commands.",
			color=0x008000)
		embed.add_field(name="Total Servers", value=f"`{len(self.bot.guilds):,}`")
		embed.add_field(name="Total Users", value=f"`{len(self.bot.users):,}`")
		embed.add_field(name="Total Commands", value=f"`{len(self.bot.commands)}`")
		embed.add_field(
            name="Disclaimer",
            value="cyberon does not collect messages or information on any users\n"
            "If issues found, get me my bug spray",
        )
		embed.add_field(name="Bug spray of my code", value="`Karuna#8722`")
		await ctx.send(embed=embed)	
def setup(bot):
	bot.add_cog(GeneralCog(bot))
