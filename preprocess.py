import pandas as pd
import numpy as np
from preprocess_functions import *
def preprocess(tweets_df):
    tweets_df['social_count'] = tweets_df['favorite_count'] + tweets_df['retweet_count']
    tweets_df['positivity'] = tweets_df['user_tweets'].apply(getPositiveSentiment)

    tweets_df['tweet_length'] = tweets_df['user_tweets'].apply(len)
    tweets_df['user_tweets'] = tweets_df['user_tweets'].apply(remove_links)
    tweets_df['tweet_type'] = tweets_df['social_count'].apply(classifyTweets)
    tweets_df['tweetLengthType'] = tweets_df['tweet_length'].apply(classifyTweetLength)
    return tweets_df
