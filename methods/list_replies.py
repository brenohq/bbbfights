import tweepy
import logging
import time
import json

user_name = "@bbbfights"

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def list_replies(api, tweet_id):
    replies = tweepy.Cursor(api.search, q='to:{}'.format(user_name),
                            since_id=tweet_id, tweet_mode='extended').items()

    while True:
        try:
            reply = replies.next()

            if not hasattr(reply, 'in_reply_to_status_id_str'):
                continue
            if reply.in_reply_to_status_id == tweet_id:
                logging.info(
                    f'Reply of tweet: {reply.full_text} with {reply.favorite_count} likes')

        except tweepy.RateLimitError as e:
            logging.error("Twitter api rate limit reached")
            logging.error(e)
            time.sleep(60)
            continue

        except tweepy.TweepError as e:
            logging.error(f'Tweepy error occured: {e}')
            break

        except StopIteration:
            break

        except Exception as e:
            logging.error("Failed while fetching replies {}".format(e))
            break
