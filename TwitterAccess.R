library("twitteR")
#Username: oject_
#Password: iridia
#Project name: infoh512proj

#Useful links:
#    http://140dev.com/twitter-api-programming-tutorials/aggregating-tweets-search-api-vs-streaming-api/
#    https://dev.twitter.com/discussions/10783

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

requestURL <- "https://api.twitter.com/oauth/request_token"
accessURL <- "http://api.twitter.com/oauth/access_token"
authURL <- "http://api.twitter.com/oauth/authorize"

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")

consumer_key="XVTXB2htK3FijPZ8w5g2cQ"
consumer_secret="V439XDFqiiVFAECLuiH0zElMcFurlBDRAFPcAPMpbs"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="1525178712-nDcycRs7XqNHoHIMI9JhS14OsDF8ErLfG0wbNGX"
access_token_secret="jYNsqWN0pN0EulJUIGdhwxxtd0U3rHiKnZaFogEr6Y"

cred <- OAuthFactory$new(consumerKey=consumer_key,
                         consumerSecret=consumer_secret,
                         requestURL=requestURL,
                         accessURL=accessURL,
                         authURL=authURL)
cred$handshake()
#At this point, you’ll be prompted with another URL, go to that URL with
#your browser and you’ll be asked to approve the connection for this application.
#Once you do this, you’ll be presented with a PIN, enter that into your R session.
#Your object is now veriﬁed.
#Lastly, to use that credential object within an R session, use the registerTwitterOAuth function. Passing your OAuth object to that function will cause
#all of the API calls to go through Twitter’s OAuth mechanism instead of the
#standard URLs:
registerTwitterOAuth(cred)
#=== End Authentication ===

# Getting an user
# user <- getUser('<username>')

# Searching all the tweets according to some criteria
# tweets <- twitterSearch('<query>', n = 'Number of results')

# Converting tweet list to dataframe
# df <- twListToDF(publicTweets)

# EXAMPLES
#Jeﬀrey Breen’s sentiment analysis example: http://www.inside-r.org/howto/mining-twitter-airline-consumer-sentiment
#Mapping your followers: http://simplystatistics.org/2011/12/21/an-r-function-to-map-your-twitter-followers/
#Yangchao Zhao’s book on data mining w/ R http://www.amazon.com/Data-Mining-Examples-Case-Studies/dp/0123969638
#Gary Miner et al’s book on data mining http://www.amazon.com/Practical-Statistical-Analysis-Non-structured-Applications/dp/012386979X
#Mining Twitter with R https://sites.google.com/site/miningtwitter/home
#Organization or conversation in Twitter: A case study of chatterboxing - https://www.asis.org/asist2012/proceedings/Submissions/185.pdf