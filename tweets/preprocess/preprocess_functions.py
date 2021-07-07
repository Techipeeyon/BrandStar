import re
import requests
import os
from expertai.nlapi.cloud.client import ExpertAiClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
from time import sleep
from dotenv import load_dotenv
load_dotenv() 
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
