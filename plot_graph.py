import plotly.express as px
import plotly
import seaborn as sns
import matplotlib.pyplot as plt
import json
from collections import Counter
import pandas as pd
from expertai.nlapi.cloud.client import ExpertAiClient
from preprocess_functions import *
def drawGraph(df):
    fig = px.histogram(df,y="tweet_type",color="tweetLengthType",width=700,height=500)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json
def drawTopKeywords(tweets,width=1100,height=800):
    cnt = Counter(" ".join(tweets).split()).most_common(10)
    word_frequency = pd.DataFrame(cnt, columns=['Top Keywords', 'Frequency'])
    wordfreq = px.histogram(word_frequency,x="Top Keywords",y="Frequency",color_discrete_sequence=px.colors.qualitative.Pastel,width=width,height=height)
    keyword_plot_json = json.dumps(wordfreq, cls=plotly.utils.PlotlyJSONEncoder)
    wordfreq.update_yaxes(automargin=True)

    return keyword_plot_json
def tweetLengthGraph(df):
    lengthvstweettype = px.histogram(df,x="tweet_type",y="tweet_length",color_discrete_sequence=px.colors.qualitative.Safe,width=500,height=600)
    length_json = json.dumps(lengthvstweettype, cls=plotly.utils.PlotlyJSONEncoder)
    return length_json
def sentimentGraph(df):
    try:
        fig = px.scatter(df, y="positivity",x="tweet_length",color="tweet_type",size="social_count",size_max=60,width=1100,height=800)
    except:
        fig = px.scatter(df,y="positivity",x="tweet_length",size="social_count",size_max=60)
    sentiment_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return sentiment_json
def tweetLengthHist(df):
    fig = px.histogram(df, x="tweet_length",width=500,height=600)
    hist_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return hist_json
def drawDonutCharts(df):
    fig = px.pie(df, names='emotional_traits', title='Emotional traits',hole=.6,width=500,height=600)
    e_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return e_json
def drawTopLocationChart(df):
    fig = px.bar(df,x='Location',color_discrete_sequence=px.colors.qualitative.Pastel)
    loc_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return loc_json
def drawRatingChart(df):
    fig = px.histogram(df,x='Rating')
    rate_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return rate_json
def drawBehavorialEmotionalChart(df):
    reviews_df, b_reviews_df = getUserTraits(df)
    final_traits_graph = px.pie(b_reviews_df, names='final_traits', title='',hole=.6,width=500,height=600)
    big_5_trait_graph = px.bar(b_reviews_df, x='big_5_traits', color= 'big_5_trait_rate',width=500,height=600,color_discrete_sequence=px.colors.qualitative.Pastel)
    f_graph_json = json.dumps(final_traits_graph, cls=plotly.utils.PlotlyJSONEncoder)
    big5_graph_json = json.dumps(big_5_trait_graph, cls=plotly.utils.PlotlyJSONEncoder)
    fig = px.pie(reviews_df, names='emotional_traits',hole=.6,width=500,height=600)
    e_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return (e_json,f_graph_json,big5_graph_json)

def drawBehavorialCharts(df):
    final_traits_graph = px.pie(df, names='final_traits', title='',hole=.6,width=500,height=600)
    big_5_trait_graph = px.bar(df, x='big_5_traits', color= 'big_5_trait_rate',width=500,height=600,color_discrete_sequence=px.colors.qualitative.Pastel)
    f_graph_json = json.dumps(final_traits_graph, cls=plotly.utils.PlotlyJSONEncoder)
    big5_graph_json = json.dumps(big_5_trait_graph, cls=plotly.utils.PlotlyJSONEncoder)
    return (f_graph_json,big5_graph_json)

    

    






    



