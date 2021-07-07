import pandas as pd
from expertai.nlapi.cloud.client import ExpertAiClient
import os
from ..preprocess.preprocess_functions import *
from dotenv import load_dotenv
load_dotenv() 
os.environ["EAI_USERNAME"] = os.environ['EMAIL']
os.environ["EAI_PASSWORD"] = os.environ['PASSWORD']
def getEmotionalTraits(df):
    client = ExpertAiClient()
    taxonomy='emotional-traits'
    language='en'
    emotional_traits = []
    if(len(df['user_tweets'])>20):
        no_of_tweets = 20
    else:
        no_of_tweets = len(df['user_tweets'])
    for i in range(no_of_tweets):
        text = df['user_tweets'][i]
        output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
        for category in output.categories:
            emotional_traits.append(category.hierarchy[1])
    e_dict = {"emotional_traits":emotional_traits}
    e_df = pd.DataFrame(e_dict)
    return e_df
def getBehavorialTraits(df):

    client = ExpertAiClient()
    taxonomy='behavioral-traits'
    language='en'
    big_5_traits = []
    big_5_trait_rate = []
    final_traits = []
    if(len(df['user_tweets'])>20):
        no_of_tweets = 20
    else:
        no_of_tweets = len(df['user_tweets'])
        output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
    for i in range(no_of_tweets):
        text = df['user_tweets'][i]
        output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
        for category in output.categories:
            big_5_traits.append(category.hierarchy[0])
            big_5_trait_rate.append(category.hierarchy[1])
            final_traits.append(category.hierarchy[2])
    b_dict = {
        "big_5_traits":big_5_traits,
        "big_5_trait_rate" : big_5_trait_rate,
        "final_traits" : final_traits
    
    }
    b_df = pd.DataFrame(b_dict)
    b_df['big_5_trait_rate'] = b_df['big_5_trait_rate'].apply(cleanTraitRate)
    return b_df

