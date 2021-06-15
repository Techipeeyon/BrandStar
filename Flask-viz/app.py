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
from rq import Queue
from rq.job import Job
from worker import conn
tweets_df = None
e_df = None
app = Flask(__name__,static_url_path='/static', static_folder="/home/dazedtiara6667/Flask-viz/templates/assets")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
q = Queue(connection=conn)
@app.route('/<username>/dashboard',methods=['GET','POST'])
def dashboard(username):
    print(username)
    context,tweets_df,ed_df = getUserContext(user=username)
    return render_template('index.html',context=context)
def getUserContext(user):
    tweets_df = get_tweets(user)
    retweet_sum = tweets_df['retweet_count'].sum()
    e_df = getEmotionalTraits(tweets_df)
    plot_graph = drawGraph(tweets_df)
    screen_name,image_url,followers,friends = getUserDetails(user)
    total_fav = tweets_df['favorite_count'].sum()
    context = {
        "plot_graph" : plot_graph,
        "retweet_sum" : retweet_sum,
        "screen_name" : screen_name,
        "image_url" : image_url,
        "followers" : followers,
        "friends" : friends,
        "favorites" : total_fav

    }
    return (context,tweets_df,e_df)
        


@app.route('/',methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        user = request.form['username']
        user = str(user)
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
@app.route('/dashboard/charts')
def charts(e_df,tweets_df):
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
        "e_graph" : emot_graph
    }
    return render_template('chart.html',context=context)
if __name__ == '__main__':
   app.run(debug=True)
