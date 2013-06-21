from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import Status
from time import gmtime, strftime
import json
import pprint
import sys
import argparse

LANG = "en"


def main():

    parser = argparse.ArgumentParser(description='Retrieves the tweets matching the queries passed as parameters using Streaming API.')
    parser.add_argument('queries', metavar='queries', type=str, nargs='+',
                         help='Queries to pass to the streaming API')
    searchQuery = parser.parse_args()

    print '''
    ###########################################################################
    #                            StreamFetcher 1.0                            #
    ###########################################################################
    '''

    consumer_key = "XVTXB2htK3FijPZ8w5g2cQ"
    consumer_secret = "V439XDFqiiVFAECLuiH0zElMcFurlBDRAFPcAPMpbs"
    access_token = "1525178712-nDcycRs7XqNHoHIMI9JhS14OsDF8ErLfG0wbNGX"
    access_token_secret = "jYNsqWN0pN0EulJUIGdhwxxtd0U3rHiKnZaFogEr6Y"

    l = FileListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=["Nba, Finals,#Heat,#Spurs,#LBJ"],languages=["en"])
    #stream.filter(track=["Windows8,#Windows8,Surface"])

class FileListener(StreamListener):
    FLUSH_THRESHOLD = 1000
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self):
        self.JSONDataList = []
        try:
            basicFilename = "Stream"+ strftime("%d-%m-%Y %H:%M:%S", gmtime())
            self.timesFile = open(str(basicFilename) + ".times", "w+")
            self.tweetsFile = open(str(basicFilename) + ".tweets", "w+")
            self.filteredTweetsFile = open(str(basicFilename) + ".filtered", "w+")
        except IOError as e:
            sys.stderr.write(e)
            sys.stderr.write("\n[ERROR] - Error in opening files!")
            sys.exit(2)


    def on_connect(self):
        """Called once connected to streaming server.

        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        print "[STATUS] - Connected!"

    def on_data(self, data):
        """Called when raw data is received from connection.
        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """

        if len(self.JSONDataList) > self.FLUSH_THRESHOLD:
            print ("[STATUS] - Started flushing at " + strftime("%d-%m-%Y %H:%M:%S", gmtime()))
            for element in self.JSONDataList:
                relevantInformations = self.extractTweet(element)
                self.timesFile.write(relevantInformations[u'created_at'].encode("utf8") + "\n")
                self.tweetsFile.write(relevantInformations[u'text'].encode("utf8") + "\n")
                self.filteredTweetsFile.write(relevantInformations[u'filtered_text'].encode("utf8") + "\n")
            del self.JSONDataList[0:len(self.JSONDataList)]
            print ("[STATUS] - Ended flushing at " + strftime("%d-%m-%Y %H:%M:%S", gmtime()))

        if 'in_reply_to_status_id' in data:
            #status = Status.parse(self.api, json.loads(data))
            if self.on_status(json.loads(data)) is False:
                print "[STATUS] - Connected closed!"
                return False
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                print "[STATUS] - Connected closed!"
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                print "[STATUS] - Connected closed!"
                return False
        else:
            print data

    def on_status(self, JSONData):
        self.JSONDataList.append(JSONData)
        return True

    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status"""
        return

    def on_limit(self, track):
        """Called when a limitation notice arrvies"""
        sys.stderr.write("[LIMIT] - Limitation notice received:" + str(track) + "\n")
        return

    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        sys.stderr.write("[ERROR] - Status code received : "+str(status_code)+"\n")
        return False

    def on_timeout(self):
        """Called when stream connection times out"""
        sys.stderr.write("[ERROR] - Connection timed out at " + strftime("%d-%m-%Y %H:%M:%S", gmtime()) +"\n")
        return

    def extractTweet(self,JSONData):
        partsToRemove = []
        hashtags = []
        relevantInformations = {}

        if len((JSONData[u'entities'])[u'hashtags']) > 0:
            for hashtag in ((JSONData[u'entities'])[u'hashtags']):
                partsToRemove.append(hashtag[u'indices'][0])
                partsToRemove.append(hashtag[u'indices'][1])
                hashtags.append(hashtag[u'text'])

        if len((JSONData[u'entities'])[u'urls']) > 0:
            for url in ((JSONData[u'entities'])[u'urls']):
                partsToRemove.append(url[u'indices'][0])
                partsToRemove.append(url[u'indices'][1])

        if len((JSONData[u'entities'])[u'user_mentions']) > 0:
            for user in ((JSONData[u'entities'])[u'user_mentions']):
                partsToRemove.append(user[u'indices'][0])
                partsToRemove.append(user[u'indices'][1])

        # Clean the tweet content.
        text = JSONData[u'text']
        text = text.replace(u'^MP', u'')

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
        filteredText = filteredText.replace(u'\xa0', u'')
        filteredText = filteredText.replace(u'&amp', u'')

        # Build the object to be returned
        relevantInformations[u'text'] = text
        relevantInformations[u'filtered_text'] = filteredText
        relevantInformations[u'hashtags'] = hashtags
        relevantInformations[u'created_at'] = JSONData[u'created_at']

        return relevantInformations



if __name__ == '__main__':
    main()
