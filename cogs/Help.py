import discord
from discord.ext import commands
from discord.ext.commands import cooldown,BucketType
from cogs.usefullTools.dbIntegration import *


class HelpCog(commands.Cog):


	def __init__(self, bot):
		self.bot = bot


	# Help console

	@commands.command()
	@cooldown(1, 3, BucketType.channel)
	async def help(self, ctx, argument=None, page = None):
		mod_role = discord.utils.get(ctx.author.roles, name='Moderator')
		admin_role = discord.utils.get(ctx.author.roles, name='Administrator')



		fun_embed = discord.Embed(
				title = 'Fun commands for Cyberon',
				description=f'**8ball**\nUses AI to give you the best answers to your questions\n**Usage:** `cyb!8ball <question>`\n\n'
							f'**meme**\nSends you a beautifully crafted meme\nUsage `cyb!meme`\n\n'
							f'**dog | doggo | pupper**\nGets you a dog picture\n**Usage:** `cyb!dog`\n\n'
							f'**cat | kitty**\nGets you a cat picture\n**Usage:** `cyb!cat`\n\n'
							f'**fact | facts**\nGets you a random animal fact if it exists\n**Usage:** `cyb!fact <animal>`\n\n'
							f'**asciify**\nASCIIfies your message\n**Usage:** `cyb!asciify <message>`\n\n'
							f'**apod**\nGets you an Astronomy Picture Of the Day\n**Usage:** `cyb!apod`\n\n'
							f'**joke**\nRandom joke has been delivered!\n**Usage:** `cyb!joke`\n\n'
							f'**pjoke**\nGets you a programming related joke\n**Usage:** `cyb!pjoke`\n\n'
							f'**quotes**\nA random quote\n**Usage:** `cyb!quote`\n\n',
				colour=0x01a901
			)

		utils_embed = discord.Embed(
				title = 'Utility commands for cyberon',
				description='**avatar** | **av**\nShows the avatar of the user mentioned\n**Usage:** `cyb!avatar <member_name | member_tag | member_id>`\nIf nothing is provided then it shows your avatar\n\n'
							'**userinfo | ui**\nGives the info of the mentioned user\n**Usage:** `cyb!userinfo <member_name | member_tag | member_id>`\n\n'
							'**serverinfo | si**\nGives the info of the server\n**Usage:** `cyb!serverinfo`, No arguments required\n\n'
							'**servercount | sc**\nShows you how many servers the bot is in and total number of members in those servers combined\n**Usage:** `cyb!sc`, No arguments required\n\n'
							'**wikipedia | wiki | ask | whatis**\nGets you information from the wiki\n**Usage:** `cyb!wiki <query>`\nQuery is necessary\n\n'
							'**howdoi**\nInformation from stackoverflow\n**Usage:** `cyb!howdoi <query>`\nQuery is necessary\n\n'
							'**cipher | morse**\nConverts your message to morse code\n**Usage:** `cyb!cypher <message>`\n\n'
							'**base64**\nEncodes your message to base64\n**Usage:** `cyb!base64 "<message>" <iteration>`\nMessage must be in **quotes**\n\n'
							'**dbase64**\nDecodes your base64 encoded message\n**Usage:** `cyb!dbase64 "<message>"`\nMessage must be in **quotes**\n\n'
							'**qrcode**\nConverts a text to qr code\n**Usage:** `cyb!qrcode <message>`\n\n'
							'**qrdecode**\nDecodes the qr code link provided\n**Usage:** `cyb!qrdecode <url link>`\n\n'
							'**translate**\nTranslates your messag to your desired language\n**Usage:** `cyb!translate <source_anguage> <destination_language> <text>`\n\n'
							'**hack-show**\nGives you a list of websites for hackathons\n**Usage:** `cyb!hack-show`\n\n'
							'**at**\nAesthetifies your message\n**Usage:** `cyb!at <text>`\n\n'
							'**hug**\ngives a hug with intensity 0,6,9,10\n**Usage:** `cyb!hug <member> <intensity>`\n\n'
							'**botstats**\nShows the bot\'s statistics\n**Usage:** `cyb!botstats`\n\n',
				colour=0x01a901
			)

		mod_embed = discord.Embed(
				title = 'Moderation commands for cyberon\nPage 1',
				description=f'**kick**\nKicks the member out of the server\n**Usage:** `cyb!kick <member_name | member_id | member_tag> <reason>`, reason is not neccessary\n\n'
							f'**multikick**\nKicks multiple users out of the guild\n**Usage:** `cyb!multikick <member_name | member_id | member_tag>`, reason is not needed\n\n'
							f'**ban | hardban**\nBans the user from the server, **purging the messages**\n**Usage:** `cyb!ban <member_name | member_id | member_tag> <reason>`, reason is not necessary\n\n'
							f'**softban**\nBans the user from the server, **without removing the messages**\n**Usage:** `cyb!softban <member_name | member_id | member_tag> <reason>`, reason is not necessary\n\n'
							f'**multiban**\nBans multiple users out of the guild\n**Usage:** `cyb!multiban <member_name | member_id | member_tag>`, reason is not needed\n\n'
							f'**unban**\nUnbans the user, you need to know the member\'s name\n**Usage:** `cyb!unban <member_name#discriminator>`\n\n'
							f'**warn**\nWarns the user\n**Usage:** `cyb!warn <member_name | member_id | member_tag> <infraction>`\n\n'
							f'**warns | warnings**\nDisplays the infractions of the user mentioned\n**Usage:** `cyb!warns <member_name | member_id | member_tag>`\n\n'
							f'**clearwarns | clearwarn**\nClears all the infractions of the user\n**Usage:** `cyb!clearwarns <member_name | member_id | member_tag>`\n\n'
							f'\nDo `cyb!help mod 2` to get next page',
				colour=0x01a901
			)
		mod_embed.set_footer(text='Made for hacker community with ❤')

		mod_embed_2 = discord.Embed(
				title = 'Page 2',
				description=f'**mute**\nMutes the user\n**Usage:** `cyb!mute <member_name | member_id | member_tag> <reason>`, reason is not necessary\n\n'
							f'**unmute**\nUnmutes the user\n**Usage:** `cyb!unmute <member_name | member_id | member_tag>`\n\n'
							f'**clear | remove | purge**\nClears messages from the channel where it is used\n**Usage:** `cyb!clear <n>` where `n` is the number of messages to be purged\n\n'
							f'**addrole**\nAdds role to member\n**Usage:** `cyb!addrole <member_name | member_id | member_tag> <role_name>`\n\n'
							f'**removerole | purgerole**\nRemoves role from mentioned member\n**Usage:** `cyb!removerole <member_name | member_id | member_tag> <role_name>`\n\n',
				colour=0x01a901
			)
		mod_embed_2.set_footer(text='Made for hacker community ❤')

		config_embed = discord.Embed(
				title = 'Configuration commands for cyberon',
				description=f'**setwarnthresh | setwarnthreshold**\nSets the warning threshold for the server, beyond which the member gets banned\n**Usage:** `cyb!setwarnthresh <integer>`\n\n'
							f'**clearwanthresh(old) | delwarnthresh(old)**\nClears the warning threshold of the server\n**Usage:** `cyb!clearwarnthresh`\n\n'
							f'**serverconfig | config | serversetup | setup**\nConfigures the channels for moderation logging\n**Usage:** `cyb!config`\n\n'
							f'**showconfig**\nShows channels that are for logging\n**Usage:** `cyb!showconfig <args>`\nArgs can be optional (type `help` to get a list)\n\n',
				colour=0x01a901
			)
		config_embed.set_footer(text='Made for hacker community ❤')

		support_embed = discord.Embed(
				title = 'Support commands for cyberon',
				description=f'**bug | bugs**\nFound any bugs? Use this command to report the bugs\n**Usage:** `cyb!bugs "<message>"`\n\nMessage must be greater than 20 charecters.\nYou can also direct message the bot instead of invoking the command\n\n'
							f'**invite**\nInvite me to your server! 😁\n**Usage:** `cyb!invite`\n\n'
							f'**source | sourcecode**\nWant to know what was I written in? I\'ll send you a github link 😉\n**Usage:** `cyb!source`\nNo argument required\n\n'
							f'**supportserver | ss**\nLink to the support server\n**Usage:** `cyb!ss`\n\n',
				colour=0x01a901
			)
		support_embed.set_footer(text='Made for hacker community ❤')

		hackathons_embed = discord.Embed(
				title = 'hackathon commands for cyberon',
				description=f'**notify | notify**\nnotify Hack a channel for upcoming hackathon notifications.\n**Usage:** `cyb!notify "<channel>"`\n\n'
							f'**unsub**\nUnsubscribe the channel from notifications! 😁\n**Usage:** `cyb!unsub`\n\n'
							f'**web**\nWant to know hackathons from MLH/Devpost/Devfolio? I\'ll send them for you 😉\n**Usage:** `cyb!web "<MLH/devpost/devfolio>"`\n\n',
				colour=0x01a901
			)
		hackathons_embed.set_footer(text='Made for hacker community ❤')


		initial_help_dialogue = discord.Embed(
				title = 'Help command',
				description=f'`cyb!help Fun`\nFun commands\n\n'
				            f'`cyb!help support`\nSupport commands\n\n'
							f'`cyb!help Moderation` | `cyb!help mod`\nModeration commands\n\n'
							f'`cyb!help utils` | `cyb!help util`\nUtility commands\n\n'
							f'`cyb!help config`\nConfiguration commands\n\n'
							f'`cyb!help hackathons`\nHackathons commands\n\n',
				colour=0x01a901
			)
		initial_help_dialogue.set_footer(text='Made for hacker community❤')

		if argument is None:
			await ctx.send(embed=initial_help_dialogue)
		elif argument.lower() == 'fun':
			await ctx.send(embed=fun_embed)
		elif argument.lower() in ['moderation', 'mod']:

			if page == '1' or page is None or page != '2':
				await ctx.send(embed=mod_embed)
			else:
				await ctx.send(embed=mod_embed_2)
		elif argument.lower() in ['utils', 'util']:
			await ctx.send(embed=utils_embed)
		elif argument.lower() == 'config':
			await ctx.send(embed=config_embed)
		elif argument.lower() == 'support':
			await ctx.send(embed=support_embed)
		elif argument.lower() == 'hackathons':
			await ctx.send(embed=support_embed)


	# Help console: Error handling

	@help.error
	async def help_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)
		else:
			await ctx.send(f'An error occured ({error})\nPlease check console for traceback, or raise an issue to cyberon')
			raise error


def setup(bot):
	bot.add_cog(HelpCog(bot))