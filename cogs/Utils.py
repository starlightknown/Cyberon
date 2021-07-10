import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, MemberConverter
from aiohttp import request
import aiohttp
import asyncio
import wikipedia
from howdoi import howdoi
import random
import requests
from cogs.usefullTools.info import hack_message, parse_data
import urllib.parse

from platform import python_version
import psutil
from psutil import Process, virtual_memory
from datetime import datetime, timedelta
from time import time
from cogs.usefullTools.mlh_hackathons import parse_mlh_resp, get_pages
from pygicord import Paginator


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
                embed = discord.Embed(
                    title=f'{multiple_member_array[0]}', colour=0x0000ff)

            else:
                embed = discord.Embed(
                    title=f'{multiple_member_array[0]}({multiple_member_array[0].display_name})', colour=0x0000ff)

            embed.set_image(url=f'{multiple_member_array[0].avatar_url}')
            await ctx.send(embed=embed)

        elif len(multiple_member_array) > 1:

            multiple_member_array_duplicate_array = []
            for multiple_member_array_duplicate in multiple_member_array:
                if len(multiple_member_array_duplicate_array) < 10:
                    multiple_member_array_duplicate_array.append(
                        multiple_member_array_duplicate.name)
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

    @commands.command(name='hackclub')
    @cooldown(1, 2, BucketType.channel)
    async def hackdclub(self, ctx):
        url = 'https://hackathons.hackclub.com/api/events/upcoming'
        r = requests.get(url)
        result = r.json()
        result1 = {}
        for d in result:
            result1.update(d)
            data = parse_data(result1)
            await ctx.channel.send(embed=hack_message(data))

    @hackdclub.error
    async def hackdclub_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
            raise error

    @commands.command()
    @cooldown(1, 2, BucketType.channel)
    async def mlh(self, ctx):
        url = 'https://mlh.io/seasons/2022/events'
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    result = await resp.read()
        hackathons = parse_mlh_resp(result)
        pages = get_pages(hackathons)

        paginator = Paginator(pages=pages)
        await paginator.start(ctx=ctx)

    @mlh.error
    async def mlh_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
            raise error

    # Userinfo

    @ commands.command(aliases=['ui'])
    @ cooldown(1, 5, BucketType.channel)
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
                colour=0x0000ff,
            )
            embed.set_author(name=f'User Info - {multiple_member_array[0]}')
            embed.set_thumbnail(url=multiple_member_array[0].avatar_url)
            embed.set_footer(text='made by cyberon with ❤')

            embed.add_field(name='ID:', value=multiple_member_array[0].id)
            embed.add_field(name='Member Name:',
                            value=multiple_member_array[0])
            embed.add_field(name='Member Nickname:',
                            value=multiple_member_array[0].display_name)

            embed.add_field(name='Created at: ', value=multiple_member_array[0].created_at.strftime(
                '%a, %#d %B %Y, %I:%M %p UTC'))
            embed.add_field(name='Joined at:', value=multiple_member_array[0].joined_at.strftime(
                '%a, %#d %B %Y, %I:%M %p UTC'))

            if len(roles) == 1:
                embed.add_field(
                    name=f'Roles ({len(roles) - 1})', value='**NIL**')
            else:
                embed.add_field(
                    name=f'Roles ({len(roles) - 1})',
                    value=' '.join(
                        role.mention for role in roles if role.name != '@everyone'),
                )

            embed.add_field(name='Is this my friend beep bop beep?',
                            value=multiple_member_array[0].bot)

            await ctx.send(embed=embed)

        elif len(multiple_member_array) > 1:

            multiple_member_array_duplicate_array = []
            for multiple_member_array_duplicate in multiple_member_array:
                if len(multiple_member_array_duplicate_array) < 10:
                    multiple_member_array_duplicate_array.append(
                        multiple_member_array_duplicate.name)
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

    @ userinfo.error
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

    @ commands.command(aliases=['si'])
    @ cooldown(1, 4, BucketType.channel)
    async def serverinfo(self, ctx):

        members = await ctx.guild.fetch_members().flatten()

        count = sum(1 for people in members if people.bot)

        embed = discord.Embed(
            title=f'{ctx.guild.name} info',
            colour=0x0000ff
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)

        embed.add_field(name='Owner name:', value=f'<@{ctx.guild.owner_id}>')
        embed.add_field(name='Server ID:', value=ctx.guild.id)

        embed.add_field(name='Server region:', value=ctx.guild.region)
        embed.add_field(name='Members:', value=ctx.guild.member_count)
        embed.add_field(name='bots:', value=count)
        embed.add_field(name='Humans:', value=ctx.guild.member_count - count)

        embed.add_field(name='Number of roles:', value=len(ctx.guild.roles))
        embed.add_field(name='Number of boosts:',
                        value=ctx.guild.premium_subscription_count)

        embed.add_field(name='Text Channels:',
                        value=len(ctx.guild.text_channels))
        embed.add_field(name='Voice Channels:',
                        value=len(ctx.guild.voice_channels))
        embed.add_field(name='Categories:', value=len(ctx.guild.categories))

        embed.add_field(name='Created On:', value=ctx.guild.created_at.strftime(
            '%a, %#d %B %Y, %I:%M %p UTC'))

        await ctx.send(embed=embed)

    # Serverinfo: Error handling

    @ serverinfo.error
    async def serverinfo_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f"An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon.")

        raise error

    # Servercount

    @ commands.command(name='servercount', aliases=['sc'])
    @ cooldown(1, 1, BucketType.channel)
    async def servercount(self, ctx):

        member_count = sum(guild.member_count for guild in self.bot.guilds)
        await ctx.send(f'Cyberon is being loved in `{len(self.bot.guilds)}` servers, helping `{member_count}` members')

    # Servercount: cooldown

    @ servercount.error
    async def sc_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
            raise error

    # Wikipedia support

    @ commands.command(name='wikipedia', aliases=['whatis', 'wiki'])
    @ cooldown(1, 2, BucketType.channel)
    async def wiki(self, ctx, *, query=None):
        if query is not None:
            try:
                r = wikipedia.page(query)
            except wikipedia.exceptions.DisambiguationError as e:
                await ctx.send(f"```\n{e}\n```\nThis beep bop bot cannot understand it, be more specific")
                return
            except wikipedia.exceptions.PageError as e:
                await ctx.send(e)
                return
            except wikipedia.exceptions.HTTPTimeoutError:
                await ctx.send("Timeout, please try again later")
                return
            embed = discord.Embed(
                title=r.title,
                description=r.summary[0: 2000],
                colour=0x808080
            )
            async with ctx.typing():
                await asyncio.sleep(2)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Your query is empty {ctx.author.mention}!\nEnter something!")

    # Wikipedia: Error handling

    @ wiki.error
    async def wiki_error(self, ctx, error):
        if isinstance(error, wikipedia.exceptions.DisambiguationError):
            await ctx.send(f'There are many articles that match your query, please be more specific {ctx.author.mention}')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error has occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
            raise error

    # Howdoi stackoverflow API

    @ commands.command(name='howdoi')
    @ cooldown(1, 2, BucketType.channel)
    async def howdoi(self, ctx, *, query=None):
        if query is not None:
            parser = howdoi.get_parser()
            arguments = vars(parser.parse_args(query.split(' ')))

            embed = discord.Embed(
                title=f'how to {query}',
                description=howdoi.howdoi(arguments)
            )
            async with ctx.typing():
                await asyncio.sleep(2)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send(f'What did you wanted to ask? {ctx.author.mention}')

    # Howdoi: Error Handling

    @ howdoi.error
    async def howdoi_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check the console for traceback')
            raise error

    # Morse code cypher

    @ commands.command(name='cypher', aliases=['morse'])
    @ cooldown(1, 2, BucketType.channel)
    async def cypher(self, ctx, *, message):

        MORSE_DICT = {'A': '.-', 'B': '-...',
                      'C': '-.-.', 'D': '-..', 'E': '.',
                      'F': '..-.', 'G': '--.', 'H': '....',
                      'I': '..', 'J': '.---', 'K': '-.-',
                      'L': '.-..', 'M': '--', 'N': '-.',
                      'O': '---', 'P': '.--.', 'Q': '--.-',
                      'R': '.-.', 'S': '...', 'T': '-',
                      'U': '..-', 'V': '...-', 'W': '.--',
                      'X': '-..-', 'Y': '-.--', 'Z': '--..',
                      '1': '.----', '2': '..---', '3': '...--',
                      '4': '....-', '5': '.....', '6': '-....',
                      '7': '--...', '8': '---..', '9': '----.',
                      '0': '-----', ', ': '--..--', '.': '.-.-.-',
                      '?': '..--..', '/': '-..-.', '-': '-....-',
                      '(': '-.--.', ')': '-.--.-'}

        cipher = ''.join(MORSE_DICT[letter] + ' ' if letter != ' ' else ' '
                         for letter in message.upper())

        await ctx.send(f'Here is your secret text from interstellar in morse code, enjoy!:\n```\n{cipher}\n```')

    # Morse code cypher: Error handling

    @ cypher.error
    async def cypher_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        elif isinstance(error, commands.BadArgument):
            await ctx.send('I can not send an empty message to the space traveller, what do you want to convey?')
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
            raise error

    # QR Code generator

    @ commands.command(name='qrcode')
    @ cooldown(1, 5, BucketType.channel)
    async def qr_code_generator(self, ctx, *, message=None):
        if message is not None:
            embed = discord.Embed(
                title='Here is your encoded text',
                colour=0x01a901
            )

            query = urllib.parse.quote(message, safe='')

            url = f'http://api.qrserver.com/v1/create-qr-code/?data={query}'

            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Please enter a message to qrcode encode it")

    # QR Code generator: Error handling

    @ qr_code_generator.error
    async def qr_code_generator_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)
        else:
            await ctx.send(f'An error occured \n```\n{error}\n```\nPlease check console for traceback, or raise an issue to cyberon')
            raise error

    # QR Code reader

    @ commands.command(name='qrdecode')
    @ cooldown(1, 5, BucketType.channel)
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

    @ commands.command(name="hack-show")
    async def hack_show(self, ctx):
        await ctx.send("**Cyberon loves hackathons, find good hackathons here!**\nhttps://devpost.com/hackathons\nhttps://www.hackathon.io/events\nhttps://confs.tech/#\nhttps://mlh.io/seasons/2021/events\nhttp://www.hackalist.org/\nhttps://devfolio.co/\nhttps://angelhack.com/\nhttps://gitcoin.co/hackathons\nhttps://hackathons.hackclub.com/\nhttps://www.incubateind.com/\nhttps://skillenza.com/")

    @ commands.command(name="botabout")
    async def about(self, ctx):
        embed = discord.Embed(
            title=":information_source: About Cyberon",
            description="I'm a bot with a mission, mission impawssible. Call the halp"
            " command via `cyb!help` to receive a message with a full list of commands.",
            color=0x008000)
        embed.add_field(name="Total Servers",
                        value=f"`{len(self.bot.guilds):,}`")
        embed.add_field(name="Total Users", value=f"`{len(self.bot.users):,}`")
        embed.add_field(name="Total Commands",
                        value=f"`{len(self.bot.commands)}`")
        embed.add_field(
            name="Disclaimer",
            value="cyberon does not collect messages or information on any users\n"
            "If issues found, get me my bug spray",
        )
        embed.add_field(name="Bug spray of my code", value="`Karuna#8722`")
        await ctx.send(embed=embed)

    @ commands.command(aliases=['calm'])
    async def anxiety(self, ctx):
        image = random.choice([
            "Hello there, here's a gif for a breathing exercise.\nhttps://media.giphy.com/media/3oxQNhjjZKLPs26Mve/giphy.gif",
            "Hello there, here's a gif for a breathing exercise.\nhttps://i.imgur.com/XbH6gP4.gif",
            "Hello there, here's a gif for a breathing exercise.\nhttps://media.giphy.com/media/8YfwmT1T8PsfC/giphy.gif",
            "Hello there, here's a gif for a breathing exercise.\nhttp://karlolabs.com/wp-content/uploads/2017/01/breathing.gif",
            "Hello there, here's a gif for a breathing exercise.\nhttp://i67.tinypic.com/2qant76.gif",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/monday-destress-3o7WTp5nxyRqh6T21O",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/monday-destress-l0NhWtOfbVze6KzFm",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/monday-destress-xThuWwbtRvTFh7fjxu",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/monday-destress-xThuWqxgKOhbutFyCY",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/monday-destress-xThuWkfIpGNrUnhu9O",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/destressmonday-relax-meditation-l1J9MS2Ia617Kky3u",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/meditation-mAsGwBc4pZGYE",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/square-ZwuBxuIHhIkXm",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/yoga-air-relax-3o7aD2T6zL8bKIt2tq",
            "Hello there, here's a gif for a breathing exercise.\nhttps://giphy.com/gifs/meditation-NwzYTVWay9T6o",
            "Hello there, here's a gif for a breathing exercise.\nhttps://media.boingboing.net/wp-content/uploads/2016/11/tumblr_og31bxrtOn1qls18ho6_400.gif"
        ])
        await ctx.send(image)

    @ commands.command(aliases=['praise'])
    async def compliment(self, ctx):
        randomcomp = random.choice([
            "You're so resourceful.", "You're such a strong person.", 'Your light shines so brightly.',
            'You matter, and a lot.', "You have an incredible talent even if you don't see it.",
            'You are deserving of a hug right now.', "You're more helpful than you realize.", 'You can inspire people.',
            'I bet you do the crossword puzzle in ink.',
            "You're someone's reason to smile, even if you don't realize it.",
            "It's so great to see you're doing your best.", "Your smile can make someone's day.", 'Your ideas matter.',
            'Your feelings matter.', 'Your emotions matter.', 'Your opinions matter.', 'Your needs matter.',
            'Your own vision of the world is unique and interesting.',
            "Even if you were cloned, you'd still be one of a kind. (And the better one between the two.)",
            'You are more unique and wonderful than the smell of a new book.',
            "You're great at being you! No one can replace you - so keep it up.", 'You can get through this.',
            "If you're going through something, remember: this too shall pass.",
            'You deserve to get help if you need it.', 'You - yes you - are valid.', 'You are more than enough.',
            'Your presence is appreciated.', 'You can become whoever you want to be.', 'You deserve to be listened to.',
            'You deserve to be heard.', 'You deserve to be respected.', "You're an absolute bean.",
        ])
        await ctx.send(randomcomp)

    @ commands.command(aliases=['comfort'])
    async def comfortme(self, ctx):
        randomcomf = random.choice(
            ["You've always been able to always figure out how to pick yourself up. You can do it again.",
             "It's so great to see you're doing your best.",
             'You can get through this.',
             "If you're going through something, remember: this too shall pass.",
             "If today was bad, remember that you won't have to repeat this day ever again.",
             "Even if you feel like you're getting nowhere you're still one step ahead of yesterday - and that's still progress.",
             "You're growing so much, and if you can't see it now, you certainly will in a few months.",
             "You're strong for going on even when it's so hard.",
             "If you are having really awful thoughts right now or feeling very insecure, remember that what you think does not always reflect the reality of things.",
             "I know they can be hard to deal with, but even a bot like me knows your emotions are valid and important!",
             "(source: softangelita)\nhttps://78.media.tumblr.com/757d6f9eceacd22e585f5763aed3b6b7/tumblr_pbs2drA9yX1wzarogo1_1280.gif",
             "You are going to be okay. Things are going to be okay. You will see.",
             "(source: princess-of-positivity)\nhttps://78.media.tumblr.com/209ac4a784925d71d3d3c7293b7d75f4/tumblr_o883p7C7e21vwxwino1_1280.jpg",
             "Sit down, take a breath. There’s still time. Your past isn’t going anywhere, the present is right here and the future will wait.",
             "It is never too late to make a positive change in your life.",
             "https://78.media.tumblr.com/14a19b1f5c785c0af5966175c0c87c8f/tumblr_owob0dUAzy1ww31y6o1_500.jpg",
             "Don't be upset if you aren't always doing your absolute best every waking moment. Flowers cannot always bloom.",
             "(source: jessabella-hime)\nhttps://78.media.tumblr.com/b1e54721f7520a6f425c112a67170e63/tumblr_ozi5gdM4de1trvty1o1_500.png",
             "There are good people in this world who do or will help you, care about you, and love you.",
             "(source: harmony-is-happiness)\nhttps://78.media.tumblr.com/37778dd51384fbdba835349e6f0081d5/tumblr_oz8v11c9CC1wssyrbo1_500.jpg",
             "https://78.media.tumblr.com/ed8e14743dac29bbc606fc099ab77ec3/tumblr_nphyqvqGvi1qzz08do1_500.jpg",
             "(source: harmony-is-happiness)\nhttps://78.media.tumblr.com/980109437f848b501d9ac96ed5a9ead0/tumblr_p285yaPKk31wssyrbo2_r2_250.jpg",
             "(source: harmony-is-happiness)\nhttps://78.media.tumblr.com/63a7933dfe6ed98dd00682533d249efe/tumblr_pc558poobr1wssyrbo1_250.jpg",
             "(source: harmony-is-happiness)\nhttps://78.media.tumblr.com/5827e477fff5b22c693c00d94eb19b2a/tumblr_p40de4xrrC1wssyrbo1_250.jpg",
             "It is perfectly okay to rest and take a break from things If you are taking yourself to exhaustion, at that point it isn't your best anymore.",
             "(source: harmony-is-happiness)\nhttps://78.media.tumblr.com/50f06d2360aae36c815b1757326d878d/tumblr_p40de4xrrC1wssyrbo5_r1_250.jpg",
             "Sometimes it's okay if the only thing you did today was breathe.",
             "(source: recovering-and-healing)\nhttps://78.media.tumblr.com/e7b47e53ba372425728f384685748435/tumblr_oc93tmtPBj1ue8qxbo3_r1_250.jpg",
             "(source: positivedoodles)\nhttps://78.media.tumblr.com/c04f396bfd2501b4876c239a329c035b/tumblr_pcutj6i57Z1rpu8e5o1_1280.png",
             "(source: harmony-is-happiness)\nhttps://78.media.tumblr.com/6602114029258f4097fffc33a2ae5887/tumblr_otfj86Xgq91wssyrbo1_r4_250.jpg"])

        await ctx.send(randomcomf)


def setup(bot):
    bot.add_cog(GeneralCog(bot))
