# Necessary imports
import pandas as pd
import tweepy
from ..preprocess.preprocess import *
import os
from dotenv import load_dotenv
load_dotenv() 
class TweetUtils:
    def __init__(self):
        # Initializing the utils class
        self.tweets_df = None
        self.consumer_key = os.environ['CONSUMER_KEY']
        self.consumer_secret = os.environ['CONSUMER_SECRET']
        self.access_key = os.environ['ACCESS_KEY']
        self.access_secret = os.environ['ACCESS_SECRET']

    def populateDataFrame(self, df):
        # Populate dataframe with collected twitter data
        self.tweets_df = df
    
    def getDataFrame(self):
        return self.tweets_df

    def get_tweets(self, username):
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

        # Access to user's access key and access secret
        auth.set_access_token(self.access_key, self.access_secret)

        # Calling api
        api = tweepy.API(auth)

        # 100 tweets to be extracted
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
        df = pd.DataFrame(dict)
        df = preprocess(df)
        self.tweets_df = df

        return self.tweets_df
