#TWITTER DATA COLLECTION

import time
import sqlite3
import urllib
from lxml import html
import requests
import TwitterRequest as tr
import ssl
import urllib3
import certifi


# Handle Web Certificate Approval
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)


BASEURL = "https://twitter.com/search?"
SEARCHTERMS = "terrorist bangladesh isil"

#q=terrorist%20bangladesh&src=typd&lang=en"

# 1. Setup Twitter Search Query
request = tr.TwitterRequest(SEARCHTERMS)
headers = {'User-agent' : 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'}
query = request.getURL()
res = http.get(query)
response = requests.get(query, headers = headers)
print query

# 2. Parse Search Results
tweetCount = 0
#bool continueSearch = True

#scrape page at hand
print response
tree = html.fromstring(response.content)

#while(continueSearch)
#  time.sleep(10)	


# 3. Save to DB
db = sqlite3.connect('attacks.db')
dbcursor = db.cursor()

#sql = 'INSERT'
#dbcursor.execute(baseSQL)

db.close()

