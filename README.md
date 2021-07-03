# Cyberon - a cool discord bot for hackathon servers

<div align="center">
    
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/language-Python-blue.svg?v=103"></a>
<a href="https://github.com/Rapptz/discord.py/releases/tag/v1.5.0"><img src="https://img.shields.io/badge/discord.py-v1.6.0-7289da.svg?color=brightgreen" alt="discord.py version"></a>

<a href="https://github.com/starlightknown/Cyberon"><img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103"></a>
<a href="https://github.com/starlightknown/Cyberon"><img src="https://img.shields.io/badge/Built%20by-developers%20%3C%2F%3E-0059b3"></a>
<a href="https://github.com/starlightknown/Cyberon"><img src="https://img.shields.io/static/v1.svg?label=Contributions&message=Welcome&color=yellow"></a>
<a href="https://github.com/starlightknown/"><img src="https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg?v=103"></a>
<a href="https://github.com/starlightknown/Cyberon/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?v=103"></a>

<a href="https://github.com/starlightknown/Cyberon/graphs/contributors"><img src="https://img.shields.io/github/contributors/starlightknown/Cyberon?color=brightgreen"></a>
<a href="https://github.com/starlightknown/Cyberon/stargazers"><img src="https://img.shields.io/github/stars/starlightknown/Cyberon?color=0059b3"></a>
<a href="https://github.com/starlightknown/Cyberon/network/members"><img src="https://img.shields.io/github/forks/starlightknown/Cyberon?color=yellow"></a>
<a href="https://github.com/starlightknown/Cyberon/issues"><img src="https://img.shields.io/github/issues/starlightknown/Cyberon?color=0059b3"></a>
<a href="https://github.com/starlightknown/Cyberon/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed-raw/starlightknown/Cyberon?color=yellow"></a>
<a href="https://github.com/starlightknown/Cyberon/pulls"><img src="https://img.shields.io/github/issues-pr/starlightknown/Cyberon?color=brightgreen"></a>
<a href="https://github.com/starlightknown/Cyberon/pulls?q=is%3Apr+is%3Aclosed"><img src="https://img.shields.io/github/issues-pr-closed-raw/starlightknown/Cyberon?color=0059b3"></a> 

</div>

<img src="https://raw.githubusercontent.com/starlightknown/Cyberon/main/images/call_me_cyb.gif">

# Overview:

Cyberon is a customisable, friendly, fun discord bot which you can add to our servers and customise it according to your needs.
Cyberon is a bot with mission. This bot is for helping people who are new to hackathons and can't find good ones or are overwhelmed with the number of sites 
they need to search for hackatons. (still in development)

[Installation](#installation) is easy, and you do **NOT** need to know anything about coding!
**The default set of modules includes and is not limited to:**

- Moderation features (kick/ban/softban, mod-log, multiban, warn, role assignment)
- Fun commands 
- Utility commands (hackathon alerts, general commands)
- Server configs commands and permissions
- Support commands

# Installation

```
git clone https://github.com/starlightknown/cyberon
cd cyberon
sudo pip3 install -r requirements.txt
```
or 
```
sudo python3 -m pip install -r requirements.txt
```  
NOTE: Make a .env file and put them in the the same folder as the `bot.py` file, i.e. in the root directory 
and add your tokens as `BOT_TOKEN`, `DATABASE_CLIENT_URL` and `NASA_API_KEY` respectively.  

Run `python3 bot.py`

There are a few steps you will need in order to set up a local instance of Cyberon. If you are not comfortable with doing this, you can [join our server](https://discord.gg/sTYguvHP8t) 

You can use the Discord Developer portal to generate an invitation link, or you can use the Client ID from your Cyberon's application page to create a link yourself. If you wish to manually create the link, the format is:

`https://discord.com/oauth2/authorize?client_id=<CLIENT_ID_HERE>&scope=bot`

Visit the link and choose the server you would like to add the bot. All done!

# Docs

- [Project board](https://github.com/starlightknown/Cyberon/projects/1) of `to do`, `in progress`, `done`

Full docs deployed to https://starlightknown.github.io/Cyberon/#/ and available in the repo at [docs/index.md](docs/index.md)

# Configure your Server

You need to configure Cyberon's settings using the cyb!config command. You can see all config commands using `cyb!help config` or `cyb!config` and type out the channels for questions asked by Cyberon.

<img src="https://raw.githubusercontent.com/starlightknown/Cyberon/main/images/ezgif.com-gif-maker.gif">

# Problem

- too many hackathon websites to seacrh for a beginner
- no alerts when a new hackathon is added
- low moderation hackathon servers gets spammed

# Solution

- Get all hackathon updates in the server you are in
- One command for one website you want to search
- set a warn threshold, after it's crossed the user gets banned

# Requirements
- discord.py
- PyNaCl==1.3.0
- dnspython
- async-timeout
- pyfiglet
- wikipedia
- howdoi
- pymongo
- psutil

# Invite bot to your server :robot: ❤️
[Invite bot to your server](https://discordapp.com/oauth2/authorize?&client_id=819568634673889341&scope=bot&permissions=8)

**Bot is constantly updated, If you find any bugs use `cyb!bugs <describe bug in 20 words>` this will send the report to our support channel or raise an issue on this repository with proper description of the problem/issue you found and we will fix it. Read the CONTRIBUTING.md file before contributing to get a clear understanding of the workflow**

**You can join our support channel on discord to test it out [here](https://discord.gg/tgaRPHaVKX)**

# License

Cybeon is licensed under MIT license


