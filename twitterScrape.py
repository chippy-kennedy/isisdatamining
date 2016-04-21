#https://github.com/Jefferson-Henrique/GetOldTweets-python
import got
import sqlite3
import datetime

def main():

	def printTweet(descr, t):
		print descr
		print "Username: %s" % t.username
		print "Retweets: %d" % t.retweets
		print "Text: %s" % t.text
		print "Mentions: %s" % t.mentions
		print "Hashtags: %s\n" % t.hashtags


	def getSearchTerms(cursor, attack):
		cursor.execute('SELECT end_date,type,primary_location,perpetrator FROM attacks WHERE attack_id = ?;', (attack,))
		allTerms = list(cursor.fetchone())
		date = allTerms.pop(0)
		searchTerms = ','.join(map(str,allTerms))
		allTerms = (date, searchTerms)
		print allTerms
		return allTerms

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


	def insertMetrics(dbcursor, attack):
		#run intended twitter query with got lib
		terms = getSearchTerms(dbcursor,attack)

		date = datetime.datetime.strptime(terms[0], "%Y-%m-%d %H:%M:%S")
		startQueryDate = date.strftime('%Y-%m-%d')
		endQueryDate = (date + datetime.timedelta(days=3)).strftime('%Y-%m-%d')

		print startQueryDate

		#tweetCriteria = got.manager.TweetCriteria().setQuerySearch(terms[1])#.setSince(startQueryDate).setUntil(endQueryDate).setMaxTweets(100)
		tweetCriteria = got.manager.TweetCriteria().setQuerySearch(terms[1]).setSince(startQueryDate).setUntil(endQueryDate).setMaxTweets(56)
		tweets = got.manager.TweetManager.getTweets(tweetCriteria)

		print tweets

		numTweets = len(tweets)
		avgRetweets = getAvgRetweets(tweets)

		print 'size: '+str(numTweets)
		print 'avg retweets: ' + str(avgRetweets)

		#delay for twitter
		sleep(10)

		insert_sql = (
			"INSERT INTO tweet_metrics (search_terms, attack_id, tweet_count, avg_retweets, start_date, end_date) "
			"VALUES (?, ?, ?, ?, ?, ?)"
		)
		data = (terms[1], attack, numTweets, avgRetweets, startQueryDate, endQueryDate)
		try:
			dbcursor.execute(insert_sql, data)
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
		insertMetrics(dbcursor, aid)

	db.commit()
	db.close()


if __name__ == '__main__':
	main()
