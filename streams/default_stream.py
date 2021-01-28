import tweepy
import time


class TwitterStreamListener(tweepy.StreamListener):

    def __init__(self, api):
        self.api = api

    def on_limit(self, status):
        print(f"called on_limit with status: {status}")
        time.sleep(1 * 60)

    def on_status(self, status):
        self.api.create_friendship(status.user.screen_name)
        self.api.create_favorite(status.id)

    def on_error(self, status_code):
        if status_code == 403:
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False
        else:
            print(f"Unhandled error: {status_code}")
