from flask import Flask, render_template, send_file, make_response, url_for, Response,request,redirect

#Pandas and Matplotlib
import pandas as pd
from plot_graph import *
import plotly.express as px
import os
import asyncio
import seaborn as sns
from collections import Counter
from scrape_tweets import *
from user_details import *
from user_stats import *
from text_analyze import *
tweets_df = None
app = Flask(__name__,static_url_path='/static', static_folder="/home/dazedtiara6667/Flask-viz/templates/assets")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
@app.route('/<username>/dashboard',methods=['GET','POST'])
def dashboard(username):
    print(username)
    context = getUserContext(user=username)
    return render_template('index.html',context=context)
def getUserContext(user):
    global tweets_df
    tweets_df = get_tweets(user)
    max,min,max_index,min_index = getTweetPopularityStats(tweets_df)
    retweet_sum,screen_name,image_url,followers,friends,total_fav = getGeneralStats(user = user,tweets_df = tweets_df)
    avg_sentiment,max_sentiment_value = getSentimentStats(tweets_df)
    maxlength_count,minlength_count,maxlengthtype_index,minlengthtype_index = getTweetLengthStats(tweets_df)
    plot_graph = drawGraph(tweets_df)
    context = {
        "plot_graph" : plot_graph,
        "retweet_sum" : retweet_sum,
        "screen_name" : screen_name,
        "image_url" : image_url,
        "followers" : followers,
        "friends" : friends,
        "favorites" : total_fav,
        "user" : user,
        "max_index" : max_index,
        "min_index" : min_index,
        "max" : max,
        "min" : min,
        "maxlength_count" : maxlength_count,
        "minlength_count" : minlength_count,
        "maxlengthtype_index" : maxlengthtype_index,
        "minlengthtype_index" : minlengthtype_index,
        "avg_sentiment" : int(avg_sentiment),
        "max_sentiment_value" : max_sentiment_value
    }
    return (context)
        


@app.route('/',methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        user = request.form['username']
        return redirect(url_for('dashboard',username=user))
    return render_template('landing.html')

@app.route('/visualize')
def visualize():
    sns.distplot(tweets_df['tweet_length'])
    canvas = FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='img/png')

@app.route('/<username>/reports')
def textAnalyze(username):
    global tweets_df

    back = request.referrer
    keyword_graph = drawTopKeywords(tweets=tweets_df['user_tweets'],height=300,width=900)
    final_string = getTweetInsights(tweets_df)
    pop_string = getPopularityInsights(tweets_df)
    keyword_insights = getTopKeywordInsights(tweets=tweets_df['user_tweets'])
    screen_name,image_url,followers,friends = getUserDetails(username)
    context = {
        "final_string" : final_string,
        "pop_string" : pop_string,
        "keyword_insights" : keyword_insights,
        "image_url" : image_url,
        "screen_name" : screen_name,
        "keyword_graph" : keyword_graph,
        "user" : username
    }
    return render_template('reports.html',context = context)

@app.route('/<username>/charts')
def charts(username):
    global tweets_df
    back = request.referrer
    e_df = getEmotionalTraits(tweets_df)
    keyword_graph = drawTopKeywords(tweets_df['user_tweets'])
    length_graph = tweetLengthGraph(tweets_df)
    sentiment_graph = sentimentGraph(tweets_df)
    hist_graph = tweetLengthHist(tweets_df)
    emot_graph = drawDonutCharts(e_df)
    context = {
        "keyword_graph":keyword_graph,
        "length_graph" :length_graph,
        "sentiment_graph":sentiment_graph,
        "hist_graph" : hist_graph,
        "e_graph" : emot_graph,
        "user" : username,
    }
    return render_template('chart.html',context=context)


if __name__ == '__main__':
   app.run(debug=True)
