import discord
from discord import Intents
import random
import time
import os
from scrapper import advscrape
from scrapper import scrape
from discord.ext import commands
# pylint: disable=unused-wildcard-import
from cogs.usefullTools.dbIntegration import *
intents = Intents.default()
# pylint: disable=assigning-non-slot
intents.members = True

bot = commands.Bot(command_prefix="cyb!",
                   case_insensitive=True, intents=intents)
bot.remove_command('help')
working_directory = os.getcwd()


try:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            bot.load_extension(f"cogs.{filename[:-3]}")
except Exception as e:
    print("Cogs error: Cannot load cogs")
    print("\033[5;37;40m\033[1;33;40mWARNING\033[1;33;40m\033[0;37;40m", end=' ')
    print("Functionality limited!\n")
    print(f"exception thrown:\n{e}")

# Basic stuff


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('cyb!help'))
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
        print(
            f'+[NEW_MEMBER]    {member} has joined the server: {member.guild.name}')

        channel = None
        if fetch_join_log_channel(int(member.guild.id)) is not None:
            channel = bot.get_channel(fetch_join_log_channel(
                int(member.guild.id))["channel_id"])

        if channel is not None:
            embed = discord.Embed(
                title='Member joined the server',
                description=f'Member **{member.name}** joined the server!\nWelcome! My name is cyberon I will be here to help, just say `cyb!help` whenever needed ',
                colour=0x008000
            )
            members = await member.guild.fetch_members().flatten()

            bot_count = sum(people.bot is True for people in members)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name='Number of members',
                            value=len(members) - bot_count)
            embed.add_field(name='Number of bots', value=bot_count)
            embed.set_footer(text=f'id: {member.id}')
            await channel.send(embed=embed)
    except Exception as e:
        raise Exception


@bot.event
async def on_member_remove(member):
    try:
        print(
            f'+[REMOVE_MEMBER]   {member} has left the server: {member.guild.name}')

        delete_warns(member.guild.id, member.id)

        channel = None
        if fetch_leave_log_channel(int(member.guild.id)):
            channel = bot.get_channel(fetch_leave_log_channel(
                int(member.guild.id))["channel_id"])

        if channel is not None:
            embed = discord.Embed(
                title='Member left the server',
                description=f'Member **{member.name}** has left the server!\n:cry: I will miss you',
                colour=0xFF0000
            )
            try:
                members = await member.guild.fetch_members().flatten()

                bot_count = sum(people.bot is True for people in members)
                embed.set_thumbnail(url=member.avatar_url)
                embed.add_field(name='Number of members',
                                value=len(members) - bot_count)
                embed.add_field(name='Number of bots', value=bot_count)
                embed.set_footer(text=f'id: {member.id}')
                await channel.send(embed=embed)
            except:
                pass
    except Exception as e:
        raise Exception


@bot.event
async def on_guild_channel_delete(channel):

    join_channel = None
    if fetch_join_log_channel(int(channel.guild.id)) is not None:
        join_channel = fetch_join_log_channel(
            int(channel.guild.id))["channel_id"]

        if channel.id == join_channel:
            delete_join_log_channel(int(channel.guild.id))

    leave_channel = None
    if fetch_leave_log_channel(int(channel.guild.id)) is not None:
        leave_channel = fetch_leave_log_channel(
            int(channel.guild.id))["channel_id"]

        if channel.id == leave_channel:
            delete_leave_log_channel(int(channel.guild.id))

    log_channel = None
    if fetch_mod_log_channel(int(channel.guild.id)) is not None:
        mod_channel = fetch_mod_log_channel(
            int(channel.guild.id))["channel_id"]

        if channel.id == mod_channel:
            delete_mod_log_channel(int(channel.guild.id))


@bot.event
async def on_guild_remove(guild):

    clear_server_data(guild.id)


@bot.event
async def on_bulk_message_delete(messages):

    message_channel = fetch_message_edit_log_channel(int(messages[0].guild.id))
    if message_channel is not None:

        message_channel = fetch_message_edit_log_channel(
            int(messages[0].guild.id))["channel_id"]
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

        message_channel = fetch_message_edit_log_channel(
            int(message.guild.id))["channel_id"]
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

    if not after.author.bot and before.content != after.content:

        message_channel = fetch_message_edit_log_channel(
            int(before.guild.id))
        if message_channel is not None:

            message_channel = fetch_message_edit_log_channel(int(before.guild.id))[
                "channel_id"]
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
    print(
        "\033[1;31;40mFATAL ERROR\033[0m 1;31;40m\nToken is malformed; invalid token")
