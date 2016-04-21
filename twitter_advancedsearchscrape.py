#TWITTER DATA COLLECTION

import urllib,urllib2,re,datetime
import time
import sqlite3
from pyquery import PyQuery as pq
from lxml import html
import requests
import TwitterRequest as tr
import json


# Handle Web Certificate Approval
#http = urllib3.PoolManager(
#    cert_reqs='CERT_REQUIRED', # Force certificate check.
#    ca_certs=certifi.where(),  # Path to the Certifi bundle.
#)


BASEURL = "https://twitter.com/search?"
SEARCHTERMS = "terrorist bangladesh isil"

#q=terrorist%20bangladesh&src=typd&lang=en"

# 1. Setup Twitter Search Query
twitterURL = tr.TwitterRequest(SEARCHTERMS)
url = twitterURL.getURL()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
req = urllib2.Request(url, headers = headers)
jsonResponse = urllib2.urlopen(req).read()

dataJson = json.loads(jsonResponse)


refreshCursor = dataJson['min_position']			
tweets = PyQuery(dataJson['items_html'])('div.js-stream-tweet')



print tweets


# 2. Parse Search Results
tweetCount = 0
#bool continueSearch = True

#scrape page at hand
#tree = html.fromstring(r.text)

#while(continueSearch)
#  time.sleep(10)	


# 3. Save to DB
db = sqlite3.connect('attacks.db')
dbcursor = db.cursor()

#sql = 'INSERT'
#dbcursor.execute(baseSQL)

db.close()

