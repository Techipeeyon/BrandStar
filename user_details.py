import tweepy
consumer_key = "NgBti22Stqnqz7v6ZqwTdUDxp"
consumer_secret = "4JvCE6t1rkMiVhUD97NBezm34eR7hV5wLQ27NmYJg2QAyYE28w"
access_key = "1143115156295077888-QRzzKGCMuiS0pKUkF2EzbTWjKqLVyb"
access_secret = "Cl23SQe1mESEUKfK3kdTgqpaQIHso8xxpfr9eEmDY43SY"

def getUserDetails(username):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Calling api
    api = tweepy.API(auth)
    user = api.get_user(screen_name=username)
    return(user.screen_name,user.profile_image_url_https,user.followers_count,user.friends_count)
