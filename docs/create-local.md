# Create a Local Instance

There are a few steps you will need in order to set up a local instance of Cyberon. You will need some knowledge of Python, pip and git. If you are not comfortable with doing this, you can [join our server](https://discord.gg/sTYguvHP8t) 

## Clone the GitHub Repository

Before doing anything else, you have to make sure you have a GitHub Account. If you do not have one, we recommend signing up for free here.

Once you have signed in to GitHub, navigate to our [GitHub repository](https://github.com/starlightknown/Cyberon) and either fork the repository into your own account or download the files to your computer.

## Install the Necessary Software

Using your preferred development environment (if you do not have one, we recommend either Visual Studio Code (VSCode) or Atom), load the directory containing your copy of Cyberon's files.

Cyberon uses Python 3.8.1 or higher. Open the terminal - you will now need to install the requirements using pip. Enter the following commands into the terminal to perform the installations:

`sudo python3 -m pip install -r requirements.txt`  OR `sudo pip3 install -r requirements.txt`

All done! You are now ready to run the code locally - the start command is `cd Cyberon/` - `python3 bot.py`. To connect the code to your Discord Bot application, continue reading.
