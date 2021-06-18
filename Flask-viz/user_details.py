import tweepy
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def getUserDetails(username):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Calling api
    api = tweepy.API(auth)
    user = api.get_user(screen_name=username)
    return(user.screen_name,user.profile_image_url_https,user.followers_count,user.friends_count)
