# Creating Your Bot Application and Connecting it to Your Instance

Once your environment is set up, you need to connect the code to a Discord Bot application. If you have not created a Discord Bot application, you will need to follow these steps:

- Log in to the [Discord Developer site](https://discord.com/developers)
- Create a new application by clicking on the "New Application" button.
- On the left, select "Bot", then create a new bot.

## Link Your Bot Application to Cyberon's Code

Now that you have a bot application, you'll need to create a file called .env. You can either create the file manually. This file will contain the following variables:

- token.0 - Contains the bot token.
- NASA_API_KEY.0 - For the Nasa Api key, the apod command requires it.
- mongodbclient.0 - A file that contains the url to connect to your MongoDB cluster.

NOTE: The files are CASE SENSITIVE, please make sure the files are named exactly as given above and put them in the same folder as the bot.py file, i.e. in the Cyberon/ deirectory. You can also replace the token.0, mongodbclient.0 and NASA_API_KEY.0 with environment variables, but as BOT_TOKEN, DATABASE_CLIENT_URL and NASA_API_KEY respectively.

- `BOT_TOKEN` (REQUIRED) - The value of this variable will be your Token from the Discord developer page. It is VERY important that you keep this token a secret - do not upload it to GitHub or share it publicly, as this will allow anyone to access your Discord Bot application.
- `DATABASE_CLIENT_URL` (REQUIRED) - The value of this variable will be your MongoDB authentication URI. Like the token, this needs to be kept secret to prevent unauthorised access to and modification of your database.
- `NASA_API_KEY` (OPTIONAL) - This is the API key for the NASA API. If this is not provided then `cyb!apod` command will give you an error
