import os
import sys
import discord
import yaml
import datetime
from discord.ext import commands

# Only if you want to use variables that are in the config.yaml file.
if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


# Here we name the cog and create a new class for the cog.
class botinfo(commands.Cog, name="botinfo"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="about")
    async def about(self, ctx):
        """Get information about cyberon"""
        embed = discord.Embed(
            title=":information_source: About cyberon",
            description="I'm a bot with a mission, mission impawssible. Call the halp"
            " command via `cyb!help` to receive a message with a full list of commands.",
            color=config["main_color"])
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

    @commands.command(name="invite")
    async def invite(self, ctx):
        """
        Get the invite link of the bot to be able to invite it.
        """
        await ctx.send("I sent you a private message!")
        await ctx.author.send(
            f"Invite me by clicking here: https://discordapp.com/oauth2/authorize?&client_id={config.APPLICATION_ID}&scope=bot&permissions=8")
    
    @commands.command(name="bug-report")
    async def server(self, ctx):
        """
        Report Issues, questions, enhancements or bugs related to bot.
        """
        await ctx.send("Found something odd? Contact my bug spray here: https://github.com/starlightknown/Cyberon/")


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(botinfo(bot))
