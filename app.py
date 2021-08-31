# Necessary Imports
from flask import Flask, render_template, make_response, url_for, request,redirect
import pandas as pd
from tweets.preprocess.preprocess_functions import *
from tweets.nlp_functions.sentiments import *
from tweets.preprocess.preprocess import * 
from tweets.graphs.plot_graph import *
from tweets.user.user_details import *
from tweets.user.user_stats import *
from tweets.reports.text_analyze import *
from reviews.preprocess.get_user_reviews import *
from tweets.utils.TweetUtils import TweetUtils
from reviews.utils.ReviewUtils import ReviewUtils
import os

# Intializing the tweets_df 
tweet_utils = TweetUtils()

# Initializing the flask app
app = Flask(__name__,static_url_path='/static', static_folder="templates/assets")

# Dashboard route
@app.route('/<username>/dashboard',methods=['GET','POST'])
def dashboard(username):
    print(username)
    context = getUserContext(user=username)
    return render_template('index.html',context=context)

# Getting some common things like retweets and favorites etc to be shown on dashboard
def getUserContext(user):
    tweets_df = tweet_utils.get_tweets(user)
    ## Getting the maximum and minimum values along with the indexes for the popularity of tweets
    max,min,max_index,min_index = getTweetPopularityStats(tweets_df)
    # Getting the retweet sum, screen_ame and image_url etc to be shown on the dashboard
    retweet_sum,screen_name,image_url,followers,friends,total_fav = getUserInfo(user = user,tweets_df = tweets_df)
    
    # Getting the maximum and average sentiment score found in the tweets
    avg_sentiment,max_sentiment_value = getSentimentStats(tweets_df)
    
    # Getting the no of tweets which have a certain tweet length type("LONG=SIZED", "MEDIUM-SIZED", "SHORT")
    maxlength_count,minlength_count,maxlengthtype_index,minlengthtype_index = getTweetLengthStats(tweets_df)
    
    # Getting the graphs in JSON format to be plotted
    plot_graph = drawTweetTypeGraph(tweets_df)
    hist_graph = tweetLengthHist(tweets_df)

    # Passing these values in the context which would then be used in the html files
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
        "max_sentiment_value" : max_sentiment_value,
        "hist_graph" : hist_graph

    }
    return (context)
        

# Home route where the landing page is shown
@app.route('/',methods = ['POST', 'GET'])
def home():
    # POST method used to get the username entered by the user
    if request.method == 'POST':
        user = request.form['username']
        
        # Redirecting the user to the dashboard page
        return redirect(url_for('dashboard',username=user))
    return render_template('landing.html')

# Reports route where the reports are shown
@app.route('/<username>/reports')
def textAnalyze(username):
    # Using the tweets_df defined
    tweets_df = tweet_utils.getDataFrame()
    
    # Getting the graphs in JSON format to be drawn in the reports section
    keyword_graph = drawTopKeywords(tweets=tweets_df['user_tweets'],height=300,width=900)
    
    # Getting various insights from data in text format
    final_string = getTweetInsights(tweets_df)
    pop_string = getPopularityInsights(tweets_df)
    keyword_insights = getTopKeywordInsights(tweets=tweets_df['user_tweets'])
    screen_name,image_url,followers,friends = getUserDetails(username)
    
    # Creating context which would be used to access these values in the html file
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

# Error page
@app.route('/error')
def error():
    return render_template('error.html')

# Route for showing the detailed analysis of the brand
@app.route('/<username>/charts')
def charts(username):
    # Getting the tweets collected
    tweets_df = tweet_utils.getDataFrame()
    # Collecting the graphs in JSON format to be shown on the site
    e_df = getEmotionalTraits(tweets_df)
    keyword_graph = drawTopKeywords(tweets_df['user_tweets'])
    screen_name,image_url,followers,friends = getUserDetails(username)
    b_df = getBehavorialTraits(tweets_df)
    f_graph_json,big5_graph_json = drawBig5TraitCharts(b_df)
    length_graph = tweetLengthGraph(tweets_df)
    sentiment_graph = sentimentGraph(tweets_df)
    emot_graph = drawDonutCharts(e_df)
    
    # Creating context to access these values in our html file
    context = {
        "keyword_graph":keyword_graph,
        "length_graph" :length_graph,
        "sentiment_graph":sentiment_graph,
        "e_graph" : emot_graph,
        "user" : username,
        "screen_name" : screen_name,
        "image_url" : image_url,
        "f_graph_json" : f_graph_json,
        "big5_graph_json" : big5_graph_json, 
    }
    return render_template('chart.html',context=context)

# Route for showing the detailed analysis of user-reviews
@app.route('/<username>/user-base-analysis')
def userBaseAnalysis(username):
    # Searching for the company on trustpilot(user-review site) with the username
    review_utils = ReviewUtils(username = username, n_pages = 2)

    review_utils.getReviewEndPoint()

    review_utils.scrape_reviews()
    
    # Creating the PATH with the endpoint recieved
    
    # Getting the data back as Pandas dataframe
    user_reviews_df, scrape_success = review_utils.user_reviews_df, review_utils.scrape_success
    
    # Redirecting user to error page if the site was not found on trustpilot
    if(scrape_success == 0):
        return(redirect(url_for('error')))
    
    # Collecting the graphs in JSON format
    loc_json = drawTopLocationChart(user_reviews_df)
    rate_json = drawRatingChart(user_reviews_df)
    review_json,f_graph_json,big5_graph_json = drawBehavorialEmotionalChart(user_reviews_df)
    screen_name,image_url,followers,friends = getUserDetails(username)
    
    # Creating the context to be used in our html file
    context = {
        "image_url" : image_url,
        "screen_name" : screen_name,
        "user" : username,
        "loc_json" : loc_json,
        "rate_json" : rate_json,
        "review_json" : review_json,
        "f_graph_json" : f_graph_json,
        "big5_graph_json" : big5_graph_json
    }
    return render_template('user-analysis.html',context=context)


# Starting the app
if __name__ == '__main__':
   app.run(debug=True)
