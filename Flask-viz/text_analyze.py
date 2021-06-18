import pandas as pd
import numpy as np
from collections import Counter

def getTopKeywordInsights(tweets):
    cnt = Counter(" ".join(tweets).split()).most_common(10)
    word_frequency = pd.DataFrame(cnt, columns=['Top Keywords', 'Frequency'])
    keyword_insights = "Based on our analysis the keyword used the most in your tweets was this {}. On the contrast the least used keyword was {}".format(word_frequency['Top Keywords'][word_frequency['Frequency'].argmax()],word_frequency['Top Keywords'][word_frequency['Frequency'].argmin()])
    return keyword_insights

def getTweetInsights(tweets_df):
    final_string = ""
    index = tweets_df['tweet_length'].argmax()
    min_index = tweets_df['tweet_length'].argmin()
    if(tweets_df['tweet_type'][index] == 'UNPOPULAR'):
        final_string = "Your max tweet length of {} characters is not popular which could mean that maybe having a shorter tweet might result in better reach!".format(tweets_df['tweet_length'][index])
    elif(tweets_df['tweet_type'][index] == 'POPULAR'):
        final_string = "Your max tweet length of {} characters has a very good reach with your users which means that whatever you are doing is right and keep on doing it:)".format(tweets_df['tweet_length'][index])
    elif(tweets_df['tweet_type'][index] == 'NORMAL'):
        final_string = "Your max tweet length of {} is reaching users just right. Try having more content and see how it influences your reach! ".format(tweets_df['tweet_length'][index])        
    if(tweets_df['tweet_type'][min_index] == 'UNPOPULAR'):
        final_string += "On the contrary your tweet having {} characters is not popular which could mean that maybe having a longermin_ tweet might result in better reach!".format(tweets_df['tweet_length'][min_index])
    elif(tweets_df['tweet_type'][min_index] == 'POPULAR'):
        final_string += "On the contrary your tweet having {} characters has a very good reach with your users which means that whatever you are doing is right and keep on doing it:)".format(tweets_df['tweet_length'][min_index])
    elif(tweets_df['tweet_type'][min_index] == 'NORMAL'):
        final_string += "On the contrary your tweet having {} is reaching users just right. Try having more content and see how it influences your reach! ".format(tweets_df['tweet_length'][min_index])
    return final_string

def getPopularityInsights(tweets_df):
    max_value = tweets_df['tweet_type'].value_counts().argmax()
    min_value = tweets_df['tweet_type'].value_counts().argmin()
    max_index = tweets_df['tweet_type'].value_counts().index[max_value]
    min_index = tweets_df['tweet_type'].value_counts().index[min_value]
    return_str = "Most of your tweets fall in the {} category according to the data from your last 100 tweets which also means that most of your tweets are not {}  ".format(max_index, min_index)
    return return_str