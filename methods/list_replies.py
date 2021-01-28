import tweepy
import logging
import time
import json
import ipdb

user_name = "@bbbfights"

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def list_replies(api, tweet_id):

    replies = []

    for reply in tweepy.Cursor(api.search, q=f'to:{user_name}', since_id=tweet_id, tweet_mode='extended').items():
        try:
            if not hasattr(reply, 'in_reply_to_status_id_str'):
                continue
            if reply.in_reply_to_status_id == tweet_id:
                replies.append(reply)
                logging.info(f'Reply: {reply.full_text} with {reply.favorite_count} likes.')

        except tweepy.RateLimitError as e:
            logging.error("Twitter api rate limit reached.")
            logging.error(e)
            time.sleep(60)
            continue

        except tweepy.TweepError as e:
            logging.error(f'Tweepy error occured: {e}')
            break

        except StopIteration:
            break

        except Exception as e:
            logging.error("Failed while fetching replies.")
            logging.error(e)
            break

    return replies
