import discord, asyncio, os, platform, sys
from discord.ext.commands import Bot
from discord.ext import commands, tasks
from core import database, schema
import datetime, threading
import configparser
import asyncio
from shutil import copy
from sys import platform, exit as shutdown
from dotenv import load_dotenv
load_dotenv('.env')
if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config

intents = discord.Intents.all()
directory = os.path.dirname(os.path.realpath(__file__))
prefix = config.BOT_PREFIX
bot = Bot(command_prefix=config.BOT_PREFIX, intents=intents)

db_file = f"{directory}/files/bot.db"
db = database.Database(db_file)

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
	await database_updates()
	cleandb.start()
	check_cleanup_queued_guilds.start()
	bot.loop.create_task(status_task())
	print(f"Logged in as {bot.user.name}")

# Setup the game status task of the bot
async def status_task():
	while True:
		await bot.change_presence(activity=discord.Game("with you!"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("with freedom!"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game(f"{prefix} help"))
		await asyncio.sleep(60)
		await bot.change_presence(activity=discord.Game("with magic!"))
		await asyncio.sleep(60)

# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

if __name__ == "__main__":
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			extension = file[:-3]
			try:
				bot.load_extension(f"cogs.{extension}")
				print(f"Loaded extension '{extension}'")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"Failed to load extension {extension}\n{exception}")

# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
	# Ignores if a command is being executed by a bot or by the bot itself
	if message.author == bot.user or message.author.bot:
		return
	# Ignores if a command is being executed by a blacklisted user
	if message.author.id in config.BLACKLIST:
		return
	await bot.process_commands(message)

# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
	fullCommandName = ctx.command.qualified_name
	split = fullCommandName.split(" ")
	executedCommand = str(split[0])
	print(f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
	if isinstance(error, commands.CommandOnCooldown):
		embed = discord.Embed(
			title="Error!",
			description="This command is on a %.2fs cool down" % error.retry_after,
			color=config.error
		)
		await context.send(embed=embed)
	raise error

#database - reaction role
class Locks:
    def __init__(self):
        self.locks = {}
        self.main_lock = asyncio.Lock()

    async def get_lock(self, user_id):
    	async with self.main_lock:
    		if user_id not in self.locks:
    			self.locks[user_id] = asyncio.Lock()

    		return self.locks[user_id]
lock_manager = Locks()


def isadmin(member, guild_id):
    # Checks if command author has an admin role that was added with cyb!admin @role
    admins = db.get_admins(guild_id)

    if isinstance(admins, Exception):
        print(f"Error when checking if the member is an admin:\n{admins}")
        return False

    try:
        member_roles = [role.id for role in member.roles]
        return [admin_role for admin_role in admins if admin_role in member_roles]

    except AttributeError:
        # Error raised from 'fake' users, such as webhooks
        return False


async def getchannel(channel_id):
    channel = bot.get_channel(channel_id)

    if not channel:
        channel = await bot.fetch_channel(channel_id)

    return channel


async def getguild(guild_id):
    guild = bot.get_guild(guild_id)

    if not guild:
        guild = await bot.fetch_guild(guild_id)

    return guild


async def getuser(user_id):
    user = bot.get_user(user_id)

    if not user:
        user = await bot.fetch_user(user_id)

    return user

async def database_updates():
    handler = schema.SchemaHandler(db_file, bot)
    if handler.version == 0:
        handler.zero_to_one()
        messages = db.fetch_all_messages()
        for message in messages:
            channel_id = message[1]
            channel = await getchannel(channel_id)
            db.add_guild(channel.id, channel.guild.id)

    if handler.version == 1:
        handler.one_to_two()

    if handler.version == 2:
        handler.two_to_three()


async def system_notification(guild_id, text, embed=None):
    # Send a message to the system channel (if set)
    if guild_id:
        server_channel = db.fetch_systemchannel(guild_id)

        if isinstance(server_channel, Exception):
            await system_notification(
                None,
                "Database error when fetching guild system"
                f" channels:\n```\n{server_channel}\n```\n\n{text}",
            )
            return

        if server_channel:
            server_channel = server_channel[0][0]

        if server_channel:
            try:
                target_channel = await getchannel(server_channel)
                if embed:
                    await target_channel.send(text, embed=embed)
                else:
                    await target_channel.send(text)

            except discord.Forbidden:
                await system_notification(None, text)

        else:
            if embed:
                await system_notification(None, text, embed=embed)
            else:
                await system_notification(None, text)

    else:
        print(text)


async def formatted_channel_list(channel):
    all_messages = db.fetch_messages(channel.id)
    if isinstance(all_messages, Exception):
        await system_notification(
            channel.guild.id,
            f"Database error when fetching messages:\n```\n{all_messages}\n```",
        )
        return

    formatted_list = []
    counter = 1
    for msg_id in all_messages:
        try:
            old_msg = await channel.fetch_message(int(msg_id))

        except discord.NotFound:
            # Skipping emote-role messages that might have been deleted without updating CSVs
            continue

        except discord.Forbidden:
            await system_notification(
                channel.guild.id,
                "I do not have permissions to edit a emote-role message"
                f" that I previously created.\n\nID: {msg_id} in"
                f" {channel.mention}",
            )
            continue

        entry = (
            f"`{counter}`"
            f" {old_msg.embeds[0].title if old_msg.embeds else old_msg.content}"
        )
        formatted_list.append(entry)
        counter += 1

    return formatted_list

@tasks.loop(hours=24)
async def cleandb():
	# Cleans the database by deleting rows of reaction role messages that don't exist anymore
	messages = db.fetch_all_messages()
	guilds = db.fetch_all_guilds()
	# Get the cleanup queued guilds
	cleanup_guild_ids = db.fetch_cleanup_guilds(guild_ids_only=True)

	if isinstance(messages, Exception):
	    await system_notification(
	        None,
	        "Database error when fetching messages during database"
	        f" cleaning:\n```\n{messages}\n```",
	    )
	    return

	for message in messages:
		try:
			channel_id = message[1]
			channel = await bot.fetch_channel(channel_id)

			await channel.fetch_message(message[0])

		except discord.NotFound as e:
			            # If unknown channel or unknown message
			if e.code in [10003, 10008]:
				delete = db.delete(message[0], message[3])

				if isinstance(delete, Exception):
				    await system_notification(
				        channel.guild.id,
				        "Database error when deleting messages during database"
				        f" cleaning:\n```\n{delete}\n```",
				    )
				    return

				await system_notification(
				    channel.guild.id,
				    "I deleted the database entries of a message that was removed."
				    f"\n\nID: {message} in {channel.mention}",
				)

		except discord.Forbidden:
		    # If we can't fetch the channel due to the bot not being in the guild or permissions we usually cant mention it or get the guilds id using the channels object
		    await system_notification(
		        message[3],
		        "I do not have access to a message I have created anymore. "
		        "I cannot manage the roles of users reacting to it."
		        f"\n\nID: {message[0]} in channel {message[1]}",
		    )

	if isinstance(guilds, Exception):
	    await system_notification(
	        None,
	        "Database error when fetching guilds during database"
	        f" cleaning:\n```\n{guilds}\n```",
	    )
	    return

	for guild_id in guilds:
	    try:
	        await bot.fetch_guild(guild_id)
	        if guild_id in cleanup_guild_ids:
	            db.remove_cleanup_guild(guild_id)

	    except discord.Forbidden:
	        # If unknown guild
	        if guild_id in cleanup_guild_ids:
	            continue
	        else:
	            db.add_cleanup_guild(
	                guild_id, round(datetime.datetime.utcnow().timestamp())
	            )

	cleanup_guilds = db.fetch_cleanup_guilds()

	if isinstance(cleanup_guilds, Exception):
	    await system_notification(
	        None,
	        "Database error when fetching cleanup guilds during"
	        f" cleaning:\n```\n{cleanup_guilds}\n```",
	    )
	    return

	current_timestamp = round(datetime.datetime.utcnow().timestamp())
	for guild in cleanup_guilds:
	    if int(guild[1]) - current_timestamp <= -86400:
	        # The guild has been invalid / unreachable for more than 24 hrs, try one more fetch then give up and purge the guilds database entries
	        try:
	            await bot.fetch_guild(guild[0])
	            db.remove_cleanup_guild(guild[0])
	            continue

	        except discord.Forbidden:
	            delete = db.remove_guild(guild[0])
	            delete2 = db.remove_cleanup_guild(guild[0])
	            if isinstance(delete, Exception):
	                await system_notification(
	                    None,
	                    "Database error when deleting a guilds datebase entries during"
	                    f" database cleaning:\n```\n{delete}\n```",
	                )
	                return

	            elif isinstance(delete2, Exception):
	                await system_notification(
	                    None,
	                    "Database error when deleting a guilds datebase entries during"
	                    f" database cleaning:\n```\n{delete2}\n```",
	                )
	                return
@tasks.loop(hours=6)
async def check_cleanup_queued_guilds():
    cleanup_guild_ids = db.fetch_cleanup_guilds(guild_ids_only=True)
    for guild_id in cleanup_guild_ids:
        try:
            await bot.fetch_guild(guild_id)
            db.remove_cleanup_guild(guild_id)

        except discord.Forbidden:
            continue

@bot.event
async def on_guild_remove(guild):
    db.remove_guild(guild.id)

@bot.event
async def on_raw_reaction_add(payload):
    reaction = str(payload.emoji)
    msg_id = payload.message_id
    ch_id = payload.channel_id
    user_id = payload.user_id
    guild_id = payload.guild_id
    exists = db.exists(msg_id)

    async with (await lock_manager.get_lock(user_id)):
        if isinstance(exists, Exception):
            await system_notification(
                guild_id,
                f"Database error after a user added a reaction:\n```\n{exists}\n```",
            )

        elif exists:
            # Checks that the message that was reacted to is a reaction-role message managed by the bot
            reactions = db.get_reactions(msg_id)

            if isinstance(reactions, Exception):
                await system_notification(
                    guild_id,
                    f"Database error when getting reactions:\n```\n{reactions}\n```",
                )
                return

            ch = await getchannel(ch_id)
            msg = await ch.fetch_message(msg_id)
            user = await getuser(user_id)
            if reaction not in reactions:
                # Removes reactions added to the emote-role message that are not connected to any role
                await msg.remove_reaction(reaction, user)

            else:
                # Gives role if it has permissions, else 403 error is raised
                role_id = reactions[reaction]
                server = await getguild(guild_id)
                member = server.get_member(user_id)
                role = discord.utils.get(server.roles, id=role_id)
                if user_id != bot.user.id:
                    unique = db.isunique(msg_id)
                    if unique:
                        for existing_reaction in msg.reactions:
                            if str(existing_reaction.emoji) == reaction:
                                continue
                            async for reaction_user in existing_reaction.users():
                                if reaction_user.id == user_id:
                                    await msg.remove_reaction(existing_reaction, user)
                                    # We can safely break since a user can only have one reaction at once
                                    break

                    try:
                        await member.add_roles(role)
                        notify = db.notify(guild_id)
                        if isinstance(notify, Exception):
                            await system_notification(
                                guild_id,
                                f"Database error when checking if role notifications are turned on:\n```\n{notify}\n```",
                            )
                            return

                        if notify:
                            await user.send(
                                f"You now have the following role: **{role.name}**"
                            )

                    except discord.Forbidden:
                        await system_notification(
                            guild_id,
                            "Someone tried to add a role to themselves but I do not have"
                            " permissions to add it. Ensure that I have a role that is"
                            " hierarchically higher than the role I have to assign, and"
                            " that I have the `Manage Roles` permission.",
                        )


@bot.event
async def on_raw_reaction_remove(payload):
    reaction = str(payload.emoji)
    msg_id = payload.message_id
    user_id = payload.user_id
    guild_id = payload.guild_id
    exists = db.exists(msg_id)

    if isinstance(exists, Exception):
        await system_notification(
            guild_id,
            f"Database error after a user removed a reaction:\n```\n{exists}\n```",
        )

    elif exists:
        # Checks that the message that was unreacted to is a reaction-role message managed by the bot
        reactions = db.get_reactions(msg_id)

        if isinstance(reactions, Exception):
            await system_notification(
                guild_id,
                f"Database error when getting reactions:\n```\n{reactions}\n```",
            )

        elif reaction in reactions:
            role_id = reactions[reaction]
            # Removes role if it has permissions, else 403 error is raised
            server = await getguild(guild_id)
            member = server.get_member(user_id)

            if not member:
                member = await server.fetch_member(user_id)

            role = discord.utils.get(server.roles, id=role_id)
            try:
                await member.remove_roles(role)
                notify = db.notify(guild_id)
                if isinstance(notify, Exception):
                    await system_notification(
                        guild_id,
                        f"Database error when checking if role notifications are turned on:\n```\n{notify}\n```",
                    )
                    return

                if notify:
                    await member.send(
                        f"You do not have the following role anymore: **{role.name}**"
                    )

            except discord.Forbidden:
                await system_notification(
                    guild_id,
                    "Someone tried to remove a role from themselves but I do not have"
                    " permissions to remove it. Ensure that I have a role that is"
                    " hierarchically higher than the role I have to remove, and that I"
                    " have the `Manage Roles` permission.",
                )


@bot.command(name="new", aliases=["create"])
async def new(ctx):
    if isadmin(ctx.message.author, ctx.guild.id):
        sent_initial_message = await ctx.send(
            "Welcome to the cyberon creation program. Please provide the required information once requested. If you would like to abort the creation, do not respond and the program will time out."
        )
        bot_object = {}
        cancelled = False

        def check(message):
            return message.author.id == ctx.message.author.id and message.content != ""

        if not cancelled:
            error_messages = []
            user_messages = []
            sent_reactions_message = await ctx.send(
                "Attach roles and emojis separated by one space (one combination"
                " per message). When you are done type `done`. Example:\n:smile:"
                " `@Role`"
            )
            bot_object["reactions"] = {}
            try:
                while True:
                    reactions_message = await bot.wait_for(
                        "message", timeout=120, check=check
                    )
                    user_messages.append(reactions_message)
                    if reactions_message.content.lower() != "done":
                        reaction = (reactions_message.content.split())[0]
                        try:
                            role = reactions_message.role_mentions[0].id
                        except IndexError:
                            error_messages.append(
                                (
                                    await ctx.send(
                                        "Mention a role after the reaction. Example:\n:smile:"
                                        " `@Role`"
                                    )
                                )
                            )
                            continue

                        if reaction in bot_object["reactions"]:
                            error_messages.append(
                                (
                                    await ctx.send(
                                        "You have already used that reaction for another role. Please choose another reaction"
                                    )
                                )
                            )
                            continue
                        else:
                            try:
                                await reactions_message.add_reaction(reaction)
                                bot_object["reactions"][reaction] = role
                            except discord.HTTPException:
                                error_messages.append(
                                    (
                                        await ctx.send(
                                            "You can only use reactions uploaded to servers the bot has"
                                            " access to or standard emojis."
                                        )
                                    )
                                )
                                continue
                    else:
                        break
            except asyncio.TimeoutError:
                await ctx.author.send(
                    "cyberon creation failed, you took too long to provide the requested information."
                )
                cancelled = True
            finally:
                await sent_reactions_message.delete()
                for message in error_messages + user_messages:
                    await message.delete()

        if not cancelled:
            sent_limited_message = await ctx.send(
                "Would you like to limit users to select only have one of the roles at a given time? Please react with a 🔒 to limit users or with a ♾️ to allow users to select multiple roles."
            )

            def reaction_check(payload):
            	return (payload.member.id == ctx.message.author.id
            	        and payload.message_id == sent_limited_message.id
            	        and str(payload.emoji) in ["🔒", "♾️"])

            try:
                await sent_limited_message.add_reaction("🔒")
                await sent_limited_message.add_reaction("♾️")
                limited_message_response_payload = await bot.wait_for(
                    "raw_reaction_add", timeout=120, check=reaction_check
                )

                if str(limited_message_response_payload.emoji) == "🔒":
                    bot_object["limit_to_one"] = 1
                else:
                    bot_object["limit_to_one"] = 0
            except asyncio.TimeoutError:
                await ctx.author.send(
                    "cyberon creation failed, you took too long to provide the requested information."
                )
                cancelled = True
            finally:
                await sent_limited_message.delete()

        if not cancelled:
            sent_oldmessagequestion_message = await ctx.send(
                f"Would you like to use an existing message or create one using {bot.user.mention}? Please react with a 🗨️ to use an existing message or a 🤖 to create one."
            )

            def reaction_check2(payload):
            	return (payload.member.id == ctx.message.author.id
            	        and payload.message_id == sent_oldmessagequestion_message.id
            	        and str(payload.emoji) in ["🗨️", "🤖"])

            try:
                await sent_oldmessagequestion_message.add_reaction("🗨️")
                await sent_oldmessagequestion_message.add_reaction("🤖")
                oldmessagequestion_response_payload = await bot.wait_for(
                    "raw_reaction_add", timeout=120, check=reaction_check2
                )

                if str(oldmessagequestion_response_payload.emoji) == "🗨️":
                    bot_object["old_message"] = True
                else:
                    bot_object["old_message"] = False
            except asyncio.TimeoutError:
                await ctx.author.send(
                    "cyberon creation failed, you took too long to provide the requested information."
                )
                cancelled = True
            finally:
                await sent_oldmessagequestion_message.delete()

        if not cancelled:
            error_messages = []
            user_messages = []
            if bot_object["old_message"]:
                sent_oldmessage_message = await ctx.send(
                    "Which message would you like to use? Please react with a 🔧 on the message you would like to use."
                )

                def reaction_check3(payload):
                    return (
                        payload.member.id == ctx.message.author.id
                        and payload.guild_id == sent_oldmessage_message.guild.id
                        and str(payload.emoji) == "🔧"
                    )

                try:
                    while True:
                        oldmessage_response_payload = await bot.wait_for(
                            "raw_reaction_add", timeout=120, check=reaction_check3
                        )
                        try:
                            try:
                                channel = await getchannel(
                                    oldmessage_response_payload.channel_id
                                )
                            except discord.InvalidData:
                                channel = None
                            except discord.HTTPException:
                                channel = None
                            
                            if channel is None:
                                raise discord.NotFound
                            try:
                                message = await channel.fetch_message(
                                    oldmessage_response_payload.message_id
                                )
                            except discord.HTTPException:
                                raise discord.NotFound
                            try:
                                await message.add_reaction("👌")
                                await message.remove_reaction("👌", message.guild.me)
                                await message.remove_reaction("🔧", ctx.author)
                            except discord.HTTPException:
                                raise discord.NotFound
                            if db.exists(message.id):
                                raise ValueError
                            bot_object["message"] = dict(
                                message_id=message.id,
                                channel_id=message.channel.id,
                                guild_id=message.guild.id,
                            )
                            final_message = message
                            break
                        except discord.NotFound:
                            error_messages.append(
                                (
                                    await ctx.send(
                                        "I can not access or add reactions to the requested message. Do I have sufficent permissions?"
                                    )
                                )
                            )
                        except ValueError:
                            error_messages.append(
                                (
                                    await ctx.send(
                                        f"This message already got a cyberon instance attached to it, consider running `{prefix}edit` instead."
                                    )
                                )
                            )
                except asyncio.TimeoutError:
                    await ctx.author.send(
                        "cyberon creation failed, you took too long to provide the requested information."
                    )
                    cancelled = True
                finally:
                    await sent_oldmessage_message.delete()
                    for message in error_messages:
                        await message.delete()
            else:
                sent_channel_message = await ctx.send(
                    "Mention the #channel where to send the auto-role message."
                )
                try:
                    while True:
                        channel_message = await bot.wait_for(
                            "message", timeout=120, check=check
                        )
                        if channel_message.channel_mentions:
                            bot_object[
                                "target_channel"
                            ] = channel_message.channel_mentions[0]
                            break
                        else:
                            error_messages.append(
                                (
                                    await message.channel.send(
                                        "The channel you mentioned is invalid."
                                    )
                                )
                            )
                except asyncio.TimeoutError:
                    await ctx.author.send(
                        "cyberon creation failed, you took too long to provide the requested information."
                    )
                    cancelled = True
                finally:
                    await sent_channel_message.delete()
                    for message in error_messages:
                        await message.delete()

        if not cancelled and "target_channel" in bot_object:
            error_messages = []
            selector_embed = discord.Embed(
                title="Embed_title",
                description="Embed_content"
            )

            sent_message_message = await message.channel.send(
                "What would you like the message to say?\nFormatting is:"
                " `Message // Embed_title // Embed_content`.\n\n`Embed_title`"
                " and `Embed_content` are optional. You can type `none` in any"
                " of the argument fields above (e.g. `Embed_title`) to make the"
                " bot ignore it.\n\n\nMessage",
                embed=selector_embed,
            )
            try:
                while True:
                    message_message = await bot.wait_for(
                        "message", timeout=120, check=check
                    )
                    # I would usually end up deleting message_message in the end but users usually want to be able to access the
                    # format they once used incase they want to make any minor changes
                    msg_values = message_message.content.split(" // ")
                    # This whole system could also be re-done using wait_for to make the syntax easier for the user
                    # But it would be a breaking change that would be annoying for thoose who have saved their message commands
                    # for editing.
                    selector_msg_body = (
                        msg_values[0] if msg_values[0].lower() != "none" else None
                    )
                    

                    if len(msg_values) > 1:
                        if msg_values[1].lower() != "none":
                            selector_embed.title = msg_values[1]
                        if len(msg_values) > 2 and msg_values[2].lower() != "none":
                            selector_embed.description = msg_values[2]

                    # Prevent sending an empty embed instead of removing it
                    selector_embed = (
                        selector_embed
                        if selector_embed.title or selector_embed.description
                        else None
                    )

                    if selector_msg_body or selector_embed:
                        target_channel = bot_object["target_channel"]
                        sent_final_message = None
                        try:
                            sent_final_message = await target_channel.send(
                                content=selector_msg_body, embed=selector_embed
                            )
                            bot_object["message"] = dict(
                                message_id=sent_final_message.id,
                                channel_id=sent_final_message.channel.id,
                                guild_id=sent_final_message.guild.id,
                            )
                            final_message = sent_final_message
                            break
                        except discord.Forbidden:
                            error_messages.append(
                                (
                                    await message.channel.send(
                                        "I don't have permission to send messages to"
                                        f" the channel {target_channel.mention}. Please check my permissions and try again."
                                    )
                                )
                            )
            except asyncio.TimeoutError:
                await ctx.author.send(
                    "Cyberon role creation failed, you took too long to provide the requested information."
                )
                cancelled = True
            finally:
                await sent_message_message.delete()
                for message in error_messages:
                    await message.delete()

        if not cancelled:
            # Ait we are (almost) all done, now we just need to insert that into the database and add the reactions 💪
            try:
                r = db.add_reaction_role(bot_object)
            except database.DuplicateInstance:
                await ctx.send(
                    f"The requested message already got a cyberon instance attached to it, consider running `{prefix}edit` instead."
                )
                return

            if isinstance(r, Exception):
                await system_notification(
                    ctx.message.guild.id,
                    f"Database error when creating reaction-light instance:\n```\n{r}\n```",
                )
                return
            for reaction, _ in bot_object["reactions"].items():
                await final_message.add_reaction(reaction)
            await ctx.message.add_reaction("✅")
        await sent_initial_message.delete()

        if not cancelled:
            await ctx.message.add_reaction("❌")
    else:
        await ctx.send(
            f"You do not have an admin role. You might want to use `{prefix}admin`"
            " first."
        )


@bot.command(name="edit")
async def edit_selector(ctx):
	if isadmin(ctx.message.author, ctx.guild.id):
		# Reminds user of formatting if it is wrong
		msg_values = ctx.message.content.split()
		if len(msg_values) < 2:
			await ctx.send(
			    f"**Type** `{prefix}edit #channelname` to get started. Replace"
			    " `#channelname` with the channel where the reaction-role message you"
			    " wish to edit is located."
			)
			return

		elif len(msg_values) == 2:
		    try:
		        channel_id = ctx.message.channel_mentions[0].id

		    except IndexError:
		        await ctx.send("You need to mention a channel.")
		        return

		    channel = await getchannel(channel_id)
		    all_messages = await formatted_channel_list(channel)
		    if len(all_messages) == 1:
		        await ctx.send(
		            "There is only one reaction-role message in this channel."
		            f" **Type**:\n```\n{prefix}edit #{channel.name} // 1 // New Message"
		            " // New Embed Title (Optional) // New Embed Description"
		            " (Optional)\n```\nto edit the reaction-role message. You can type"
		            " `none` in any of the argument fields above (e.g. `New Message`)"
		            " to make the bot ignore it."
		        )

		    elif len(all_messages) > 1:
		        await ctx.send(
		            f"There are **{len(all_messages)}** reaction-role messages in this"
		            f" channel. **Type**:\n```\n{prefix}edit #{channel.name} //"
		            " MESSAGE_NUMBER // New Message // New Embed Title (Optional) //"
		            " New Embed Description (Optional)\n```\nto edit the desired one."
		            " You can type `none` in any of the argument fields above (e.g."
		            " `New Message`) to make the bot ignore it. The list of the"
		            " current reaction-role messages is:\n\n" + "\n".join(all_messages)
		        )

		    else:
		        await ctx.send("There are no reaction-role messages in that channel.")

		elif len(msg_values) > 2:
			try:
				# Tries to edit the reaction-role message
				# Raises errors if the channel sent was invalid or if the bot cannot edit the message
				channel_id = ctx.message.channel_mentions[0].id
				channel = await getchannel(channel_id)
				msg_values = ctx.message.content.split(" // ")
				selector_msg_number = msg_values[1]
				all_messages = db.fetch_messages(channel_id)

				if isinstance(all_messages, Exception):
				    await system_notification(
				        ctx.message.guild.id,
				        "Database error when fetching"
				        f" messages:\n```\n{all_messages}\n```",
				    )
				    return

				if all_messages:
					message_to_edit_id = None
					counter = 1
					for msg_id in all_messages:
					    # Loop through all msg_ids and stops when the counter matches the user input
					    if str(counter) == selector_msg_number:
					        message_to_edit_id = msg_id
					        break

					    counter += 1

				else:
					await ctx.send(
					    "You selected a reaction-role message that does not exist."
					)
					return

				if message_to_edit_id:
				    old_msg = await channel.fetch_message(int(message_to_edit_id))

				else:
				    await ctx.send(
				        "Select a valid reaction-role message number (i.e. the number"
				        " to the left of the reaction-role message content in the list"
				        " above)."
				    )
				    return
				await old_msg.edit(suppress=False)
				selector_msg_new_body = (
				    msg_values[2] if msg_values[2].lower() != "none" else None
				)
				selector_embed = discord.Embed()

				if len(msg_values) > 3 and msg_values[3].lower() != "none":
				    selector_embed.title = msg_values[3]


				if len(msg_values) > 4 and msg_values[4].lower() != "none":
				    selector_embed.description = msg_values[4]


				try:
				    if selector_embed.title or selector_embed.description:
				        await old_msg.edit(
				            content=selector_msg_new_body, embed=selector_embed
				        )

				    else:
				        await old_msg.edit(content=selector_msg_new_body, embed=None)

				    await ctx.send("Message edited.")
				except discord.Forbidden:
				    await ctx.send(
				        "I can only edit messages that are created by me, please edit the message in some other way."
				    )
				    return
				except discord.HTTPException as e:
				    if e.code == 50006:
				        await ctx.send(
				            "You can't use an empty message as role-reaction message."
				        )

				    else:
				        guild_id = ctx.message.guild.id
				        await system_notification(guild_id, str(e))

			except IndexError:
			    await ctx.send("The channel you mentioned is invalid.")

			except discord.Forbidden:
			    await ctx.send("I do not have permissions to edit the message.")

	else:
		await ctx.send("You do not have an admin role.")

@bot.command(name="reaction")
async def edit_reaction(ctx):
	if isadmin(ctx.message.author, ctx.guild.id):
		msg_values = ctx.message.content.split()
		mentioned_roles = ctx.message.role_mentions
		mentioned_channels = ctx.message.channel_mentions
		if len(msg_values) < 4:
			if not mentioned_channels:
			    await ctx.send(
			        f" To get started, type:\n```\n{prefix}reaction add"
			        f" #channelname\n```or\n```\n{prefix}reaction remove"
			        " #channelname\n```"
			    )
			    return

			channel = ctx.message.channel_mentions[0]
			all_messages = await formatted_channel_list(channel)
			if len(all_messages) == 1:
				await ctx.send(
				    "There is only one reaction-role messages in this channel."
				    f" **Type**:\n```\n{prefix}reaction add #{channel.name} 1"
				    f" :reaction: @rolename\n```or\n```\n{prefix}reaction remove"
				    f" #{channel.name} 1 :reaction:\n```"
				)
			elif len(all_messages) > 1:
				await ctx.send(
				    f"There are **{len(all_messages)}** reaction-role messages in this"
				    f" channel. **Type**:\n```\n{prefix}reaction add #{channel.name}"
				    " MESSAGE_NUMBER :reaction:"
				    f" @rolename\n```or\n```\n{prefix}reaction remove"
				    f" #{channel.name} MESSAGE_NUMBER :reaction:\n```\nThe list of the"
				    " current reaction-role messages is:\n\n" + "\n".join(all_messages)
				)
			else:
				await ctx.send("There are no reaction-role messages in that channel.")
			return

		action = msg_values[1].lower()
		channel = ctx.message.channel_mentions[0]
		message_number = msg_values[3]
		reaction = msg_values[4]
		if action == "add":
		    if mentioned_roles:
		        role = mentioned_roles[0]
		    else:
		        await ctx.send("You need to mention a role to attach to the reaction.")
		        return

		all_messages = db.fetch_messages(channel.id)
		if isinstance(all_messages, Exception):
		    await system_notification(
		        ctx.message.guild.id,
		        f"Database error when fetching messages:\n```\n{all_messages}\n```",
		    )
		    return

		if all_messages:
			message_to_edit_id = None
			counter = 1
			for msg_id in all_messages:
			    # Loop through all msg_ids and stops when the counter matches the user input
			    if str(counter) == message_number:
			        message_to_edit_id = msg_id
			        break

			    counter += 1

		else:
			await ctx.send("You selected a reaction-role message that does not exist.")
			return

		if message_to_edit_id:
		    message_to_edit = await channel.fetch_message(int(message_to_edit_id))

		else:
		    await ctx.send(
		        "Select a valid reaction-role message number (i.e. the number"
		        " to the left of the reaction-role message content in the list"
		        " above)."
		    )
		    return

		if action == "add":
		    try:
		        # Check that the bot can actually use the emoji
		        await message_to_edit.add_reaction(reaction)

		    except discord.HTTPException:
		        await ctx.send(
		            "You can only use reactions uploaded to servers the bot has access"
		            " to or standard emojis."
		        )
		        return

		    react = db.add_reaction(message_to_edit.id, role.id, reaction)
		    if isinstance(react, Exception):
		        await system_notification(
		            ctx.message.guild.id,
		            "Database error when adding a reaction to a message in"
		            f" {message_to_edit.channel.mention}:\n```\n{react}\n```",
		        )
		        return

		    if not react:
		        await ctx.send(
		            "That message already has a reaction-role combination with"
		            " that reaction."
		        )
		        return

		    await ctx.send("Reaction added.")

		elif action == "remove":
		    try:
		        await message_to_edit.clear_reaction(reaction)

		    except discord.HTTPException:
		        await ctx.send("Invalid reaction.")
		        return

		    react = db.remove_reaction(message_to_edit.id, reaction)
		    if isinstance(react, Exception):
		        await system_notification(
		            ctx.message.guild.id,
		            "Database error when adding a reaction to a message in"
		            f" {message_to_edit.channel.mention}:\n```\n{react}\n```",
		        )
		        return

		    await ctx.send("Reaction removed.")

	else:
		await ctx.send("You do not have an admin role.")

@bot.command(name="notify")
async def toggle_notify(ctx):
    if isadmin(ctx.message.author, ctx.guild.id):
        notify = db.toggle_notify(ctx.guild.id)
        if notify:
            await ctx.send(
                "Notifications have been set to **ON** for this server.\n"
                "Use this command again to turn them off."
            )
        else:
            await ctx.send(
                "Notifications have been set to **OFF** for this server.\n"
                "Use this command again to turn them on."
            )

@bot.command(name="help")
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


@bot.command(pass_context=True, name="admin")
@commands.has_permissions(administrator=True)
async def add_admin(ctx, role: discord.Role):
    # Adds an admin role ID to the database
    add = db.add_admin(role.id, ctx.guild.id)

    if isinstance(add, Exception):
        await system_notification(
            ctx.message.guild.id,
            f"Database error when adding a new admin:\n```\n{add}\n```",
        )
        return

    await ctx.send("Added the role to my admin list.")


@add_admin.error
async def add_admin_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("Please mention a valid @Role or role ID.")


@bot.command(name="rm-admin")
@commands.has_permissions(administrator=True)
async def remove_admin(ctx, role: discord.Role):
    # Removes an admin role ID from the database
    remove = db.remove_admin(role.id, ctx.guild.id)

    if isinstance(remove, Exception):
        await system_notification(
            ctx.message.guild.id,
            f"Database error when removing an admin:\n```\n{remove}\n```",
        )
        return

    await ctx.send("Removed the role from my admin list.")


@remove_admin.error
async def remove_admin_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("Please mention a valid @Role or role ID.")


@bot.command(name="adminlist")
@commands.has_permissions(administrator=True)
async def list_admin(ctx):
	# Lists all admin IDs in the database, mentioning them if possible
	admin_ids = db.get_admins(ctx.guild.id)

	if isinstance(admin_ids, Exception):
	    await system_notification(
	        ctx.message.guild.id,
	        f"Database error when fetching admins:\n```\n{admin_ids}\n```",
	    )
	    return

	adminrole_objects = [
	    discord.utils.get(ctx.guild.roles, id=admin_id).mention
	    for admin_id in admin_ids
	]
	if adminrole_objects:
	    await ctx.send(
	        "The bot admins on this server are:\n- " + "\n- ".join(adminrole_objects)
	    )
	else:
	    await ctx.send("There are no bot admins registered in this server.")

# Run the bot with the token
bot.run(os.getenv('TOKEN'))
