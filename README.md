# The SAD TRAP  
The SAD TRAP (or Super Awesome Discord-Twitter-Reddit Automated Posterbot) takes pictures from a subreddit and post them on Twitter.

The main problem I encountered when written this app is that most of the free hosting services do not allow to save files. And that is when Discord joins the party.

Thanks to the Discord API you can save the reddit images id and post them to a discord chat. Now the bot will remember if it has posted the image before or not.

In the first version (https://github.com/JacoboGuijar/discordmemesbot) when Heroku restarted itself (every 24 hours or so) you had to manually insert a command in the discord chat to restart the bot.
Now with this version (hopefully the last one) the bot starts automatically when the heroku app restarts and sends a message mentioning the user to remind him that the bot is running properly.

Just to wrap things up: if you want to use it fill all the tokens in bot.py and upload it to Heroku. If you want to comment anything I will be more than willingly to hear your opinion. I know that this is not some ground breaking invention but I wanted to write something like this for a while and I am proud of the results. 
