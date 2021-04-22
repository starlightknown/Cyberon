import os, sys, discord
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot
prefix = config.BOT_PREFIX
@commands.command(name="help")
async def hlp(ctx):
    if isadmin(ctx.message.author, ctx.guild.id):
        await ctx.send(
            "**Cyberon to the rescue**\n"
            "**Help**\n"
            f"- `{prefix}lists all the commands.\n"

            "**General**\n"

            f"- `{prefix}new` starts the creation process for a new"
            " reaction role message.\n"
            f"- `{prefix}edit` edits the text and embed of an existing reaction"
            " role message.\n"
            f"- `{prefix}reaction` adds or removes a reaction from an existing"
            " reaction role message.\n"
            f"- `{prefix}notify` toggles sending messages to users when they get/lose"
            " a role (default off) for the current server (the command affects only"
            " the server it was used in).\n"
            f"- `{prefix}info` get information about the bot\n"
            f"- `{prefix}hack-show` get information and links about hackathons at one place\n"
            f"- `{prefix}serverinfo` get information about the server\n"
            f"- `{prefix}ping` scare the bot by pinging\n"
            f"- `{prefix}invite` invite the bot to your server\n"
            f"- `{prefix}server` get invite link of the server of the bot for support\n"
            f"- `{prefix}poll` create a poll where members could vote\n"
            f"- `{prefix}say` the bot will say anything you want\n"
            f"- `{prefix}embed` the bot will say anything you want in embeds\n"
            "**Fun**\n"
            f"- `{prefix}rps` play rock paper scissors with the bot\n"
            f"- `{prefix}green-squares` check your love for open source\n"

        )
        await ctx.send(
            "**Admins**\n"
            f"- `{prefix}admin` adds the mentioned role to the list of "
            " admins, allowing them to create and edit reaction-role messages."
            " You need to be a server administrator to use this command.\n"
            f"- `{prefix}rm-admin` removes the mentioned role from the list of"
            " admins, preventing them from creating and editing"
            " reaction-role messages. You need to be a server administrator to"
            " use this command.\n"
            f"- `{prefix}adminlist` lists the current admins on the server the"
            " command was run in by mentioning them and the current admins from"
            " other servers by printing out the role IDs. You need to be a server"
            " administrator to use this command.\n"
            f"- `{prefix}blacklist` Lets you add or remove a user from not being able to use the bot.\n"
            f"- `{prefix}kick` kicks a user out of the server.\n"
            f"- `{prefix}nick` changes nickname a user in the server.\n"
            f"- `{prefix}ban` bans a user from the server.\n"
            f"- `{prefix}warn` warns a user.\n"
            f"- `{prefix}purge` deletes a number of messages.\n"
            "**Bot Control**\n"
            f"- `{prefix}shutdown` shuts down the bot.\n"
            
        )

    else:
        await ctx.send("You do not have an admin role.")
        prefix = config.BOT_PREFIX
        
def setup(bot):
    bot.add_cog(Help(bot))
