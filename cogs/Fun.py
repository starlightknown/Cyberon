import discord
import random
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from aiohttp import request
import aiohttp
import asyncio
import pyfiglet
import os
import requests
from cogs.usefullTools.dbIntegration import *
from cogs.usefullTools.info import *

def NASA_API_KEY():
	return os.getenv("NASA_API_KEY")

class FunCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	# the eight ball

	@commands.command(name='8ball')
	@cooldown(1,5,BucketType.channel)
	async def eight_ball(self, ctx, *, question=None):
		if question is not None:
			responses = ["It is certain.",
						 "It is decidedly so.",
						 "Without a doubt.",
						 "Yes - definitely.",
						 "You may rely on it.",
						 "As I see it, yes.",
						 "Most likely.",
						 "Outlook good.",
						 "Yes.",
						 "Signs point to yes.",
						 "Reply hazy, try again.",
						 "Ask again later.",
						 "Better not tell you now.",
						 "Cannot predict now.",
						 "Concentrate and ask again.",
						 "Don't count on it.",
						 "My reply is no.",
						 "My sources say no.",
						 "Outlook not so good.",
						 "Very doubtful."
						 ]

			embed = discord.Embed(title='*The 8ball*', description=f'**{ctx.message.author}** asked a question.\n\nThe question was: **{question}**\n\n\n{random.choice(responses)}', colour=0x0000ff)
			await ctx.send(embed=embed)
		else:
			await ctx.send('Ask me a question!')


	# eightball: Error handling

	@eight_ball.error
	async def eightball_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')


	# Memes

	@commands.command()
	@cooldown(1, 3, BucketType.channel)
	async def meme(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

		meme_url = "https://meme-api.herokuapp.com/gimme?nsfw=false"
		async with request("GET", meme_url, headers={}) as response:
			if response.status==200:
				data = await response.json()
				image_link = data["url"]
			else:
				image_link = None

		async with request("GET", meme_url, headers={}) as response:
			if response.status==200:
				data = await response.json()
				embed = discord.Embed(
					title=data["title"],
					url=image_link,
					colour=random.choice(colour_choices)
				)
				if image_link is not None:
					embed.set_image(url=image_link)
					await ctx.send(embed=embed)

			else:
				await ctx.send(f"The API seems down, says {response.status}")


	# Memes: Error handling

	@meme.error
	async def meme_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback')
			raise error
      
	# Cat pictures

	@commands.command()
	@cooldown(1, 1, BucketType.channel)
	async def cat(self, ctx):
	  
		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

		cat_url = "http://aws.random.cat/meow"
		async with request("GET", cat_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				image_link = data["file"]
				embed = discord.Embed(
						colour= random.choice(colour_choices)
				)
				embed.set_image(url=image_link)
				await ctx.send(embed=embed)

			else:
				await ctx.send(f'The API seems down, says {response.status}')


	# Cat pictures: Error handling

	@cat.error
	async def cat_picture_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback')
			raise error


	# Animal facts

	@commands.command(name='fact', aliases=['facts'])
	async def animal_facts(self, ctx, animal:str):

		if animal.lower() in {'dog', 'cat', 'bird', 'birb', 'koala', 'panda'}:

			fact_url = f"https://some-random-api.ml/facts/{'bird' if animal == 'birb' else animal}"

			image_url=f"https://some-random-api.ml/img/{'bird' if animal == 'bird' else animal}"
			async with request("GET", image_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					image_link = data["link"]
				else:
					image_link = None

			async with request("GET", fact_url, headers={}) as response:
				if response.status == 200:
					data = await response.json()
					description = data["fact"]
					if len(description) > 2045:
						description = f'{data["fact"][:2045].strip()}...'
					else:
						description = data["fact"]

			colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]

			embed = discord.Embed(
				title = f'Facts about {animal.lower()}',
				description=description,
				colour=random.choice(colour_choices)
			)

			if image_link is not None:
				embed.set_image(url = image_link)
			embed.set_footer(text='Made for hacker community ❤')

			await ctx.send(embed=embed)

		else:
			await ctx.send(f"No facts for {animal}")

	# Animal Facts: Error handling

	@animal_facts.error
	async def animal_facts_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Which animal do you want the facts for?")
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error 


	# ASCIIfy your message

	@commands.command(name='asciify')
	@cooldown(1, 1, BucketType.channel)
	async def asciify_message(self, ctx, *, message=None):
		if message is None:
			await ctx.send('Whats it you want to asciify?')

		elif len(message) <= 50:
			if message[0] == '<' and (message[1] == '#'):
				await ctx.send('im not doing that 😂')
			elif message[0] == '<' and message[1] == '@':
				await ctx.send('im not doing that 😂')
			elif ctx.author.is_on_mobile and len(message) > 8:
				await ctx.send('The output might look a bit weird on your phone! 😅\n Landscape mode might make it look Better')
				msg = pyfiglet.figlet_format(message)
				await ctx.send(f'```\n{msg}\n```')
			else:
				msg = pyfiglet.figlet_format(message)
				await ctx.send(f'```\n{msg}\n```')
		else:
			await ctx.send(f"Your character length ({len(message)}) has exceeded a normal of 50.")


	# ASCIIfy: Error handling

	@asciify_message.error
	async def asciify_message_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error

	# APOD

	@commands.command(name='apod')
	@cooldown(1, 2, BucketType.channel)
	async def apod(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff] 

		API = NASA_API_KEY()

		if API is None:
			try:
				with open('./NASA_API_TOKEN.0', 'r', encoding='utf-8') as nasa_api_token_file_handle:
					API = nasa_api_token_file_handle.read()
			except FileNotFoundError:
				await ctx.send(f"There is an issue with the API key, it seems to not exist\nPlease run the `cyb!bug` command to report")
				print("\nNo token file or environment variable\nAPOD command failed to execute")
				return;
		

		apod_url = f'https://api.nasa.gov/planetary/apod?api_key={API}'
		data = None

		async with request("GET", apod_url, headers={}) as response:    
			data = await response.json()

		try:
			if len(data["explanation"]) > 2048:
				description = f"{data['explanation'][:2045].strip()}..."
			else:
				description = data["explanation"]
		except KeyError:
			await ctx.send('There is a problem in the content, please try again')

		embed = discord.Embed(
			title=data["title"],
			description=description,
			color=random.choice(colour_choices)
		)
		if "hdurl" in data.keys():
			embed.set_image(url=data["hdurl"])
		elif "media_type" in data.keys():
			if data["media_type"] == "video":
				url = data["url"]
				embed.add_field(name="video link: ", value=url)
			else:
				embed.set_image(url=data["url"])


		embed.set_footer(text=f"Here is the Astronomy Picture of the Day")

		async with ctx.typing():
			await asyncio.sleep(2)
		await ctx.send(embed=embed)



	# APOD: Error handling

	@apod.error
	async def apod_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error


	# Random Jokes 

	@commands.command(name='joke', aliases=['jokes'])
	@cooldown(1, 2, BucketType.channel)
	async def jokes(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]
		
		jokes_url = 'https://official-joke-api.appspot.com/random_joke'

		async with request("GET", jokes_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				title = data["setup"]
				description = data["punchline"]

				embed = discord.Embed(
								title = title,
								description = description,
								colour = random.choice(colour_choices)
					)
				await ctx.send(embed=embed)
			else:
				await ctx.send(f'The API seems down, say {response.status}')


	# Random jokes: Error handling

	@jokes.error
	async def jokes_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error            


	# Programming jokes

	@commands.command(name='pjoke', aliases=['pjokes'])
	@cooldown(1, 2, BucketType.channel)
	async def programmingjokes(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]
		
		jokes_url = 'https://official-joke-api.appspot.com/jokes/programming/random'

		async with request("GET", jokes_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				title = data[0]["setup"]
				description = data[0]["punchline"]

				embed = discord.Embed(
								title = title,
								description = description,
								colour = random.choice(colour_choices)
					)
				await ctx.send(embed=embed)
			else:
				await ctx.send(f'The API seems down, say {response.status}')


	# Programming jokes: Error handling

	@programmingjokes.error
	async def programmingjokes_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error
			
	@commands.command(name='hacks')
	@cooldown(1, 2, BucketType.channel)
	async def hackathons(self, ctx):
			url = 'https://hackathons.hackclub.com/api/events/upcoming' 
			r = requests.get(url)
			result = r.json()
			result1 = {}
			for d in result:
				result1.update(d)
				break
			data = parse_data(result1)
			await ctx.send(embed = hack_message(data))
			
	@hackathons.error
	async def hackathons_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error

	@commands.command(name='quotes', aliases=['quote'])
	@cooldown(1, 2, BucketType.channel)
	async def quotes(self, ctx):

		colour_choices= [0x400000,0x997379,0xeb96aa,0x4870a0,0x49a7c3,0x8b3a3a,0x1e747c,0x0000ff]
		
		quotes_url = 'http://staging.quotable.io/random'

		async with request("GET", quotes_url, headers={}) as response:
			if response.status == 200:
				data = await response.json()
				
				quote = data["content"]
				author = data["author"]

				await ctx.send(f'```\n{quote}\n```\n**-{author}**')
			else:
				await ctx.send(f"API seems down, says {response.status} code")


	# Quotes: Error handling

	@quotes.error
	async def quotes_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error
	
	@commands.command()
	@cooldown(1, 2, BucketType.channel)
	async def xkcd(self, ctx,  *searchterm: str):
		apiUrl = 'https://xkcd.com{}info.0.json'
		async with aiohttp.ClientSession() as cs:
			async with cs.get(apiUrl.format('/')) as response:
				js = await response.json()
				if ''.join(searchterm) == 'random':
					randomComic = random.randint(0, js['num'])
					async with cs.get(apiUrl.format('/' + str(randomComic) + '/')) as r:
						if response.status == 200:
							js = await r.json()
							comicUrl = 'https://xkcd.com/{}/'.format(js['num'])
							date = '{}.{}.{}'.format(js['day'], js['month'], js['year'])
							msg = '**{}**\n{}\nAlt Text:```{}```XKCD Link: <{}> ({})'.format(js['safe_title'], js['img'], js['alt'], comicUrl, date)
							await ctx.send(msg)
	@xkcd.error
	async def xkcd_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
			raise error		

def setup(bot):
	bot.add_cog(FunCog(bot))
