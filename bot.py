import discord
import os
import random
import praw
import tweepy
import asyncio
import urllib.parse
from discord.ext import commands

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

#Start de reddit client
reddit = praw.Reddit(
                        user_agent='reddit Twitter tool monitoring ',
                        client_id=os.environ['REDDIT_CLIENT_ID'],
                        client_secret=os.environ['REDDIT_CLIENT_SECRET'])

#Define Intents and create the client object they will be used many times
intents = discord.Intents.default()
intents.members = True
cliente = discord.Client(guild_subscriptions = True, chunk_guilds_at_startup = True, intents = intents)

async def memeitor(client):
    print('Start...')

    #Start Twitter client
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)

    client.run(os.environ['DISCORD_TOKEN'])
    #Getting Guild Channel and Admin
    print('Getting Guild Channel and Admin...')
    guild = client.get_guild(os.environ['DISCORD_GUILD'])
    print(guild)
    channel = guild.get_channel(os.environ['DISCORD_CHANNEL_ID'])
    print('getting guild and channel closed succesfully')

    #Getting messages
    print('getting messages...')
    messages = await channel.history(limit = None).flatten()
    texts = get_messages(messages)
    client.close()
    print('getting messages closed succesfully')

    #Get the subreddit and see if the post has already been posted
    print('searching for submissions...')
    submissions = search_for_memes(texts)
    for submission in submissions:
        #If already published pass
        if submissions.id in texts:
            print('submission: ' + submission.id + ' has already been posted')
            submissions.remove(submission)
        else:
            #Get the image
            print('Numero de mensajes en el canal: ' + str(len(await channel.history(limit = None).flatten())))
            urllib.request.urlretrieve(submission.url, submission.id + submission.url[-4:])

            #If the image is small it is posted
            if os.path.getsize(submission.id + submission.url[-4:]) < MAX_SIZE:
                print('posting file: ' + submission.id + submission.url[-4:])

                #Posting on twitter
                api.update_with_media(filename = os.path.abspath(submission.id + submission.url[-4:]), status = REDDIT_URL + submission.id)
                
                #Posting on Discord
                client.run(os.environ['DISCORD_TOKEN'])
                await channel.send(submission.id)
                client.close()
                print('tweet tweeted: HURRAY!')

                #Remove the file
                os.remove(submission.id + submission.url[-4:])
                print('file removed successfully')
                
                #Sleep for TIME_TO_SLEEP time and you avoid Twitter and reddit from getting mad
                await asyncio.sleep(TIME_TO_SLEEP)
            else:
                print('file ' + submission.id + submission.url[-4:] + ' is too big')




async def get_messages(messages):
    texts = []
    for message in messages:
        texts.append(message.content)
    
    return texts

def search_for_memes(texts):
    subreddit = reddit.subreddit(os.environ['SUBREDDIT_NAME'])
    submissions = []
    print("searching for memes...")
    for submission in subreddit.hot(limit = 50):
        if '.png'in submission.url or '.jpg' in submission.url:            
            submissions.append(submission)

    #print("devolviendo posts...")
    return submissions

while True:
    await memeitor(cliente)
