import pandas as pd
import tweepy
from preprocess import *
import os
def get_tweets(username):
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_key = os.environ['ACCESS_KEY']
        access_secret = os.environ['ACCESS_SECRET']
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # Access to user's access key and access secret
        auth.set_access_token(access_key, access_secret)

        # Calling api
        api = tweepy.API(auth)

        # 200 tweets to be extracted
        number_of_tweets=100
        tweets = api.user_timeline(screen_name=username,count=number_of_tweets)
        retweet_count = []
        texts = []
        possibly_sensitive = []
        favorite_count = []
        for tweet in tweets:
            texts.append(tweet.text)
            retweet_count.append(tweet.retweet_count)
            favorite_count.append(tweet.favorite_count)
        dict = {"user_tweets" : texts, "retweet_count" : retweet_count, "favorite_count" : favorite_count}
        tweet_df = pd.DataFrame(dict)
        tweet_df = preprocess(tweet_df)
        return tweet_df
