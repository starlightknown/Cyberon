# Run Your Version of Cyberon

The next step is to invite your instance of Cyberon to your server. You can use the Discord Developer portal to generate an invitation link, or you can use the Client ID from your Cyberon's application page to create a link yourself. If you wish to manually create the link, the format is:

`https://discord.com/oauth2/authorize?client_id=<CLIENT_ID_HERE>&scope=bot`

Regardless of which method you choose, the link will open a new window allowing you to choose which server you'd like to add Cyberon to.

Once you have added it to your server, switch back to your terminal and run the command `python3 bot.py`. If you have set the `mongodbclient` and `bot_token` in your environment appropriately,you should see the text +Cyberon is online! in your terminal, indicating it is online! Now you can try some of the commands to see if she is functioning correctly.

## Host a Live Version of Cyberon

By now you should have a successfully running local instance of Cyberon. Keeping this alive means you cannot shut down your computer. As an alternative, you might want to use a hosting service to run your live instance. We hosted this bot on heroku.

If you would like to add Cyberon to your server, you are welcome to [invite Cyberon to your server](https://discordapp.com/oauth2/authorize?&client_id=819568634673889341&scope=bot&permissions=8).
