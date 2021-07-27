# Necessary imports
import pandas as pd
from expertai.nlapi.cloud.client import ExpertAiClient
import os
from ..preprocess.preprocess_functions import *
from dotenv import load_dotenv
load_dotenv() 

## Setting up the password to access the expert.ai API
os.environ["EAI_USERNAME"] = os.environ['EMAIL']
os.environ["EAI_PASSWORD"] = os.environ['PASSWORD']

# Getting the emotional traits
def getEmotionalTraits(df):
    # Instantiate the client
    client = ExpertAiClient()
    taxonomy='emotional-traits'
    language='en'
    emotional_traits = []

    # Setting the threshold on the no of tweets to analyze
    if(len(df['user_tweets'])>20):
        no_of_tweets = 20
    else:
        no_of_tweets = len(df['user_tweets'])

    # Iterating through the tweets and classifying them
    for i in range(no_of_tweets):
        text = df['user_tweets'][i]
        output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
        for category in output.categories:
            emotional_traits.append(category.hierarchy[1])

    # Saving as a dict
    e_dict = {"emotional_traits":emotional_traits}

    # Conversion to dataframe
    e_df = pd.DataFrame(e_dict)

    # Returning the dataframe
    return e_df

# Getting the behavorial traits from the tweets
def getBehavorialTraits(df):
    # Instantiate the client
    client = ExpertAiClient()
    taxonomy='behavioral-traits'
    language='en'
    big_5_traits = []
    big_5_trait_rate = []
    final_traits = []

    # Setting the threshold on the no of tweets to analyze
    if(len(df['user_tweets'])>20):
        no_of_tweets = 20
    else:
        no_of_tweets = len(df['user_tweets'])
        output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})

    # Iterating through the tweets and classifying them
    for i in range(no_of_tweets):
        text = df['user_tweets'][i]
        output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
        for category in output.categories:
            big_5_traits.append(category.hierarchy[0])
            big_5_trait_rate.append(category.hierarchy[1])
            final_traits.append(category.hierarchy[2])
    
    # Saving as dict
    b_dict = {
        "big_5_traits":big_5_traits,
        "big_5_trait_rate" : big_5_trait_rate,
        "final_traits" : final_traits
    
    }

    # Conversion to dataframe
    b_df = pd.DataFrame(b_dict)

    # Applying preprocessing function 
    b_df['big_5_trait_rate'] = b_df['big_5_trait_rate'].apply(cleanTraitRate)

    # Returning the dataframe
    return b_df

