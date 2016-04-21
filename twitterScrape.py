#https://github.com/Jefferson-Henrique/GetOldTweets-python
import got
import sqlite3
import datetime, time

def main():

	def printTweet(descr, t):
		print descr
		print "Username: %s" % t.username
		print "Retweets: %d" % t.retweets
		print "Text: %s" % t.text
		print "Mentions: %s" % t.mentions
		print "Hashtags: %s\n" % t.hashtags


	def getSearchTerms(cursor, attack):
		cursor.execute('SELECT start_date, end_date, type, primary_location, perpetrator FROM attacks WHERE attack_id = ?;', (attack,))
		allTerms = list(cursor.fetchone())

		startDate 		= allTerms[0]
		endDate 		= allTerms[1]
		attackType 		= allTerms[2]
		attackLocation 	= allTerms[3]
		perpetrator 	= allTerms[4]

		searchTerms = {
			'startDate': startDate,
			'endDate': endDate,
			'attackType': attackType,
			'attackLocation': attackLocation,
			'perpetrator': perpetrator,
		}

		if attack < 10:
			print searchTerms

		return searchTerms

	def getAvgRetweets(tweets):
		numTweets = len(tweets)
		if numTweets <= 0:
				return None

		# Pop pulls off first tweet so it doesn't affect average
		firstTweet = tweets.pop(0)
		totalRetweets = firstTweet.retweets

		for tweet in tweets:
			totalRetweets += tweet.retweets

		return totalRetweets /  numTweets



	def insertMetrics(db, dbcursor, attack):
		#run intended twitter query with got lib
		terms = getSearchTerms(dbcursor,attack)

		start_date = datetime.datetime.strptime(terms['startDate'], "%Y-%m-%d %H:%M:%S")
		end_date = datetime.datetime.strptime(terms['endDate'], "%Y-%m-%d %H:%M:%S")
		startQueryDate = start_date.strftime('%Y-%m-%d')
		endQueryDate = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

		print startQueryDate

		#tweetCriteria = got.manager.TweetCriteria().setQuerySearch(terms['searchTerms'])#.setSince(startQueryDate).setUntil(endQueryDate).setMaxTweets(100)
		tweetCriteria = got.manager.TweetCriteria().setQuerySearch(terms['searchTerms']).setSince(startQueryDate).setUntil(endQueryDate).setMaxTweets(56)
		tweets = got.manager.TweetManager.getTweets(tweetCriteria)

		print tweets

		numTweets = len(tweets)
		avgRetweets = getAvgRetweets(tweets)

		print 'number of tweets: '+str(numTweets)
		print 'avg retweets: ' + str(avgRetweets)

		#delay for twitter
		time.sleep(10)

		insert_sql = (
			"INSERT INTO tweet_metrics (search_terms, attack_id, tweet_count, avg_retweets, start_date, end_date) "
			"VALUES (?, ?, ?, ?, ?, ?)"
		)
		data = (terms['searchTerms'], attack, numTweets, avgRetweets, startQueryDate, endQueryDate)
		try:
			dbcursor.execute(insert_sql, data)
			db.commit()
		except sqlite3.Error as e:
			print "Tweet Metrics Not Saved: ", e.args[0]


	#MAIN
	db = sqlite3.connect('attacks.db')
	db.text_factory = str
	dbcursor = db.cursor()

	dbcursor.execute("SELECT attack_id from attacks")
	attackids = dbcursor.fetchall()

	for attack in attackids:
		aid = attack[0]
		insertMetrics(db, dbcursor, aid)

	db.commit()
	db.close()


if __name__ == '__main__':
	main()
