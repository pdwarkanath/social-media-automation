import tweepy
import pandas as pd
import json
import sys
import time
import random


tweets = pd.read_csv(sys.argv[1])


# These lengths are constant across all of twitter and used to extract username and status ID from a link to a tweet

stem = len('https://twitter.com/')
end = len('/status/1133040847853723650')
status_length = len('1133040847853723650')

tweets['username'] = tweets.tweet.str.slice(start = stem, stop = -end)
tweets['status_id'] = tweets.tweet.str.slice(start = -status_length)

# Access Twitter API using access tokens and keys saved in the tweetapi.json file

with open('tweetapi.json') as f:
    tweetapi = json.load(f)

consumer_key = tweetapi['consumer_key']
consumer_secret = tweetapi['consumer_secret']
access_key = tweetapi['access_key']
access_secret = tweetapi['access_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret) 
api = tweepy.API(auth)

# Post tweets as replies to tweets

def post_tweets(tweets):
    num_tweets = tweets.shape[0]
    for i in range(num_tweets):
        meme = tweets.meme[i]
        username = tweets.username[i]
        status_id = tweets.status_id[i]
        reply_txt = f'@{username} Hey! This tweet is featured here: https://weekinmemes.com/memes/{meme}/ '
        api.update_status(reply_txt, in_reply_to_status_id = status_id)
        print(f'tweet posted to {username}')
        if i % 10 == 0:
        	time.sleep(random.random() + 1)


post_tweets(tweets)

