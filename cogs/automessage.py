import discord
from discord.ext import commands
from time import ctime
from discord.ext.commands import bot
import yaml
import os, sys

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

class message():
    def __init__(self, welcome_id):
        self.id = id(self)
        self.welcome_id = welcome_id

class automessage(commands.Cog, name="automessage"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member, welcome_id):
        channel = automessage.bot.get_channel((welcome_id))
        embedVar = discord.Embed(title="USER JOINED:", description=f"User: **{member.mention}**",
                                 color=0x979c9f)
        embedVar.add_field(name="Time:", value=f"**{ctime()}**", inline=True)
        embedVar.set_footer(text="Welcome to the server!")
        await channel.send(embed=embedVar)

    @commands.Cog.listener()
    async def on_member_remove(self, member, welcome_id):
        channel = automessage.bot.get_channel((welcome_id))
        embedVar = discord.Embed(title="USER LEFT:", description=f"User: **{member.mention}**",
                                 color=0x979c9f)
        embedVar.add_field(name="Time:", value=f"**{ctime()}**", inline=True)
        embedVar.set_footer(text="Goodbye!")
        await channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(automessage(bot))
