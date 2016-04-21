#TWITTER DATA COLLECTION

import time
import sqlite3
import urllib
from lxml import html
import requests
import TwitterRequest as tr

BASEURL = "https://twitter.com/search?"
SEARCHTERMS = "terrorist bangladesh isil"

#q=terrorist%20bangladesh&src=typd&lang=en"

# 1. Setup Twitter Search Query
query = tr.TwitterRequest(SEARCHTERMS)

print query

# 2. Parse Search Results
tweetCount = 0
#bool continueSearch = True

#scrape page at hand
page = requests.get(query)
tree = html.fromstring(page.content)



#while(continueSearch)
#  time.sleep(10)	


# 3. Save to DB
db = sqlite3.connect('test.db')
dbcursor = db.cursor()

#sql = 'INSERT'



#Prep a new DB Table
#tempSQL ='CREATE TABLE Attacks (attackid INTEGER PRIMARY KEY)'
#baseSQL ='CREATE TABLE TweetMetrics (SearchTerms CHAR(40) PRIMARY KEY,FOREIGN KEY(attackid) REFERENCES attack(attackid),TweetCount INTEGER,StartDate DATE,EndDate DATE'


dbcursor.execute(baseSQL)

#response = urllib2.urlopen(searchURL)
#
#insertSQL = """#INSERT INTO TWEET-METRICS (AttackID, TweetCount, StartDate, EndDate, SearchTerms)
#				VALUES (1, 100, 2015-04-12, 2015-06-14, 'terrorist')""" 
#dbcursor.execute(insertSQL)


db.close()



class TwitterResponse:
	def __init__(hmi, ih, isr, irr, sc, rc, fri):
		self.has_more_items = hmi
		self.items_html = ih
		self.is_scrolling_req = isr
		self.is_refresh_req = irr
		self.scroll_cursor = sc
		self.refresh_cursor = rc
		self.focused_refresh_interval = fri
	 
