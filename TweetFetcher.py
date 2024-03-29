__authors__ = 'Jacopo De Stefani (jacopo.de.stefani@ulb.ac.be)\n    Nadine Khouzam (nadine.khouzam@ulb.ac.be)\n'

import getopt
import sys
import tweepy
#import TweetGatherer
import unicodedata
import time
import re
#import pprint

#Username: oject_
#Password: iridia
#Project name: infoh512proj

#Useful links:
#    http://140dev.com/twitter-api-programming-tutorials/aggregating-tweets-search-api-vs-streaming-api/
#    https://dev.twitter.com/discussions/10783

COUNT = 200
LANG = "en"
INCLUDE_RTS = False
TRIM_USER = True
INCLUDE_ENTITIES = True
EXCLUDE_REPLIES = True
PAGES = 30
USERNAME = "oject_"

def main():
    searchQuery = None
    screenName = None
    global _verbose
    _verbose = 1

    print '''
    ###########################################################################
    #                            TweetFetcher 1.0                             #
    ###########################################################################
    '''

    try:
        shortflags = 'hs:u:q'
        longflags = ["help", "search_query" ,"user_timeline","quiet"]
        #longflags = ['help', 'consumer-key=', 'consumer-secret=',
                 #'access-key=', 'access-secret=', 'encoding=']
        opts, args = getopt.gnu_getopt(sys.argv[1:], shortflags, longflags)
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-q':
            _verbose = 0
        elif opt in ("-s", "--search_query"):
            searchQuery = arg
        elif opt in ("-u", "--user_timeline"):
            screenName = arg

    if screenName is None and searchQuery is None:
        sys.stderr.write("\n[ERROR] - No search mode chosen!\n\n")
        usage()
        sys.exit(2)

    if screenName is not None and searchQuery is not None:
        sys.stderr.write("\n[ERROR] - Multiple search mode chosen!\n\n")
        usage()
        sys.exit(2)

    # First perform the twitter authentication
    consumer_key = "XVTXB2htK3FijPZ8w5g2cQ"
    consumer_secret = "V439XDFqiiVFAECLuiH0zElMcFurlBDRAFPcAPMpbs"
    access_token = "1525178712-nDcycRs7XqNHoHIMI9JhS14OsDF8ErLfG0wbNGX"
    access_token_secret = "jYNsqWN0pN0EulJUIGdhwxxtd0U3rHiKnZaFogEr6Y"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterAPI = tweepy.API(auth)

    if auth.get_username() == USERNAME:
        print ("[STATUS] - Authentication successful as " + auth.get_username() + "!\n")
        displayRateLimits(twitterAPI.rate_limit_status())
    else:
        sys.stderr.write("[STATUS] - Authentication failed!\n")
        sys.exit(2)

    if screenName is not None and searchQuery is None:
        filenameTweets = str(screenName + ".tweets")
        filenameFiltered = str(screenName + ".filtered")
        filenameHashtags = str(screenName + ".ht")

    if screenName is None and searchQuery is not None:
        filenameTweets = str(searchQuery + ".tweets")
        filenameFiltered = str(searchQuery + ".filtered")
        filenameHashtags = str(searchQuery + ".ht")
    try:
        tweetsFile = open(filenameTweets, "w+")
        filteredTweetsFile = open(filenameFiltered, "w+")
        hashtagsFile = open(filenameHashtags, "w+")
    except IOError as e:
        sys.stderr.write(e)
        sys.stderr.write("\n[ERROR] - Error in opening files!")
        sys.exit(2)


    statusList = []
    i = 1

    if screenName is not None and searchQuery is None:
        if _verbose == 1:
            print ("[STATUS] - Fetching tweets for user " + screenName + " with options:\n")
            print("\tInclude Retweets = " + str(INCLUDE_RTS))
            print("\tTrim User = " + str(TRIM_USER))
            print("\tInclude Entities = " + str(INCLUDE_ENTITIES))
            print("\tExclude Replies = " + str(EXCLUDE_REPLIES))
            print("\tCount = " + str(COUNT) + " \n")

        for page in tweepy.Cursor(twitterAPI.user_timeline, screen_name=screenName, count=COUNT,include_rts=INCLUDE_RTS, trim_user=TRIM_USER,include_entities=INCLUDE_ENTITIES, exclude_replies=EXCLUDE_REPLIES).pages(PAGES):
            for status in page:
                statusList.append(status)
            if _verbose == 1:
                print ("[STATUS] - Fetched page " + str(i) + " out of " + str(PAGES) + "\n")
            i = i + 1

    if screenName is None and searchQuery is not None:
        if _verbose == 1:
            print ("[STATUS] - Fetching tweets for matching query " + searchQuery + " with options:\n")
            print("\tInclude Retweets = " + str(INCLUDE_RTS))
            print("\tLanguage = " + LANG)
            print("\tInclude Entities = " + str(INCLUDE_ENTITIES))
            print("\tCount = " + str(COUNT) + " \n")

        for page in tweepy.Cursor(twitterAPI.search, q=searchQuery, lang=LANG, include_entities=INCLUDE_ENTITIES, count=COUNT).pages(PAGES):
            for status in page:
                statusList.append(status)
            if _verbose == 1:
                print ("[STATUS] - Fetched page " + str(i) + " out of " + str(PAGES) + "\n")
            i = i + 1

    if _verbose == 1:
        print ("[STATUS] - Starting tweet filtering")

    #Tweet filtering
    for status in statusList:
        relevantInformations = filterTweet(status)
        #splitRelevantIrrelevant(relevantInformations[u'filtered_text'])
        tweetsFile.write(relevantInformations[u'text'] + "\n")
        filteredTweetsFile.write(relevantInformations[u'filtered_text'] + "\n")
        for hashtag in relevantInformations[u'hashtags']:
            hashtagsFile.write(unicodedata.normalize('NFKD',hashtag).encode("ascii",'ignore')+"\t")
        hashtagsFile.write("\n")

    if _verbose == 1:
        print ("[STATUS] - Completed tweet filtering")

    tweetsFile.close()
    filteredTweetsFile.close()

    ## If the authentication was successful, you should
    ## see the name of the account print out
    ##apiResponse = api.me().name

    ##print api.getUser("")


def usage():
    USAGE = '''Usage: TweetFetcher [PARAMETERS] -s [SEARCH_QUERY] | -u [SCREEN_NAME]

  This script is a command-line interface to the twitter Search REST API.

  Options:

    -h --help : print this help
    -q,--quiet: Non verbose output mode"

  Required options (mutually exclusive):
    -s,--search_query: Search query to be passed to the Search API to retrieve tweets.
    -u,--user_timeline:  Screen name of the user for which the tweets should be retrieved.

    This is free software, and you are welcome to redistribute it under certain conditions.
    See the GNU General Public License for details.
    There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    AUTHORS:
    '''
    print(USAGE+__authors__)


def filterTweet(status):
    partsToRemove = []
    hashtags = []
    relevantInformations = {}

    #if len((status.entities)[u'hashtags']) > 0:
        #for hashtag in ((status.entities)[u'hashtags']):
            #partsToRemove.append(hashtag[u'indices'][0])
            #partsToRemove.append(hashtag[u'indices'][1])
            #hashtags.append(hashtag[u'text'])

    if len((status.entities)[u'urls']) > 0:
        for url in ((status.entities)[u'urls']):
            partsToRemove.append(url[u'indices'][0])
            partsToRemove.append(url[u'indices'][1])

    #if len((status.entities)[u'user_mentions']) > 0:
        #for user in ((status.entities)[u'user_mentions']):
            #partsToRemove.append(user[u'indices'][0])
            #partsToRemove.append(user[u'indices'][1])

    # Clean the tweet content.
    text = status.text

    partsToRemove.append(0)
    partsToRemove.append(len(text))
    partsToRemove = sorted(partsToRemove)

    filteredText = ""

    # Remove the unnecessary elements
    for i in range(len(partsToRemove) / 2):
        filteredText += text[partsToRemove[2 * i]:partsToRemove[2 * i + 1]]

    # Clean the tweet content.
    text = text.replace(u'\xa0', u'')
    text = text.replace(u'&amp', u'')
    text = text.replace(u'w/', u'with')
    text = text.replace(u'#',u' #')
    text = text.replace(u'@',u' @')
    filteredText = filteredText.replace(u'\xa0', u'')
    filteredText = filteredText.replace(u'&amp', u'')
    filteredText = filteredText.replace(u'w/', u'with')
    filteredText = filteredText.replace(u'#',u' #')
    filteredText = filteredText.replace(u'@',u' @')

    text = unicodedata.normalize('NFKD',text).encode("ascii",'ignore')
    filteredText = unicodedata.normalize('NFKD',filteredText).encode("ascii",'ignore')

    text = re.sub(r'\^[A-Z]+', r'', text)
    filteredText = re.sub(r'\^[A-Z]+', r'', filteredText)

    # Build the object to be returned
    relevantInformations[u'text'] = text
    relevantInformations[u'filtered_text'] = filteredText
    relevantInformations[u'hashtags'] = hashtags
    relevantInformations[u'created_at'] = status.created_at

    return relevantInformations

def displayRateLimits(JSONReponse):
    print("[LIMITS] - 15 minutes time windows\n")
    userTimelineLimits = JSONReponse["resources"]["statuses"]["/statuses/user_timeline"]
    print("[LIMITS] - [User Timeline]")
    print("\tRemaining requests: " + str(userTimelineLimits["remaining"]))
    print("\tReset at " + time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(userTimelineLimits["reset"])) + "\n")

    searchLimits = JSONReponse["resources"]["search"]["/search/tweets"]
    print("[LIMITS] - [Search]")
    print("\tRemaining requests: " + str(searchLimits["remaining"]))
    print("\tReset at " + time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(searchLimits["reset"])) + "\n")
    return


if __name__ == "__main__":
    main()
