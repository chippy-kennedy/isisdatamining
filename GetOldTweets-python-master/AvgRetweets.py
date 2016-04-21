import got
import sys

def main():

	def printTweet(descr, t):
		print descr
		print "Username: %s" % t.username
		print "Retweets: %d" % t.retweets
		print "Text: %s" % t.text
		print "Mentions: %s" % t.mentions
		print "Hashtags: %s\n" % t.hashtags

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


	# Example 2 - Get tweets by query search
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('rocket isis').setSince("2015-10-31").setUntil("2015-11-01").setMaxTweets(sys.maxint)
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)
	firstTweet = tweets[0]
	numTweets = len(tweets)
	avgRetweets = getAvgRetweets(tweets)

	printTweet("### Example 2 - Get tweets by query search [rocket isis]", firstTweet)
	print 'size: '+str(numTweets)
	print 'avg retweets: ' + str(avgRetweets)

if __name__ == '__main__':
	main()
