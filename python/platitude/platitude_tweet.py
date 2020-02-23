#! /usr/bin/python3

# set debug flag to True, to run the program but not actually create the tweet
debug = True

# https://www.pythonforbeginners.com/feedparser/using-feedparser-in-python
import feedparser

# https://medium.freecodecamp.org/creating-a-twitter-bot-in-python-with-tweepy-ac524157a607
import tweepy

# https://pypi.org/project/html2text/
import html2text

# https://stackoverflow.com/questions/3878555/how-to-replace-repeated-instances-of-a-character-with-a-single-instance-of-that
# https://docs.python.org/3/library/re.html#re.sub
# for getting rid of duplicate characters (specifically, spaces)
import re

# My twitter account credentials (https://twitter.com/BotPlat)
from twitter_credentials import *


# stuff copied from the internet to set things up
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
user = api.me()

# Now construct the tweet, from the RSS feed
d = feedparser.parse("http://platitudes.home.blog/feed/")

# Retrieve text from the RSS feed, for the i-th entry in the feed
def retrieve_text(i):
    longentry = d['entries'][i]['description']
    # At one stage I was truncating the mp3 file link, but the posts are too ill-structured to do this, 
    # and in any way I was doing it to keep the message short, but I'm not doing multiple tweets if needed
    # match = longentry.rfind('<a href="/mp3')
    '''
    match = len(longentry)
    if match != -1:
        longentry = longentry[0:match]
    match = longentry.rfind('<a href="https://www.bbc.co.uk/radio/play')
    if match != -1:
        longentry = longentry[0:match]
    '''
    shortstring = longentry
    # Turn URLs into something that will work
    shortstring = shortstring.replace('href="/mp3','href="http://www.platitudes.org.uk/mp3') 
    shortstring = html2text.html2text(shortstring)
    if debug:
        print ("original = " + longentry)
        print("html2text = " + shortstring)
    shortstring = shortstring.replace('\n', ' ').replace('\r', '').replace('\t', '')
    shortstring = re.sub(" +", " ", shortstring)
    shortstring = shortstring.replace('> ','')
    shortstring = shortstring.replace('<br /','')
    # When the blog moved to wordpress, the content extracted from the page now ends with "Advertisements"
    shortstring = re.sub("Advertisements", "", shortstring)
    
    # it's a non-trivial length string, then add the name of the speaker
    if (len(shortstring)>1): 
        shortstring = d['entries'][i]['title'] + ": " + shortstring
    
    return shortstring

# Testing
'''
for i in range(0,20):
    print (str(i) + ": " + retrieve_text(i) + "\n")
exit()
'''

# Find first entry
shortstring = retrieve_text(0)

# Set up for API calls
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Testing
# shortstring = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including and then"

# ... and now tweet, breaking into separate tweets if necessary
if (len(shortstring)>1): 
    # it's a non-trivial length string
    if len(shortstring) > 280:
        # break into segments
        i = 1
        while True:
            # Assume update will not require more than 9 tweets, hence len(str(i)) = 1
            if len(shortstring) > 277:
                # truncate at a word boundary (ie, not part-way through a word)
                last_space = shortstring[0:276].rfind(" ")
                twt = str(i) + "/ " + shortstring[0:last_space]
                shortstring = shortstring[(last_space+1):]
            else:
                twt = str(i) + "/ " + shortstring
                shortstring = ""
            i += 1
            print ("Tweet will be this: " + twt)
            if (not debug):
                api.update_status (twt)
                print("tweet created")
            else:
                print("debug mode -- tweet not created")
            if len(shortstring) < 1:
                break
    else:
        print ("Tweet will be this: " + shortstring)
        if (not debug):
            api.update_status (shortstring)
            print("tweet created")
        else:
            print("debug mode -- tweet not created")



