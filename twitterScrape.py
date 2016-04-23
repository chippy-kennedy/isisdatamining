#https://github.com/Jefferson-Henrique/GetOldTweets-python
import got

import re, sys
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


    def getFields(cursor, attack):
        cursor.execute('SELECT start_date, end_date, type, primary_location, perpetrator FROM attacks WHERE attack_id = ?;', (attack,))
        allTerms = list(cursor.fetchone())

        startDate         = allTerms[0]
        endDate         = allTerms[1]
        attackType         = str(allTerms[2])
        attackLocation     = str(allTerms[3])
        perpetrator     = str(allTerms[4])

        fields = {
            'startDate': startDate,
            'endDate': endDate,
            'attackType': attackType,
            'attackLocation': attackLocation,
            'perpetrator': perpetrator,
        }

        return fields

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

    # given a perpetratro returns a twitter search term
    # with any additional names that the group go's by
    # separated by OR for twitter search
    def getExtendedPerpetrator(perpetrator):
        extended_name_dict = {
            "PKK"   : "Kurdistan Workers' Party OR PKK",
            "ISIS"  : "ISIS OR ISIL OR Islamic State"
        }
        if perpetrator in extended_name_dict:
            return extended_name_dict[perpetrator]
        else:
            return perpetrator

    # given a term converts the commas to OR's
    # this is so twitters search knows to search for either of the terms
    def commaToOr(term):
        if not term:
            return ""
        return re.sub("( )*,( )*", " OR ", term)

    # combines terms for search on twitter
    # basically just adds AND between them
    def combineTerms(term1, term2):
        return str(term1)+' AND '+str(term2)

    # given a dictionary containing
    # attackType, attackLocation, perpetrator
    # returns a list of search terms for twitter
    def getSearchQueries(fields):
        searchQueries = []

        # computed terms
        perpetratorExtended = getExtendedPerpetrator(fields['perpetrator'])

        attackType = commaToOr(fields['attackType'])
        attackLocation = commaToOr(fields['attackLocation'])
        perpetratorExtended = commaToOr(perpetratorExtended)

        typeLocation = combineTerms(attackType, attackLocation)
        typeGroup = combineTerms(attackType, perpetratorExtended)
        locationGroup = combineTerms(attackLocation, perpetratorExtended)

        searchQueries = {
            "type and location"  : typeLocation,
            "type and group"     : typeGroup,
            "location and group" : locationGroup,
            "general 1"          : "terrorist attack"
        }

        return searchQueries

    # Given a query, searches Twitter and returns
    # numTweets, avgRetweets, avgFavorites
    def searchTwitter(query):


    def insertMetrics(db, dbcursor, attack):
        #run intended twitter query with got lib
        fields = getFields(dbcursor,attack)

        start_date = datetime.datetime.strptime(fields['startDate'], "%Y-%m-%d %H:%M:%S")
        end_date = datetime.datetime.strptime(fields['endDate'], "%Y-%m-%d %H:%M:%S")
        startQueryDate = start_date.strftime('%Y-%m-%d')
        endQueryDate = (start_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        searchQueries = getSearchQueries(fields)

        if attack < 10 or attack == 606 or attack == 94:
            print searchQueries

        for queryType, query in searchQueries.items():
            # enter each search term in db separately
            numTweets, avgRetweets, avgFavorites = searchTwitter(query)
            addToDB(queryType, query, numTweets, avgRetweets, avgFavorites)


        # # tweetCriteria = got.manager.TweetCriteria().setQuerySearch(fields['searchTerms'])#.setSince(startQueryDate).setUntil(endQueryDate).setMaxTweets(100)
        # tweetCriteria = got.manager.TweetCriteria().setQuerySearch(fields['searchTerms']).setSince(startQueryDate).setUntil(endQueryDate).setMaxTweets(56)
        # tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        #
        # # print tweets
        #
        # numTweets = len(tweets)
        # avgRetweets = getAvgRetweets(tweets)
        #
        # print 'number of tweets: '+str(numTweets)
        # print 'avg retweets: ' + str(avgRetweets)
        #
        # #delay for twitter
        # time.sleep(10)
        #
        # insert_sql = (
        #     "INSERT INTO tweet_metrics (search_terms, attack_id, tweet_count, avg_retweets, start_date, end_date) "
        #     "VALUES (?, ?, ?, ?, ?, ?)"
        # )
        # data = (fields['searchTerms'], attack, numTweets, avgRetweets, startQueryDate, endQueryDate)
        # try:
        #     dbcursor.execute(insert_sql, data)
        #     db.commit()
        # except sqlite3.Error as e:
        #     print "Tweet Metrics Not Saved: ", e.args[0]


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
