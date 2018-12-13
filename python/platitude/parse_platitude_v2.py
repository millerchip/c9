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


# Testing
'''
for i in range(0,20):
    longentry = d['entries'][i]['description']
    match = longentry.rfind('<a href="/mp3')
    if match != -1:
        longentry = longentry[0:match]
    match = longentry.rfind('<a href="https://www.bbc.co.uk/radio/play')
    if match != -1:
        longentry = longentry[0:match]
    shortstring = longentry
    shortstring = html2text.html2text(shortstring)
    shortstring = shortstring.replace('\n', ' ').replace('\r', '').replace('\t', '')
    shortstring = re.sub(" +", " ", shortstring)
    shortstring = shortstring.replace('> ','')
    shortstring = shortstring.replace('<br /','')
    print (str(i) + ": shortstring = " + shortstring + "\n")
exit()
'''

# Find first entry
longentry = d['entries'][0]['description']

# remove URL sections linking to audio
match = longentry.rfind('<a href="/mp3')
if match != -1:
    longentry = longentry[0:match]
match = longentry.rfind('<a href="https://www.bbc.co.uk/radio/play')
if match != -1:
    longentry = longentry[0:match]
shortstring = longentry

# Format text (eg, strip out HTML, line breaks, etc)
shortstring = html2text.html2text(shortstring)
shortstring = shortstring.replace('\n', ' ').replace('\r', '').replace('\t', '')
shortstring = re.sub(" +", " ", shortstring)
shortstring = shortstring.replace('> ','')
shortstring = shortstring.replace('<br /','')

# Set up for API calls
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Testing
# shortstring = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including and then"

# ... and now tweet, breaking into separate tweets if necessary
if (len(shortstring)>1): 
    # it's a non-trivial length string

    # Add title (which is the speaker)
    shortstring = d['entries'][0]['title'] + ": " + shortstring

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
            # api.update_status (twt)
            if len(shortstring) < 1:
                break
    else:
        print ("Tweet will be this: " + shortstring)
        # api.update_status (shortstring)


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