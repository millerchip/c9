#! python3

# I uninstalled Python 2.7 pyserial-2.7, Python 2.7.13 (64-bit), Python 3.7.1 (32-bit), Python 3.7.3 (64-bit), Python Launcher

# Written on home Windows10 PC
# execute using "py C:\Users\colin\Documents\GitHub\c9\python\photo_sorter\sort_photos_into_folders.py" (may not need the full path)
# or just run .py file from the containing directory
# TODO Make this OS-independent (file naming conventions)

# TODO if more than one photo take on a day, create a sub-folder for that day?
# OR option to create sub-folders for days

import os
import shutil
import datetime
import time
import sys

from datetime import datetime as dt # don't understand why I need this, but I can't call fromtimestamp without it

current_year = datetime.datetime.now().year

import exifread

# regex
import re

print("Starting copy process...")

dest_dir = "D:\sorted_photos\\"

# count all the files copied
copied_files = 0

# count any duplicates that weren't copied
duplicate_files = 0

# count any unhandled files
unhandled_files = 0

# TODO handle paths with folders that start with a number (eg, 180615), as preceding '\' followed by digits seems to be a way of encoding escaped characters 
# source_dir = "D:\colin\Google Drive\Photos to copy to home PC\\180615 OnePlus gdrive upload\\"
# source_dir = "D:\pre-Hunstanton old Lumix backup\\109_PANA\\"
# source_dir = "G:\\DCIM\\105_PANA\\"
# source_dir = "G:\\DCIM\\106_PANA\\"
# source_dir = "D:\\unsorted ubuntu photos\\"
# source_dir = "D:\colin\Google Drive\Photos to copy to home PC\\"
# source_dir = "E:\\ubuntu photos\\Photos to copy to home PC\\"
source_dir = "E:\\ubuntu photos\\2015\\"

print("Copying files: " + source_dir + " -> " + dest_dir)

# Get list of files to be copied
# TODO consider making this recursive; os.walk will help here, but I'll need to change the file name handling stuff
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(source_dir) if isfile(join(source_dir, f))]

# work out what's (roughly) a 10th of the way through the list of files
perc = int(len(onlyfiles)/10)

for i in range(len(onlyfiles)):
    # Report progress every 10% of the way through the list of files
    if i % perc == 0:
        print(str(int(10*i/perc))+"%")

    curr_file = onlyfiles[i]

    y = 0
    m = 0
    d = 0
	
    # print("filename = " + curr_file)
	
    # file extension
    extension_end = curr_file.find('.') + 1
    extension = curr_file[extension_end:].upper()
    # print("Extension = " + extension)
	
    # if curr_file.find('_') != -1:
    if (curr_file[:4].upper() == "IMG_" or curr_file[:4].upper() == "VID_" or curr_file[:5].upper() == "PANO_" or curr_file[:5].upper() == "TRIM_"):
        # Photos from phone have filename in format ("IMG_"|"VID_"|"PANO_"|"TRIM_")[YYYY][MM][DD]_[HHMMSS].jpg
        # only process such fles
        prefix_end = curr_file.find('_') + 1
        # prefix = curr_file[0:prefix_end] # Don't think we need this variable

        y = int(curr_file[prefix_end:prefix_end+4])
        m = int(curr_file[prefix_end+4:prefix_end+6])
        d = int(curr_file[prefix_end+6:prefix_end+8])
    elif (extension == "JPG" or extension == "JPEG"):
		# it's from another source (eg, my old Panasonic Lumix camera)
		# For images, pull date from exif
		# For video, pull "Date acquired" directly from the binary
		
		# ctime and mtime aren't what I need - I need Windows "Date acquired", or (better still?) pull information from image or video exif
		# https://stackoverflow.com/questions/45221014/python-exif-cant-find-date-taken-information-but-exists-when-viewer-through-wi
		# use exifread

        f = open(source_dir + curr_file, 'rb')
        tags = exifread.process_file(f)
        if "Image DateTime" in tags:
            dtstring = str(tags["Image DateTime"])
            y = int(dtstring[0:4])
            m = int(dtstring[5:7])
            d = int(dtstring[8:10])
        else:
            print ("Can't read date information from EXIF for file: " + curr_file)
            unhandled_files += 1

    elif (extension == "MP4"):
        # Logic for videos from Panasonic Lumix camera
        # After trying numerous approaches, finally got this working via direct read of the binary data
        # Note this has only been tested for videos created with my old Panasonic Lumix camera...
		
        with open(source_dir + curr_file, "rb") as f:
            bytes = f.read()[1:500000] # restrict read to start of file, just for performance reasons
            # Translate from binary to ASCII
            startoffile = bytes.decode("ascii",errors="ignore")
            matchstr="Panasonic"
            # There are 2 matches, need to find the second match
            firstmatch = startoffile.find(matchstr)
            # Now find the next match
            startoffile = startoffile [firstmatch+10:]
            secondmatch = startoffile.find(matchstr)

            # "Date acquired" starts somewhere close to 50 chars before the match
            # grab an over-sized substring that we're confident should include the date, and then use regex to pick it out
            search_string = startoffile[secondmatch-70:secondmatch-30]
            x = re.search("[12][0-9][0-9][0-9]:[01][0-9]:[0-3][0-9]",search_string)
            if (x):
                # We have a match
                dtstring = x.group(0)
                # dtstring = startoffile[secondmatch-51:secondmatch-40] # format is YYYY:MM:DD... but doesn't always work, as offset can be in a different place
                # print("testfile " + testfile + ": date = -->" + dtstring + "<--")
                y = int(dtstring[0:4])
                y = int(dtstring[0:4])
                m = int(dtstring[5:7])
                d = int(dtstring[8:10])
                # print("Test video = " + testfile)
                # print("created date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))		
            else:
                print ("Could not find date for file " + curr_file)
                unhandled_files += 1
            f.close()

    else:
        # Can't handle this file
        # TODO handle this situation, and don't drop straight into the code below (need to restructure)
        print("Can't handle file " + curr_file)
		
	# Do some basic validation: non-crazy year (eg, > 1990, less than current year), month in range 1 to 12, day in range 1 to 31 
	# TODO future enhancemend: do completely accurate day check
    if (y < 1990 or y > current_year):
        print("File " + curr_file + " has implausible creation year: " + str(y))
        unhandled_files += 1
    elif (m < 1 or m > 12):
        print("File " + curr_file + " has impossible creation month: " + str(m))
        unhandled_files += 1
    elif (d < 1 or d > 31):
        print("File " + curr_file + " has impossible creation day: " + str(d))
        unhandled_files += 1
    else:
        # We have acceptable year/month/day creation date for the file
		# Create root folder, if needed
        dest_file = dest_dir
        if not(os.path.isdir(dest_file)):
            print("create root folder: " + dest_file)
            os.mkdir(dest_file)
		
		# create year directory, if needed
        dest_file = dest_file + str(y) + "\\"
        if not(os.path.isdir(dest_file)):
            print("create year dir: " + dest_file)
            os.mkdir(dest_file)
			
        # create month directory, if needed
        dest_file = dest_file + format(m,'02') + "_" + str(datetime.date(y, m, d).strftime('%B')) + "\\"
        if not(os.path.isdir(dest_file)):
            print("create month dir: " + dest_file)
            os.mkdir(dest_file)

		# now copy the file
		# check if file already there
        dest_file = dest_file + curr_file
        if os.path.isfile(dest_file):
            print("File already exists: " + dest_file)
            duplicate_files += 1
        else:
            # print("Copy: " + source_dir + curr_file + " -> " + dest_file)
            shutil.copyfile(source_dir + curr_file, dest_file)
            print(".",end='')
            copied_files += 1
            # TODO once this is working, turn it into a move (os.rename (src, dest))

	# Testing -- break out of loop
    # if i > 1:
    #     exit()

print ("Finished. Total files copied = " + str(copied_files) + "; duplicates not copied = " + str(duplicate_files) + "; unhandled files = " + str(unhandled_files))








