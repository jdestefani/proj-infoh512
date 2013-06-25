__authors__ = 'Jacopo De Stefani (jacopo.de.stefani@ulb.ac.be)\n    Nadine Khouzam (nadine.khouzam@ulb.ac.be)\n'


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from time import localtime, strftime
import json
import pprint
import sys
import re
import unicodedata

LANG = "en"


def main():

    print '''
    ###########################################################################
    #                            StreamFetcher 1.0                            #
    ###########################################################################
    '''

    if len(sys.argv) == 1:
        usage()
        sys.exit(2)


    consumer_key = "XVTXB2htK3FijPZ8w5g2cQ"
    consumer_secret = "V439XDFqiiVFAECLuiH0zElMcFurlBDRAFPcAPMpbs"
    access_token = "1525178712-nDcycRs7XqNHoHIMI9JhS14OsDF8ErLfG0wbNGX"
    access_token_secret = "jYNsqWN0pN0EulJUIGdhwxxtd0U3rHiKnZaFogEr6Y"

    l = FileListener(100,10000)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=["#CocaCola","Coca","cola","#Coke","Coca cola"],languages=["en"])
    #stream.filter(track=sys.argv[1:],languages=["en"])

class FileListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self,flush_threshold,max_flushes):
        self.JSONDataList = []
        self.FLUSH_THRESHOLD = flush_threshold
        self.flush_counter = 0
        self.max_flushes = max_flushes
        try:
            basicFilename = "Stream" + strftime("%d-%m-%Y %H:%M:%S", localtime())
            self.timesFile = open(str(basicFilename) + ".times", "w+")
            self.tweetsFile = open(str(basicFilename) + ".tweets", "w+")
            self.filteredTweetsFile = open(str(basicFilename) + ".filtered", "w+")
            self.hashtagsFile = open(str(basicFilename) + ".ht", "w+")
            print ("[STATUS] - File " + str(basicFilename+".tweets") + " opened\n ")
            print ("[STATUS] - File " + str(basicFilename+".filtered") + " opened\n ")
            print ("[STATUS] - File " + str(basicFilename+".times") + " opened\n ")
            print ("[STATUS] - File " + str(basicFilename+".ht") + " opened \n ")

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
                for hashtag in relevantInformations[u'hashtags']:
                    self.hashtagsFile.write(hashtag.encode('utf8')+"\t")
                self.hashtagsFile.write("\n")
            del self.JSONDataList[0:len(self.JSONDataList)]
            print ("[STATUS] - Ended flushing at " + strftime("%d-%m-%Y %H:%M:%S", gmtime()))
            self.flush_counter = self.flush_counter + 1

        if self.flush_counter > self.max_flushes:
            return False


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
        relevantInformations[u'created_at'] = JSONData[u'created_at']

        return relevantInformations

def usage():
    USAGE = '''Usage: StreamFetcher [QUERIES]

    This script is a command-line interface to the twitter Streaming API.
    The values passed as queries are composed using the OR operator to build the final query.
    The characters # must be escaped.

    This is free software, and you are welcome to redistribute it under certain conditions.
    See the GNU General Public License for details.
    There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    AUTHORS:
    '''
    print(USAGE+__authors__)



if __name__ == '__main__':
    main()
