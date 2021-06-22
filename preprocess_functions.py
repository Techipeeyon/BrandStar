import re
import os
from expertai.nlapi.cloud.client import ExpertAiClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
from time import sleep
import requests
import os
 
os.environ["EAI_USERNAME"] = os.environ['EMAIL']
os.environ["EAI_PASSWORD"] = os.environ['PASSWORD']
def cleanTraitRate(text):
    rating_text = text.split(" ")[1]
    return rating_text
def classifyTweets(count):
    if(count>20000):
        return "POPULAR"
    elif(count>10000 and count<20000):
        return "NORMAL"
    elif(count>0 and count<10000):
        return "UNPOPULAR"
def classifyTweetLength(length):
    if(length>0 and length<50):
        return "SHORT TWEET"
    elif(length>=50 and length<=100):
        return "MEDIUM SIZED TWEET"
    elif(length>100 and length<=280):
        return "LONG TWEET"
def getPositiveSentiment(text):
    client = ExpertAiClient()
    language= 'en'
    output = client.specific_resource_analysis(
    body={"document": {"text": text}},
    params={'language': language, 'resource': 'sentiment'})
    return output.sentiment.positivity
def remove_links(text):
    STOP_WORDS = stopwords.words()
    wnl=WordNetLemmatizer()
    text = text.replace("RT","")
    text = re.sub(r'\d+', "", text)
    text = re.sub('http://\S+|https://\S+', '', text)
    emoji_pattern = re.compile("["
                        u"\U0001F600-\U0001F64F"
                        u"\U0001F680-\U0001F6FF"
                        u"\U0001F1E0-\U0001F1FF"
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'@\w+',  '', text).strip()
    text = re.sub("[^a-zA-Z0-9 ']", "", text)
    text=' '.join([wnl.lemmatize(i) for i in text.lower().split()])
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in STOP_WORDS]
    filtered_sentence = (" ").join(tokens_without_sw)
    text = filtered_sentence

    return text
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

def ratingClassifier(text):
    rating_value = text[0]
    return rating_value
def getUserTraits(df):
    client = ExpertAiClient()
    taxonomy = 'emotional-traits'
    language = 'en'
    headers=""
    reviews = ""
    taxonomy_b = 'behavioral-traits'
    client = ExpertAiClient()

    user_review_list = []
    emotional_traits = []
    big_5_traits = []
    big_5_trait_rate = []
    final_traits = []
    try:
        for header in df['Header']:
            headers+=header
        for review in df['Review']:
            reviews+=review
        user_review_list = [headers,reviews]
        for i in range(2):
            text = user_review_list[i]
            output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
            output_b = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
            for category in output_b.categories:
                big_5_traits.append(category.hierarchy[0])
                big_5_trait_rate.append(category.hierarchy[1])
                final_traits.append(category.hierarchy[2])
            for category in output.categories:
                emotional_traits.append(category.hierarchy[1])
        e_dict = {
            "emotional_traits" : emotional_traits
        }
        b_dict = {
            "big_5_traits":big_5_traits,
            "big_5_trait_rate" : big_5_trait_rate,
            "final_traits" : final_traits
        
        }
        b_df = pd.DataFrame(b_dict)
        b_df['big_5_trait_rate'] = b_df['big_5_trait_rate'].apply(cleanTraitRate)
        reviews_df = pd.DataFrame(e_dict)
    except:
        emotional_traits = ['Repulsion','Hatred','Happiness','Excitement','Love','Happiness','Excitement']
        big_5_traits = ['Sociality', 'Sociality']
        big_5_trait_rate = ['Sociality low', 'Sociality fair']
        final_traits = ['Asociality', 'Seriousness']
        e_dict = {
            "emotional_traits" : emotional_traits
        }


        b_dict = {
            "big_5_traits":big_5_traits,
            "big_5_trait_rate" : big_5_trait_rate,
            "final_traits" : final_traits
        
        }
        reviews_df = pd.DataFrame(e_dict)
        b_df = pd.DataFrame(b_dict)
        b_df['big_5_trait_rate'] = b_df['big_5_trait_rate'].apply(cleanTraitRate)
    return (reviews_df,b_df)