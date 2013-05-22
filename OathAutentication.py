import tweepy

#Username: CTAIProj
#Password: iridia
#Project name: infoh512proj

#Useful links:
#    http://140dev.com/twitter-api-programming-tutorials/aggregating-tweets-search-api-vs-streaming-api/
#    https://dev.twitter.com/discussions/10783

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.


# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="7lkdFGeJDLMxOBUsF81zPw"
consumer_secret="bxipD9ypPYAngBSWIRtDV2tUUGevqhHLWiwMdV0lQ9I"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="1363054009-4Tpq2Fn4gMw1nojR0Zcm3QczAU4n2f2v6Qy1Fhg"
access_token_secret="xZocT9WiJY7Bw7BSF4R0Ua4djfCLBK6PkapIdA"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print api.me().name

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
#api.update_status('Do not forget the password again!')

# Prompt the name of the user to search
stringUser = raw_input("Insert the username you want to find: ")
# Get user name and display some information
twitterUser = api.get_user(stringUser)
if(twitterUser is None):
    print("User " + stringUser +" not found!")
else:
    print("User " + stringUser + " found:")
    print(twitterUser)
    #print("Screen name:",twitterUser.screen_name)
    #print("Location:",twitterUser.location)
    #print("Time zone:",twitterUser.time_zone)
    #print("Url",twitterUser.url)
