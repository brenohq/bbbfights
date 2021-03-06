import os
import json
import tweepy
import re
from dotenv import load_dotenv

from streams.default_stream import TwitterStreamListener
from methods.list_replies import list_replies

load_dotenv()

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_SECRET')

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
# api.update_status(status='Updating using OAuth authentication via Tweepy!')

# print(json.dumps())


# for tweet in api.statuses_lookup([1353867045532807168]):
#     print(json.dumps(tweet._json))

# list_replies(api, 1353867045532807168)

poll_regex = re.compile(r'BBB Fight \d{2,}')

for tweet in api.user_timeline("@bbbfights", count=10):
    if poll_regex.match(tweet.text):
        most_recent_poll_replies = list_replies(api, tweet.id)
        print(
            f"\nEncontradas {len(most_recent_poll_replies)} replies válidas para a apuração da última enquete.\n")


streamListener = TwitterStreamListener(api)
myStream = tweepy.Stream(auth=api.auth, listener=streamListener)

myStream.filter(track=['BBBFights'], is_async=True)
