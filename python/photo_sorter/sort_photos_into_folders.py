#! python3

# I uninstalled Python 2.7 pyserial-2.7, Python 2.7.13 (64-bit), Python 3.7.1 (32-bit), Python 3.7.3 (64-bit), Python Launcher

# Written on home Windows10 PC
# execute using "py C:\Users\colin\Documents\GitHub\c9\python\photo_sorter\sort_photos_into_folders.py" (may not need the full path)
# or just run .py file from the containing directory
# TODO Make this OS-independent (file naming conventions)

# TODO with changes to use exif information, might need to execute using "python.exe C:\Users\colin\Desktop\sort_photos_into_folders.py"

# TODO if more than one photo take on a day, create a sub-folder for that day?
# OR option to create sub-folders for days

import os
import shutil
import datetime
import time
import sys

from datetime import datetime as dt # don't understand why I need this, but I can't call fromtimestamp without it

# IMAGES
# WORKING Return Exif tags for image
# UPDATE suddenly it won't import exifread; when the import was working, this code was working
# Thought https://medium.com/@dirk.avery/pytest-modulenotfounderror-no-module-named-requests-a770e6926ac5 might help, but I don't have pytest installed
# I ended up uninstalling all of Python, re-installing, and then it worked

import exifread

testimage = "D:\\sorted_photos\\2019\\06_June\\P1090440.JPG"
f = open(testimage, 'rb')
tags = exifread.process_file(f)
if "Image DateTime" in tags:
	dtstring = str(tags["Image DateTime"])
	y = int(dtstring[0:4])
	m = int(dtstring[5:7])
	d = int(dtstring[8:10])
	print("Test image = " + testimage)
	print("created date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))
else:
	print ("problems!")

# VIDEO
# After trying numerous approaches, finally got this working via direct read of the binary data
# I've stripped out all the previous attempts from this file (it's in the github version history)
# Note this only works for videos created with my old Panasonic Lumix camera...

print("Opening binary file")
# testfile="E:\\ubuntu photos\\2015\\P1030793.MP4" # 2013:11:02
# testfile="E:\\ubuntu photos\\2015\\P1040809.MP4" # 2014:11:01
testfile="E:\\ubuntu photos\\2015\\P1040709.mp4" # 2014:10:26

with open(testfile, "rb") as f:
    bytes = f.read()[1:500000] # restrict read to start of file, just for performance reasons
    # Translate from binary to ASCII
    startoffile = bytes.decode("ascii",errors="ignore")
    matchstr="Panasonic"
    # There are 2 matches, need to find the second match
    firstmatch = startoffile.find(matchstr)
	# Now find the next match
    startoffile = startoffile [firstmatch+10:]
    secondmatch = startoffile.find(matchstr)
	# "Date acquired" starts 50 chars before the match
    dtstring = startoffile[secondmatch-50:secondmatch-40] # format is YYYY:MM:DD
    # print("testfile " + testfile + ": date = -->" + dtstring + "<--")
    y = int(dtstring[0:4])
    y = int(dtstring[0:4])
    m = int(dtstring[5:7])
    d = int(dtstring[8:10])
    print("Test video = " + testfile)
    print("created date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))
    f.close()
print("Finishing binary file read")
exit()  


# Below is the main file
# TODO integrate the above procedures, into the main file


print("Starting copy process...")

dest_dir = "D:\sorted_photos\\"

# count all the files copied
copied_files = 0

# count any duplicates that weren't copied
duplicate_files = 0

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
	
	print("filename = " + curr_file)
	
	if curr_file.find('_') != -1:
		# Photos from phone have filename in format ("IMG_"|"VID_"|"PANO_")[YYYY][MM][DD]_[HHMMSS].jpg
		# only process such fles
		prefix_end = curr_file.find('_') + 1
		prefix = curr_file[0:prefix_end]
		
		if (prefix == "IMG_" or prefix == "VID_" or prefix == "PANO_" or prefix == "TRIM_"):
			# parse date
			y = int(curr_file[prefix_end:prefix_end+4])
			m = int(curr_file[prefix_end+4:prefix_end+6])
			d = int(curr_file[prefix_end+6:prefix_end+8])
			# print("d,m,y = " + str(d) + "," + str(m) + "," + str(y))
		else:
			print (">>> Unknown phone filename format: " + curr_file)
			# TODO handle this situation
	else:
		# it's from the Panasonic Lumix camera
		# >>> problems here! <<<
		# ctime and mtime aren't what I need - I need Windows "Date acquired", or (better still?) pull information from image or video exif
		# https://stackoverflow.com/questions/45221014/python-exif-cant-find-date-taken-information-but-exists-when-viewer-through-wi
		# use exifread ? or Pillow
		f = open(source_dir + curr_file, 'rb')
		tags = exifread.process_file(f)
		print ("Tags:")
		for tag in tags.keys():
			if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
				print ("Key: " + tag + ", value " + tags[tag])
		
		
		
		created = os.stat(source_dir + curr_file).st_ctime
		modified = os.stat(source_dir + curr_file).st_mtime
		dtstring = str(dt.fromtimestamp(created))
		# file date format will be YYYY-MM-DD HH:MM:SS
		y = int(dtstring[0:4])
		m = int(dtstring[5:7])
		d = int(dtstring[8:10])
		print(source_dir + curr_file + ": " + "created date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))
	
	# create root folder, if needed
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
		print("file already exists: " + dest_file)
		duplicate_files += 1
	else:
		print("Copy: " + source_dir + curr_file + " -> " + dest_file)
		# shutil.copyfile(source_dir + curr_file, dest_file)
		print(".",end='')
		copied_files += 1
		# TODO once this is working, turn it into a move (os.rename (src, dest))
		

	# Testing -- break out of loop
	if i > 1:
		exit()

print ("Finished. Total files copied = " + str(copied_files) + "; duplicates not copied = " + str(duplicate_files))








