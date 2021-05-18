import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os, sys, discord, random, asyncio

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Usermessages(commands.Cog, name="Usermessages"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="user-messages")
    async def check(self, context, timeframe=7, channel: discord.TextChannel = None, *, user: discord.Member = None):
        if timeframe > 1968:
            await context.channel.send("Sorry. The maximum of days you can check is 1968.")
        elif timeframe <= 0:
            await context.channel.send("Sorry. The minimum of days you can check is one.")

        else:
            if not channel:
                channel = context.channel
            if not user:
                user = context.author

            async with context.channel.typing():
                msg = await context.channel.send('Calculating...')
                await msg.add_reaction('🔎')

                counter = 0
                async for message in channel.history(limit=5000, after=datetime.today() - timedelta(days=timeframe)):
                    if message.author.id == user.id:
                        counter += 1

                await msg.remove_reaction('🔎', member=message.author)

                if counter >= 5000:
                    await msg.edit(content=f'{user} has sent over 5000 messages in the channel "{channel}" within the last {timeframe} days!')
                else:
                    await msg.edit(content=f'{user} has sent {str(counter)} messages in the channel "{channel}" within the last {timeframe} days.')


def setup(bot):
    bot.add_cog(Usermessages(bot))