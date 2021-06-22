# Manual Commands

These commands are run manually by sending the prefix and the associated command keyword (listed below) and arguments. Use `cyb!help` to get a short list of available commands.

## Fun Commands

These commands are just playful or fun commands.

- 8ball
Uses AI to give you the best answers to your questions
Usage: `cyb!8ball <question>`

- meme
Sends you a beautifully crafted meme
Usage: `cyb!meme`

- cat | kitty
Gets you a cat picture
Usage: `cyb!cat`

- fact | facts
Gets you a random animal fact if it exists
Usage: `cyb!fact <animal>`

- asciify
ASCIIfies your message
Usage: `cyb!asciify <message>`

- apod
Gets you an Astronomy Picture Of the Day
Usage: `cyb!apod`

- joke
Random joke has been delivered!
Usage: `cyb!joke`

- pjoke
Gets you a programming related joke
Usage: `cyb!pjoke`

- quotes
A random quote
Usage: `cyb!quote`

- at
Aesthetifies your message
Usage: `cyb!at <text>`

- hug
gives a hug with intensity 0,6,9,10
Usage: `cyb!hug <member> <intensity>`

## General Commands

These are Cyberon's general purpose commands.

- avatar | av
Shows the avatar of the user mentioned
Usage: `cyb!avatar <member_name | member_tag | member_id>`
If nothing is provided then it shows your avatar

- userinfo | ui
Gives the info of the mentioned user
Usage: `cyb!userinfo <member_name | member_tag | member_id>`

- serverinfo | si
Gives the info of the server
Usage: `cyb!serverinfo`, No arguments required

- servercount | sc
Shows you how many servers the bot is in and total number of members in those servers combined
Usage: `cyb!sc`, No arguments required

- wikipedia | wiki | ask | whatis
Gets you information from the wiki
Usage: `cyb!wiki <query>`
Query is necessary

- howdoi
Information from stackoverflow
Usage: `cyb!howdoi <query>`
Query is necessary

- cipher | morse
Converts your message to morse code
Usage: `cyb!cypher <message>`

- base64
Encodes your message to base64
Usage: `cyb!base64 "<message>" <iteration>`
Message must be in quotes

- dbase64
Decodes your base64 encoded message
Usage: `cyb!dbase64 "<message>"`
Message must be in quotes

- qrcode
Converts a text to qr code
Usage: `cyb!qrcode <message>`

- qrdecode
Decodes the qr code link provided
Usage: `cyb!qrdecode <url link>`

- hack-show
Gives you a list of websites for hackathons
Usage: `cyb!hack-show`

- botstats
Shows the bot's statistics
Usage: `cyb!botstats`

- hack club
Shows the upcoming hackathons from hack the club right in your servers
Usage: `cyb!hackclub`

## Moderation Commands

These are Cyberons's moderation commands.

- kick
Kicks the member out of the server
Usage: `cyb!kick <member_name | member_id | member_tag> <reason>`, reason is not neccessary

- multikick
Kicks multiple users out of the guild
Usage: `cyb!multikick <member_name | member_id | member_tag>`, reason is not needed

- ban | hardban
Bans the user from the server, purging the messages
Usage: `cyb!ban <member_name | member_id | member_tag> <reason>`, reason is not necessary

- softban
Bans the user from the server, without removing the messages
Usage: `cyb!softban <member_name | member_id | member_tag> <reason>`, reason is not necessary

- multiban
Bans multiple users out of the guild
Usage: `cyb!multiban <member_name | member_id | member_tag>`, reason is not needed

- unban
Unbans the user, you need to know the member's name
Usage: `cyb!unban <member_name#discriminator>`

- warn
Warns the user
Usage: `cyb!warn <member_name | member_id | member_tag> <infraction>`

- warns | warnings
Displays the infractions of the user mentioned
Usage: `cyb!warns <member_name | member_id | member_tag>`

- clearwarns | clearwarn
Clears all the infractions of the user
Usage: `cyb!clearwarns <member_name | member_id | member_tag>`

- mute
Mutes the user
Usage: `cyb!mute <member_name | member_id | member_tag> <reason>`, reason is not necessary

- unmute
Unmutes the user
Usage: `cyb!unmute <member_name | member_id | member_tag>`

- clear | remove | purge
Clears messages from the channel where it is used
Usage: `cyb!clear <n> where n is the number of messages to be purged`

- addrole
Adds role to member
Usage: `cyb!addrole <member_name | member_id | member_tag> <role_name>`

- removerole | purgerole
Removes role from mentioned member
Usage: `cyb!removerole <member_name | member_id | member_tag> <role_name>`

## Support Commands

These commands are related to Cyberon's support information.

- bug | bugs
Found any bugs? Use this command to report the bugs
Usage: `cyb!bugs "<message>"`

Message must be greater than 20 charecters.
You can also direct message the bot instead of invoking the command

- invite
Invite me to your server! :grin:
Usage: `cyb!invite`

- source | sourcecode
Want to know what was I written in? I'll send you a github link :wink:
Usage: `cyb!source`
No argument required

- supportserver | ss
Link to the support server
Usage: `cyb!ss`