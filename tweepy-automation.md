# Automating using Tweepy

This post for example https://weekinmemes.com/memes/sarfaraz-yawn/

Since I already have links to tweets in a CSV file, I just need to use a python script from the command line interface to authenticate to my Twitter account and reply to all. 

In a minute or two, all replies are sent to the right tweets with links to pages where they are featured.

## Python script

The script I use:

```
import tweepy
import pandas as pd
import json
import sys
import time
import random
```

Load the Twitter links from the CSV file and extract usernames and Tweet IDs from them. These are all saved in a table (pandas DataFrame) called `tweets`

```

tweets = pd.read_csv(sys.argv[1])

# These lengths are constant across all of twitter and used to extract username and status ID from a link to a tweet

stem = len('https://twitter.com/')
end = len('/status/1133040847853723650')
status_length = len('1133040847853723650')

tweets['username'] = tweets.tweet.str.slice(start = stem, stop = -end)
tweets['status_id'] = tweets.tweet.str.slice(start = -status_length)
```

Create the template tweet that will be sent as reply

```
reply_txt = f'@{username} Hey! This tweet is featured here: https://weekinmemes.com/memes/{meme}/ '
```

Tweepy is a Python library that is a wrapper to the Twitter API. So I can use Python commands to access Twitter API end points.

First I authenticate using the API keys I received from Twitter while creating an app *

I have saved the credentials in a file named "tweetapi.json"

```
with open('tweetapi.json') as f:
    tweetapi = json.load(f)

consumer_key = tweetapi['consumer_key']
consumer_secret = tweetapi['consumer_secret']
access_key = tweetapi['access_key']
access_secret = tweetapi['access_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret) 
api = tweepy.API(auth)
```

Then I use the Tweepy command to post status in reply to tweet ID extracted in the first step. Looping over all tweets, the script automatically sends replies while I wait for it to run.
```
def post_tweets(tweets):
    num_tweets = tweets.shape[0]
    for i in range(num_tweets):
        meme = tweets.meme[i]
        username = tweets.username[i]
        status_id = tweets.status_id[i]
        reply_txt = f'@{username} Hey! This tweet is featured here: https://weekinmemes.com/memes/{meme}/ '
        api.update_status(reply_txt, in_reply_to_status_id = status_id)
        print(f'tweet posted to {username}')
```

If you tweet too often in a short period of time, Twitter might think you're a bot. Which this is but to avoid suspicion of bot-like behavior I add a random 'sleep' timer. So the script sleeps for a random duration between 1-2 seconds after every tweet. Then resumes tweeting.
```
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

```

That's it. This code is saved in a file named `reply_to_featured.py`

Now every time I write a new post, I keep all tweets in a CSV file and run the Python script from command line. If the tweets are saved in `FeaturedTweets20190718.csv`, the command is: 

```
~$ python reply_to_featured.py FeaturedTweets20190718.csv

```


* You will need to create an app on Twitter to receive API credentials. Here is a good tutorial for that: https://docs.inboundnow.com/guide/create-twitter-application/