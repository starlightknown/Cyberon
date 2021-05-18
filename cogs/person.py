import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os, sys, discord, random, asyncio

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class personwho(commands.Cog, name="personwho"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="user")
    async def whois(self, context, member: discord.Member = None):
        if not member:  # if member is no mentioned
            member = context.message.author  # set member as the author
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.orange(), timestamp=context.message.created_at,
                              title=str(member))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {context.author}")

        embed.add_field(name="Display Name:", value=member.display_name)
        embed.add_field(name="ID:", value=member.id)

        embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1:]]))
        embed.add_field(name="Highest Role:", value=member.top_role.mention)
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(personwho(bot))