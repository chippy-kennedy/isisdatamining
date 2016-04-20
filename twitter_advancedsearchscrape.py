#TWITTER DATA COLLECTION

import MySQLdb
import urllib


db = MySQLdb.connect(host="localhost",user="testuser",passwd="test123",db="TESTDB" )
dbcursor = db.cursor()

#Prep a new DB Table
baseSQL ="""CREATE TABLE TWEET-METRICS (
			AttackID CHAR(40) FOREIGN KEY ATTACKS,
			TweetCount INTEGER,
			StartDate DATE,
			EndDate DATE,
			SearchTerms CHAR(40)"""
dbcursor.execute(baseSQL)


searchURL = "https://twitter.com/search?q=Damaturu%2C%20Nigeria&src=typd"
response = urllib2.urlopen(searchURL)

insertSQL = """INSERT INTO TWEET-METRICS (AttackID, TweetCount, StartDate, EndDate, SearchTerms)
				VALUES (1, 100, 2015-04-12, 2015-06-14, 'terrorist')""" 
dbcursor.execute(insertSQL)


db.close()

