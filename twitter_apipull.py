#TWITTER DATA COLELCTION

import tweepy
import oauth
import MySQLdb
from tweepy import OAuthHandler
 
# Open database connection & prepare a cursor
db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )
dbcursor = db.cursor()

#OAuth for Twitter API and Tweety API wrapper 
auth = OAuthHandler(oauth.consumer_key, oauth.consumer_secret)
api = tweepy.API(auth)

#Prep DB - TODO: send this to a seperate SQL file
sql = """CREATE TABLE TWEET (
         TWITTER_ID  CHAR(40),
         NAME  CHAR(40) NOT NULL,
         MATCHING_SEARCH_TERM CHAR(20),  
         GEOCODE_LAT DOUBLE PRECISION,
         GEOCODE_LON DOUBLE PRECISION,
         )"""

dbcursor.execute(sql)


#Define Queries To Run on Tweets
query = "isis"

#Iterated through a single query and store matching tweet's metadate
for status in tweepy.Cursor(api.search, q=query).items(1000):
    # Process a single status
    dbcursor.execute("SQL HERE")
    print("\n\n"+status.text)



# Fetch a single row using fetchone() method.
#data = dbcursor.fetchone()

# disconnect from server
db.close()
