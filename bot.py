import discord
import os
import random
import praw
import tweepy
import time
import urllib.parse
from discord.ext import commands
# Place your Twitter API keys here
#ACCESS_TOKEN = 'This one has a hyphen in the middle'
#ACCESS_TOKEN_SECRET = 'This one is as long as the last one I think'
#CONSUMER_KEY = 'This one is the shortest I believe'
#CONSUMER_SECRET = 'this one is as long as the AkZES_TOKEN_SECRETO'

#Reddit keys
#CLIENT_ID = 'some letters'
#CLIENT_SECRET = 'some capital letters'

#Discord info
#DISCORD_TOKEN = 'this one has a couple of dots in the middle'
#DISCORD_GUILD_ID = a long number
#DISCORD_CHANNEL_ID = another long number
#Reddit you want to watch
#SUBREDDIT = 'The subreddit you want to host'

#Maximo tamaño de los ficheros
MAX_SIZE = 3070000

#Reddit shorter url
REDDIT_URL = 'https://redd.it/'

#Pause between tweets
TIME_TO_SLEEP = 1200

reddit = praw.Reddit(
                        user_agent='reddit Twitter tool monitoring ',
                        client_id=os.environ['REDDIT_CLIENT_ID'],
                        client_secret=os.environ['REDDIT_CLIENT_SECRET'])

#It is needed to allow the intents here and in the bot console at https://discord.com/developers/applications/
intents = discord.Intents.default()
intents.members = True
client = discord.Client(guild_subscriptions = True, chunk_guilds_at_startup = True, intents = intents)

@client.event
async def on_ready():
    print('Bot is ready')
    
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    print(client.guilds)
    guild = client.guilds[0]
    #First we are going to tell the admin that the bot is running so he does not need to check the channel everyday
    
    print(guild.channels) #In case you want to see the guild channels. Use this to see the channels ids 
    #You can get the channels easily as Discord storages them in guild.channels in order of creation. In my case this are
    #the only ones I am using.
    admin_channel = guild.get_channel(guild.channels[4].id)
    admin = client.get_user(guild.owner_id)
    await admin_channel.send(admin.mention + ': running...')

    #Now we can continue
    
    channel = guild.get_channel(guild.channels[3].id)
    print('getting into the while...')
    while True:
      texts = []
      
      messages = await channel.history(limit = None).flatten()

      for message in messages:
          texts.append(message.content)

      
      submissions = search_for_memes(texts)
      
      for submission in submissions:
          if submission.id in texts:
              print("submission: " + submission.id + " has already been posted")
              submissions.remove(submission)
          else:
              print('Numero de mensajes en el canal: ' + str(len(await channel.history(limit = None).flatten())))
              urllib.request.urlretrieve(submission.url, submission.id + submission.url[-4:])
              if os.path.getsize(submission.id + submission.url[-4:]) < MAX_SIZE:
                print('posting file ' + submission.id + submission.url[-4:])
                api.update_with_media(filename = os.path.abspath(submission.id + submission.url[-4:]), status = REDDIT_URL+submission.id)
                await channel.send(submission.id)
                print(os.listdir(os.getcwd()))
                print("Tweet tweeted. HURRAY")
                
                os.remove(submission.id + submission.url[-4:])
                print('file removed successfully')
                time.sleep(1200)
              else: 
                print('file ' + submission.url + ' is too big')
              


def search_for_memes(texts):
    subreddit = reddit.subreddit(os.environ['SUBREDDIT_NAME'])
    submissions = []
    print("searching for memes...")
    for submission in subreddit.hot(limit = 100):
        if '.png'in submission.url or '.jpg' in submission.url:            
            submissions.append(submission)

    #print("devolviendo posts...")
    return submissions

client.run(os.environ['DISCORD_TOKEN'])
