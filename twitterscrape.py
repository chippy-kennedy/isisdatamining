#TWITTER DATA COLELCTION

import tweepy
import oauth
from tweepy import OAuthHandler
 
 
auth = OAuthHandler(oauth.consumer_key, oauth.consumer_secret)
auth.set_access_token(oauth.access_token, oauth.access_secret)
 
api = tweepy.API(auth)


for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text) 
