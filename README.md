# Cyberon - a cool discord bot for hackathon servers
<a href="https://www.python.org/"><img src="http://ForTheBadge.com/images/badges/made-with-python.svg" alt="made with Python"></a>
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
<a href="https://github.com/Rapptz/discord.py/releases/tag/v1.5.0"><img src="https://img.shields.io/badge/discord.py-v1.6.0-7289da.svg?style=flat-square" alt="discord.py version"></a>
<a href="http://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
  </a>

<img src="https://raw.githubusercontent.com/starlightknown/Cyberon/main/images/call_me_cyb.gif">

# Overview:

Cyberon is a customisable, friendly, fun discord bot which you can add to our servers and customise it according to your needs.
Cyberon is a bot with mission. This bot is for helping people who are new to hackathons and can't find good ones or are overwhelmed with the number of sites 
they need to search for hackatons. (still in development)

[Installation](#installation) is easy, and you do **NOT** need to know anything about coding! Aside
from installing and updating, every part of the bot can be controlled from within Discord.

**The default set of modules includes and is not limited to:**

- Moderation features (kick/ban/softban, mod-log, multiban, warn, role assignment)
- Fun commands
- Utility commands (hackathons/general commands)
- Server configs commands and permissions
- Support commands

# Installation

```
git clone https://github.com/starlightknown/cyberon
sudo pip3 install -r requirements.txt
```
or 
```
sudo python3 -m pip install -r requirements.txt
```  
NOTE: Make a .env file and put them in the the same folder as the `bot.py` file, i.e. in the root directory 
and add your tokens as `BOT_TOKEN`, `DATABASE_CLIENT_URL` and `NASA_API_KEY` respectively.  

# Create a Local Instance

There are a few steps you will need in order to set up a local instance of Cyberon. You will need some knowledge of Python, pip and git. If you are not comfortable with doing this, you can [join our server](https://discord.gg/sTYguvHP8t) 

## Clone the GitHub Repository

Navigate to our [GitHub repository](https://github.com/starlightknown/Cyberon) and either fork the repository into your own account or download the files to your computer.

## Install the Necessary Software

Using your preferred development environment (if you do not have one, we recommend either Visual Studio Code (VSCode) or Atom), load the directory containing your copy of Cyberon's files.

Cyberon uses Python 3.8.1 or higher. Open the terminal - you will now need to install the requirements using pip. Enter the following commands into the terminal to perform the installations:

`sudo python3 -m pip install -r requirements.txt`  OR `sudo pip3 install -r requirements.txt`

All done! You are now ready to run the code locally - the start command is `cd Cyberon/` - `python3 bot.py`. 
You can use the Discord Developer portal to generate an invitation link, or you can use the Client ID from your Cyberon's application page to create a link yourself. If you wish to manually create the link, the format is:

`https://discord.com/oauth2/authorize?client_id=<CLIENT_ID_HERE>&scope=bot`


# Configure your Server

You need to configure Cyberon's settings using the cyb!config command. You can see all config commands using `cyb!help config` or `cyb!config` and type out the channels for questions asked by Cyberon.

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

**Invite bot to your server**
[Invite bot to your server](https://discordapp.com/oauth2/authorize?&client_id=819568634673889341&scope=bot&permissions=8)

**Bot is constantly updated, If you find any bugs use `cyb!bugs <describe bug in 20 words>` this will send the report to our support channel or raise an issue on this repository with proper description of the problem/issue you found and we will fix it. Read the CONTRIBUTING.md file before contributing to get a clear understanding of the workflow**

**You can join our support channel on discord to test it out [here](https://discord.gg/tgaRPHaVKX)**

# License

Cybeon is licensed under MIT license


