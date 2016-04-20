#TWITTER DATA COLLECTION

import MySQLdb

db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )
dbcursor = db.cursor()

#Prep a new DB Table
sql = "CREATE TABLE TWEET-METRICS (
			ATTACK_ID CHAR(40) FOREIGN KEY ATTACKS,
			DAY0_TWEETCOUNT INTEGER,
			DAY1_TWEETCOUNT INTEGER,
			DAY2_TWEETCOUNT INTEGER,
			DAY3_TWEETCOUNT INTEGER)"

searchURL = "https://twitter.com/search?q=Damaturu%2C%20Nigeria&src=typd"i


