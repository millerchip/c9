# click the 'Run' button at the top to start this application

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
d = feedparser.parse("http://www.platitudes.org.uk/platblog/rss.php")

# test if parsing works on lots of candidate tweets
'''
for i in range(0,20):
    longentry = d['entries'][i]['description']
    shortstring = html2text.html2text(longentry[0:longentry.find('<a href')])
    shortstring = shortstring.replace('\n', ' ').replace('\r', '').replace('\t', '')
    shortstring = re.sub(" +", " ", shortstring)
    shortstring = shortstring.replace('> ','')
    twt = shortstring
    if len(twt) > 280:
        twt = twt[0:276] + "..."
    print (str(i) + " (length " + str(len(twt)) + "): " + twt)
exit()
'''

# Find first entry
longentry = d['entries'][0]['description']

# Not currently using the title, because it takes too many characters
title = d['entries'][0]['title']

# Truncate at URL
shortstring = longentry[0:longentry.find('<a href')]

# Strip out HTML
'''
shortstring = shortstring.replace('<br />',' ')
shortstring = shortstring.replace('<i>','')
shortstring = shortstring.replace('</i>','')
shortstring = shortstring.replace('&#039;','\'')
shortstring = shortstring.replace('<blockquote>','')
shortstring = shortstring.replace('</blockquote>','')
# Remove any double-spaces or triple-spaces introduced by these replace statements
shortstring = shortstring.replace('  ',' ')
shortstring = shortstring.replace('  ',' ')
'''
shortstring = html2text.html2text(longentry[0:longentry.find('<a href')])
shortstring = shortstring.replace('\n', ' ').replace('\r', '').replace('\t', '')
shortstring = re.sub(" +", " ", shortstring)
shortstring = shortstring.replace('> ','')


# print ("shortstring = " + shortstring)

# Assemble tweet
# not including title, as it's too long
# twt = "Platitude of the day, from " + title + ": " + shortstring

# Only tweet if text is non-empty:
if (len(shortstring)>1):
    # twt = "Platitude of the day: " + shortstring
    twt = shortstring
    if len(twt) > 280:
        twt = twt[0:276] + "..."
    print ("Tweet will be this: " + twt)
    # ... and now tweet
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status (twt)



'''
using Python3, which seems to have overcome an error thrown by use of tweepy
... but it's now broken the feedparser, which was working great... argh!
I've probably borked the whole environment, as I've done a few upgrades
    1  pip
    2  pip install feedparser
    3  pip list
    4  sudo pip install feedparser
    5  pip list
    6  sudo pip install tweepy
    7  pip list
    8  pip3
    9  pip3 install --upgrade pip
   10  sudo pip3 install --upgrade pip
   11  pip
   12  pip3
   13  pip list
   14  pip3 list
   15  python3-pip
   16  pip3 list
   17  sudo pip3 list
   18  sudo pip3 install --upgrade feedparser
   19  sudo pip3 install --upgrade tweepy
   20  history
Attempted a fix via https://docs.c9.io/v1.0/discuss/5582ebe0b806360d002448d9
sudo mv /usr/bin/python /usr/bin/python2
sudo ln -s /usr/bin/python3 /usr/bin/python
"python --version" now confirms it's changed from 2.7.6 to 3.4.0

https://mycodememo.com/set-up-python3-and-mysql-in-cloud9/
Then had to remove the old python 2.7 dist-packages directory (actually, I renamed it), and reinstall tweepy
... which didn't work, so I tried "sudo -H pip install --ignore-installed tweepy"
... which seems to have worked
'''