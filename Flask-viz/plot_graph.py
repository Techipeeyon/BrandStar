import plotly.express as px
import plotly
import seaborn as sns
import matplotlib.pyplot as plt
import json
from collections import Counter
import pandas as pd
from expertai.nlapi.cloud.client import ExpertAiClient

def drawGraph(df):
    fig = px.histogram(df,y="tweet_type",color="tweetLengthType",width=600,height=600)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
def drawTopKeywords(tweets):
    cnt = Counter(" ".join(tweets).split()).most_common(10)
    word_frequency = pd.DataFrame(cnt, columns=['Top Keywords', 'Frequency'])
    wordfreq = px.histogram(word_frequency,x="Top Keywords",y="Frequency",color_discrete_sequence=px.colors.qualitative.Pastel)
    keyword_plot_json = json.dumps(wordfreq, cls=plotly.utils.PlotlyJSONEncoder)
    return keyword_plot_json
def tweetLengthGraph(df):
    lengthvstweettype = px.histogram(df,x="tweet_type",y="tweet_length",color_discrete_sequence=px.colors.qualitative.Safe)
    length_json = json.dumps(lengthvstweettype, cls=plotly.utils.PlotlyJSONEncoder)
    return length_json
def sentimentGraph(df):
    fig = px.scatter(df, y="positivity",x="tweet_length",color="tweet_type",size="social_count",size_max=60)
    sentiment_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return sentiment_json
def tweetLengthHist(df):
    fig = px.histogram(df, x="tweet_length")
    hist_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return hist_json
def drawDonutCharts(df):
    fig = px.pie(df, names='emotional_traits', title='Emotional traits',hole=.6)
    e_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return e_json


    



