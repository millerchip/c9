#! /usr/bin/python3

# set debug flag to True, to run the program but not actually create the tweet
debug = False


# https://stackoverflow.com/questions/3878555/how-to-replace-repeated-instances-of-a-character-with-a-single-instance-of-that
# https://docs.python.org/3/library/re.html#re.sub
# for getting rid of duplicate characters (specifically, spaces)
import re

# Might need this to parse the response from the valspeak API
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

# FIND FIRST TWEET NOT OF ZERO LENGTH (ITERATE THROUGH LAST 20, SO CURRENTLY WILL FAIL IT NO TWEET IS NON-ZERO LENGTH)
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

# TODO change 5 back to 0
for i in range (5,return_count):
    # iterate through all returned values
    # for key in status.keys():
    #    print (str(key) + '->' + str(status[key]))
    status = statuses[i]
    original_tweet = status["full_text"]
    tweet_length = status["display_text_range"][1]
    if tweet_length > 0:
        break

# Print just the full text
if debug:
    print("tweet = " + original_tweet)
    print("length = " + str(tweet_length))

# Convert the tweet into valspeak, using public API at https://funtranslations.com/api/valspeak
# Parse response from resultant JSON, and extract translation into variable 'valspeak_tweet'

# Call API, but need to convert text
# https://api.funtranslations.com/translate/valspeak.json?text=Good%20Morning.%20Come%20on%20man%2C%20just%20saying%21

# https://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python
# https://docs.python.org/3/library/urllib.html#urllib.quote
from urllib.parse import quote
encoded_tweet = quote(original_tweet, safe='')

print(encoded_tweet)

# exit()

# Now call the API
# https://www.geeksforgeeks.org/get-post-requests-using-python/

# importing the requests library 
import requests 

# api-endpoint 
URL = "https://api.funtranslations.com/translate/valspeak.json"

# defining a params dict for the parameters to be sent to the API 
PARAMS = {'text':encoded_tweet} 

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 

# extracting data in json format 
data = r.json() 

print(data)

# from https://funtranslations.com/api/valspeak, this is definitely the right field, but what I'm currently getting back from the API doesn't look like it's being parsed. However, I only get 5 API calls an hour on the free account, so will have to test slowly! :o/
# TODO should also check data['success']['total'], which should be 1 (numeric value)
valspeak_tweet = data['contents']['translated']
print("\nhere\n")
print(valspeak_tweet)

exit()

print(data)

exit()

# Original tweet: I hope we can get Admiral @RonnyJackson4TX of Texas, who served our Country so well, into the runoff election in #TX13! Ronny is strong on Crime and Borders, GREAT for our Military and Vets, and will protect your #2A. Get out and vote for Ronny on Tuesday, March 3rd!

# Valspeak returned value: I%20hope%20we%20can%20get%20Admiral%20%40RonnyJackson4TX%20of%20Texas%2C%20who%20served%20our%20Country%20so%20well%2C%20into%20the%20runoff%20election%20in%20%23TX13%21%20Ronny%20is%20strong%20on%20Crime%20and%20Borders%2C%20GREAT%20for%20our%20Military%20and%20Vets%2C%20and%20will%20protect%20your%20%232A.%20Get%20out%20and%20vote%20for%20Ronny%20on%20Tuesday%2C%20March%203rd%21


# API returned this value:
{'success': {'total': 1}, 'contents': {'translated': 'I%20hope%20we%20can%20get%20Admiral%20%40RonnyJackson4TX%20of%20Texas%2C%20who%20served%20our%20Country%20so%20well%2C%20into%20the%20runoff%20election%20in%20%23TX13%21%20Ronny%20is%20strong%20on%20Crime%20and%20Borders%2C%20GREAT%20for%20our%20Military%20and%20Vets%2C%20and%20will%20protect%20your%20%232A.%20Get%20out%20and%20vote%20for%20Ronny%20on%20Tuesday%2C%20March%203rd%21', 'text': 'I%20hope%20we%20can%20get%20Admiral%20%40RonnyJackson4TX%20of%20Texas%2C%20who%20served%20our%20Country%20so%20well%2C%20into%20the%20runoff%20election%20in%20%23TX13%21%20Ronny%20is%20strong%20on%20Crime%20and%20Borders%2C%20GREAT%20for%20our%20Military%20and%20Vets%2C%20and%20will%20protect%20your%20%232A.%20Get%20out%20and%20vote%20for%20Ronny%20on%20Tuesday%2C%20March%203rd%21', 'translation': 'valspeak'}}


# Testing
# original_tweet = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including and then"


valspeak_tweet = "Lorem Ipsum is simply dummy text of thuh printin' and typesettin' industry. Lorem Ipsum has been thuh industry's standard dummy text ever since thuh 1500s, mostly when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, like, wow but also thuh leap into electronic typesettin', mostly remainin' essentially unchanged. It was like, ya know, popularised in thuh 1960s with thuh release of Letraset sheets containin' Lorem Ipsum passages, like, wow and more recently with desktop publishin' software like Aldus PageMaker includin' and then" 


# ... and now tweet, breaking into separate tweets if necessary
# this code first used for PlatBot, which was parsing a v.short blog post, and hence could result in multiple tweets. 
# In practice, translating to valspeak will only fractionally lengthen a tweet, so could update this to handle the fact that there would be at most
# 2 tweets... but why bother, this works.
if (len(valspeak_tweet)>1): 
    # it's a non-trivial length string
    if len(valspeak_tweet) > 280:
        # break into segments
        i = 1
        while True:
            # Assume update will not require more than 9 tweets, hence len(str(i)) = 1
            if len(valspeak_tweet) > 277:
                # truncate at a word boundary (ie, not part-way through a word)
                last_space = valspeak_tweet[0:276].rfind(" ")
                twt = str(i) + "/ " + valspeak_tweet[0:last_space]
                valspeak_tweet = valspeak_tweet[(last_space+1):]
            else:
                twt = str(i) + "/ " + valspeak_tweet
                valspeak_tweet = ""
            i += 1
            print ("Tweet will be this: " + twt)
            if (not debug):
                # api.update_status (twt)
                print("*** tweet created")
            else:
                print("*** debug mode -- tweet not created")
            if len(valspeak_tweet) < 1:
                break
    else:
        print ("Tweet will be this: " + valspeak_tweet)
        if (not debug):
            # api.update_status (valspeak_tweet)
            print("*** tweet created")
        else:
            print("*** debug mode -- tweet not created")



