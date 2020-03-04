#! /usr/bin/python3

# set debug flag to True, to run the program but not actually create the tweet
debug = True

# https://stackoverflow.com/questions/3878555/how-to-replace-repeated-instances-of-a-character-with-a-single-instance-of-that
# https://docs.python.org/3/library/re.html#re.sub
# for getting rid of duplicate characters (specifically, spaces)
import re

# Might need this to parse the response from the conversion API
import json

# https://medium.freecodecamp.org/creating-a-twitter-bot-in-python-with-tweepy-ac524157a607
import tweepy

# TODO if I ever make a Twitter bot out of this, I should create new credentials specifically for the new bot
# My twitter account credentials (https://twitter.com/BotPlat)
from twitter_credentials import *

# Set up for API calls
# stuff copied from the internet to set things up
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
user = api.me()

# FIND FIRST TWEET NOT OF ZERO LENGTH (ITERATE THROUGH AT MOST THE LAST 20, SO CURRENTLY WILL FAIL IT NO TWEET IS NON-ZERO LENGTH)
# https://twitter.com/realDonaldTrump
# From https://stackoverflow.com/questions/27900451/convert-tweepy-status-object-into-json
# OTHER SITES, MIGHT BE USEFUL FUTURE REFERENCES
# https://blog.f-secure.com/how-to-get-tweets-from-a-twitter-account-using-python-and-tweepy/
# https://towardsdatascience.com/how-to-access-twitters-api-using-tweepy-5a13a206683b
# https://www.geeksforgeeks.org/extraction-of-tweets-using-tweepy/
# http://docs.tweepy.org/en/v3.8.0/api.html
# text being truncated -- https://github.com/tweepy/tweepy/issues/935

return_count = 20
statuses = api.user_timeline(screen_name="realDonaldTrump", tweet_mode="extended", count=return_count)

for i in range (0,return_count):
    # iterate through all returned values
    # for key in status.keys():
    #    print (str(key) + '->' + str(status[key]))
    status = statuses[i]
    original_tweet = status["full_text"]
    tweet_length = status["display_text_range"][1]
    if tweet_length > 0:
        break

# Print the full text
if debug:
    print("tweet = " + original_tweet)
    print("length = " + str(tweet_length))

# Convert the tweet using public API at https://api.funtranslations.com/
# Parse response from resultant JSON, and extract translation into variable 'converted_tweet'

# Call API, but need to encode the text
# https://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python
# https://docs.python.org/3/library/urllib.html#urllib.quote
from urllib.parse import quote
from urllib.parse import unquote

encoded_tweet = quote(original_tweet, safe='')

# Now call the API
# https://www.geeksforgeeks.org/get-post-requests-using-python/

# importing the requests library 
import requests 

# api-endpoint 
# https://api.funtranslations.com/
# I tried several APIs, but many don't work well with short and grammatically challenging tweets. However, this one does:
URL = "https://api.funtranslations.com/translate/gungan.json"

# defining a params dict for the parameters to be sent to the API 
PARAMS = {'text':encoded_tweet} 

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 

# extracting data in json format 
data = r.json()

print("\ndata:")
print(data)

# I only get 5 API calls an hour on the free account, so will have to test slowly! :o/
# TODO should also check data['success']['total'], which should be 1 (numeric value)
converted_tweet = unquote(data['contents']['translated'])

print("\nConverted tweet = " + converted_tweet)

exit()

# Testing
# original_tweet = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including and then"


converted_tweet = "Lorem ipsum is simply dummy text of dha print and typesett industry. Lorem ipsum has been dha industry's standard dummy text ever since dha 1500s, when an unknown printer took a galley of type and scrambled it to maken a type specimen book. It has survived not only fife centuries, but also dha leap into electronic typesett, remain essentially unchanged. It was popularised in dha 1960s with dha release of letraset sheets contain lorem ipsum passages, and more recently with desktop publish software like aldus pagemaker includ and then" 


# ... and now tweet, breaking into separate tweets if necessary
# this code first used for PlatBot, which was parsing a v.short blog post, and hence could result in multiple tweets. 
# In practice, translation will only fractionally lengthen a tweet, so could update this to handle the fact that there would be at most
# 2 tweets... but why bother, this works.
if (len(converted_tweet)>1): 
    # it's a non-trivial length string
    if len(converted_tweet) > 280:
        # break into segments
        i = 1
        while True:
            # Assume update will not require more than 9 tweets, hence len(str(i)) = 1
            if len(converted_tweet) > 277:
                # truncate at a word boundary (ie, not part-way through a word)
                last_space = converted_tweet[0:276].rfind(" ")
                twt = str(i) + "/ " + converted_tweet[0:last_space]
                converted_tweet = converted_tweet[(last_space+1):]
            else:
                twt = str(i) + "/ " + converted_tweet
                converted_tweet = ""
            i += 1
            print ("Tweet will be this: " + twt)
            if (not debug):
                # api.update_status (twt)
                print("*** tweet created")
            else:
                print("*** debug mode -- tweet not created")
            if len(converted_tweet) < 1:
                break
    else:
        print ("Tweet will be this: " + converted_tweet)
        if (not debug):
            # api.update_status (converted_tweet)
            print("*** tweet created")
        else:
            print("*** debug mode -- tweet not created")



