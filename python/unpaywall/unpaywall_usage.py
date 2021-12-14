# First, extract the information from the extension's installation page (requires parsing the HTML)
from lxml import html
# import requests
from bs4 import BeautifulSoup

from urllib.request import urlopen

url = "https://chrome.google.com/webstore/detail/unpaywall/iplffkdpngmdjhlpjmppncnlhomiipha?hl=en"

html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')

# This is what the specific portion of HTML looks like, that contains the count of users
# <span class="e-f-ih" title="170,319 users"><span class="FokDXb e-f-ih-s" aria-hidden="true"></span>170,319 users</span>

# Pull out this section of HTML
user_text = str(soup.findAll("span", {"class": "e-f-ih"})[0])

# Now identify the user count, and convert to an integer
x = user_text.find('users">')
y = user_text.rfind(' users</span>')
user_text = user_text[x+7:y]
user_text = user_text.replace(',','')
user_count = int(user_text)

# now I need to write this into a google doc
# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
# Service account is called "service_account"

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import datetime

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('unpaywall_client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
# sheet = client.open("unpaywall_usage").sheet1
# Hmm didn't work, so open by URL instead (which works)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1QYotNHsmYfxR7lWCqJNQycrqtZLDJfoJpQLCpFz8wck/edit#gid=0").sheet1

# Extract and print all of the values
# list_of_hashes = sheet.get_all_records()

# find the first empty row
# jump in 10's, because there are already >80 entries (as of 12-Dec-18)
i=1
while True:
    if sheet.cell(i,1).value=="":
        break
    i += 10

# then count back to a blank cell
while True:
    if sheet.cell(i-1,1).value!="":
        break
    i -= 1

today = datetime.datetime.today().strftime('%d/%m/%Y')

print ("Usage today (" + today + ") = " + str(user_count))

# Now write into the spreadsheet
sheet.update_cell(i, 1, today)
sheet.update_cell(i, 2, user_count)

