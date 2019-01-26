# Original file miguelmalvarez: https://github.com/miguelmalvarez/downloadTwitterPictures
# Modified by @sergiers3


import tweepy
import os
from tweepy import OAuthHandler
import json
import wget


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


def init_tweepy():
    # Status() is the data model for a tweet
    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse
    # User() is the data model for a user profil
    tweepy.models.User.first_parse = tweepy.models.User.parse
    tweepy.models.User.parse = parse


def download_images(api, username, retweets, replies, num_tweets, output_folder):
    tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    downloaded = 0
    print("Downloading.",end='')
    while (len(tweets) != 0) and (downloaded < 99):
        last_id = tweets[-1].id

        for status in tweets:
            media = status.entities.get('media', [])
            if (len(media) > 0 and downloaded < num_tweets):
                wget.download(media[0]['media_url'], out=output_folder)
                downloaded += 1
                print(".", sep='', end='', flush=True)

        tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies,
                                   max_id=last_id - 1)


def main(username, retweets, replies, num_tweets, output_folder):

    # Obtain credentials for accessing the application
    auth = OAuthHandler(Credentials.consumer_key, Credentials.consumer_secret)
    auth.set_access_token(Credentials.access_token, Credentials.access_secret)

    # Call Twitter Auth
    api = tweepy.API(auth)
    download_images(api, username, retweets, replies, num_tweets, output_folder)
