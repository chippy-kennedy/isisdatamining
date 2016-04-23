#https://github.com/Jefferson-Henrique/GetOldTweets-python
import got

import re, sys
import sqlite3
import datetime, time

def printTweet(descr, t):
    print descr
    print "Username: %s" % t.username
    print "Retweets: %d" % t.retweets
    print "Text: %s" % t.text
    print "Mentions: %s" % t.mentions
    print "Hashtags: %s\n" % t.hashtags


def getFields(cursor, attackID):
    cursor.execute('SELECT start_date, end_date, type, primary_location, perpetrator FROM attacks WHERE attack_id = ?;', (attackID,))
    allTerms = list(cursor.fetchone())

    startDate       = allTerms[0]
    endDate         = allTerms[1]
    attackType      = str(allTerms[2])
    attackLocation  = str(allTerms[3])
    perpetrator     = str(allTerms[4])

    fields = {
        'startDate': startDate,
        'endDate': endDate,
        'attackType': attackType,
        'attackLocation': attackLocation,
        'perpetrator': perpetrator,
    }

    return fields

# given a list of tweets
# returns the paring avgRetweets, avgFavorites
def getSharingAverages(tweets):
    numTweets = len(tweets)
    if numTweets <= 0:
        return None,  None

    # Pop pulls off first tweet so it doesn't affect average
    firstTweet = tweets.pop(0)
    totalRetweets = firstTweet.retweets
    totalFavorites = firstTweet.favorites

    for tweet in tweets:
        totalRetweets += tweet.retweets
        totalFavorites += tweet.favorites

    avgRetweets = totalRetweets/numTweets
    avgFavorites = totalFavorites/numTweets

    return avgRetweets, avgFavorites

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
def searchTwitter(query, startQueryDate, endQueryDate):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(startQueryDate).setUntil(endQueryDate).setMaxTweets(56)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    numTweets = len(tweets)
    avgRetweets, avgFavorites = getSharingAverages(tweets)

    return numTweets, avgRetweets, avgFavorites

# adds the given information to the twitter_metrics db
# returns if the addition was successful
def addToDB(conn, c, metricID, attackID, queryType, query, numTweets, avgRetweets, avgFavorites, startQueryDate, endQueryDate):
    insert_sql = (
        """INSERT INTO twitter_metrics (metric_id, attack_id, query_type, query, number_of_tweets, avg_retweets, avg_favorites, query_start, query_end)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    )

    data = (metricID, attackID, queryType, query, numTweets, avgRetweets, avgFavorites, startQueryDate, endQueryDate)

    try:
        c.execute(insert_sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print "Tweet Metrics Not Saved: ", e.args[0]
        return False
    return True

def insertMetrics(conn, c, attackID):
    #run intended twitter query with got lib
    fields = getFields(c,attackID)

    start_date = datetime.datetime.strptime(fields['startDate'], "%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.strptime(fields['endDate'], "%Y-%m-%d %H:%M:%S")
    startQueryDate = start_date.strftime('%Y-%m-%d')
    endQueryDate = (end_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    searchQueries = getSearchQueries(fields)

    queryCount = 1
    for queryType, query in searchQueries.items():
        # generate a unique id based on which search query it is
        # within the current attack
        metricID = (attackID-1)*len(searchQueries)+queryCount
        queryCount+=1
        print metricID

        # enter each search term in db separately
        numTweets, avgRetweets, avgFavorites = searchTwitter(query, startQueryDate, endQueryDate)

        addToDB(conn, c, metricID, attackID, queryType, query, numTweets, avgRetweets, avgFavorites, startQueryDate, endQueryDate)


def main():
    conn = sqlite3.connect('attacks.db')
    conn.text_factory = str
    c = conn.cursor()

    c.execute("SELECT attack_id from attacks")
    attackids = c.fetchall()

    for attack in attackids:
        attackID = attack[0]
        insertMetrics(conn, c, attackID)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
