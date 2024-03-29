#! python3

# Written on home Windows10 PC
# execute using "py C:\Users\colin\Documents\GitHub\c9\python\photo_sorter\sort_photos_into_folders.py" (may not need the full path)
# or just run .py file from the containing directory
# TODO Make this OS-independent (file naming conventions)

# TODO if more than one photo take on a day, create a sub-folder for that day? (or, option to create sub-folders for days)

import os
import shutil
import datetime
import time
import sys
import pprint

from datetime import datetime as dt # don't understand why I need this, but I can't call fromtimestamp without it

current_year = datetime.datetime.now().year

import exifread

# regex
import re

# garbage collection
# required because it seems that reading lots of large binary files will ultimately run out of memory
# ... although not sure if this is working
import gc

# needed to be able to pull the "Media Created" date from .mp4 files
import pytz
import datetime
import win32com
from win32com.propsys import propsys, pscon

'''
# parse cmd-line parameters
# example usage: .\sort_photos_into_folders.py -t 1 "E:\\DONE owl pellet\\" D:\\sorted_photos\\
# This all works, but actually it's a faff having to add quoted and escaped file location parameters, so I'm not going to use this for now
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("source_dir", help="Source of photos to be sorted", type=str)
parser.add_argument("dest_root_dir", help="Root directory into which photos will be sorted", type=str)
parser.add_argument("-l", "--logging", type=int, choices=[0, 1], help="Logging level")
parser.add_argument("-t", "--test", type=int, choices=[0, 1], help="Test mode (set to 1)")
args = parser.parse_args()

print("source_dir = -->" + args.source_dir + "<---")
print("dest_root_dir = -->" + args.dest_root_dir + "<---")
print("logging = "+ str(args.logging))
print("test = "+ str(args.test))
exit()
'''

####################
# GLOBAL VARIABLES #
####################

# folder containing the photos to be sorted
# TODO handle paths with folders that start with a number (eg, 180615), as preceding '\' followed by digits seems to be a way of encoding escaped characters 
# TODO DO MANUALLY source_dir = "E:\\ubuntu photos\\philippa_pictures\\2010-12-14\\" # <-- special photos, no date information
# source_dir = "G:\\DCIM\\100_PANA\\"
# source_dir = "G:\\DCIM\\101_PANA\\"
# source_dir = "D:\\colin\\Google Drive\\Photos to sort\\"
# source_dir = "G:\\My Drive\\Photos to sort\\philippa phone\\100ANDRO\\"
# source_dir = "G:\\My Drive\\Photos to sort\\"

source_dir = "G:\\My Drive\\Photos to sort\\found on USBHD1\\Pips old nokia\\images\\MMC\\"

# if using program parameters:
# source_dir = args.source_dir

source_file = ""

dest_file = ""

# destination folder hierachy, into which the photos are to be sorted
# dest_root_dir = "D:\\sorted_photos\\"
# dest_root_dir = "D:\\colin\\Google Drive\\Photos\\" <-- worked with Backup & Sync, but has changed with new Google drive sync system
dest_root_dir = "G:\\My Drive\\Photos\\"

# if using program parameters:
# dest_root_dir = args.dest_root_dir
dest_dir = ""

# Testing: don't do the actual file copy: 1 = test mode, 0 = run for real
testing = 1
# if using program parameters:
# testing = args.test


# Logging: extra logging, beyond the core output: 2 = verbose logging; 1 = log copy statements only, 0 = no additional logging
# TODO consider additional logging levels
logging = 1
# if using program parameters:
# logging = args.logging


"""
# DEV WORK
# Recursively list all graphics files in folder (and all sub-folders)

graphics_extensions = ["JPG", "DB", "AVI", "WAV", "GIF", "JP_", "MOV", "PNG", "MP4", "JPEG", "BMP", "MTS", "PEF"]
# I've included JP_, because I've found a few such files which were (mostly) 90-degree rotations of other files. 
# However, I've addressed all such instances to date, so hopefully no more such files will be created

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(dest_root_dir):
	for file in f:
		extension_end = file.rfind('.') + 1
		extension = file[extension_end:].upper()
		if (not(extension in graphics_extensions)):
			files.append(os.path.join(r, file))

for f in files:
	# TODO process file
	dir_end = f.rfind('\\') + 1
	print("Dir = -->" + f[0:dir_end] + "<--; filename = -->" + f[dir_end:] + "<--") 

exit()
"""

#############
# FUNCTIONS #
#############

# return true if already exists, or false & (if required) changes global variable dest_file to end in _{n}, to avoid clashing with file with the same name but a different filesize (sadly this happens often with files created via iPhone export)
def already_exists ():
	if (logging > 1):
		print ("\nstarting already_exists function")
	global source_dir
	global source_file
	global dest_dir
	global dest_file
	if (logging > 1):
		print ("start: source = -->" + source_dir + source_file + "<--")
		print ("start: destination = -->" + dest_dir + dest_file + "<--")
	if os.path.isfile(dest_dir + dest_file):
		source_file_size = os.path.getsize(source_dir + source_file)
		target_dest_file_size = os.path.getsize(dest_dir + dest_file)
		if (logging > 1):
			print ("source_file_size = " + str(source_file_size) + "; target_dest_file_size = " + str(target_dest_file_size))
		if (source_file_size == target_dest_file_size):
			# we've found duplicate
			return True
		else:
			# create a new filename (append _{n}), and check again
			x = re.search("_[0-9].",dest_file) # limitation: will only handle the case of up to 10 duplicates!!!
			if (x):
				# source_file already ends _{n}.[ext], so need to increment n
				new_val = (int)(x.group(0)[1:2]) + 1
				y=re.split('_[0-9].', dest_file)
				dest_file = y[0]+"_"+str(new_val)+"."+y[1]
				if (logging > 1):
					print ("increment _n: source = -->" + source_dir + source_file + "<--")
					print ("increment _n: destination = -->" + dest_dir + dest_file + "<--")
			else:
				# change end from .[ext] to _1.[ext]
				y=re.split('\.', dest_file)
				dest_file = y[0]+"_1."+y[1]
				if (logging > 1):
					print ("_1: source = -->" + source_dir + source_file + "<--")
					print ("_1: destination = -->" + dest_dir + dest_file + "<--")
			return (already_exists())
	else:
		return False




################
# MAIN PROGRAM #
################

print("Starting copy process...")

# count all the files copied
copied_files = 0

# count any duplicates that weren't copied
duplicate_files = 0

# record any unhandled files
unhandled_files_array = []


print("Copying files: " + source_dir + " -> " + dest_root_dir)

# Get list of files to be copied
# TODO consider making this recursive; os.walk will help here, but I'll need to change the file name handling stuff
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(source_dir) if isfile(join(source_dir, f))]

# DEBUGGING -- explore why a particular file / set of files don't work
# onlyfiles = ['photo (1).jpg', 'photo (2).jpg', 'photo (3).jpg', 'photo (4).jpg', 'photo (5).jpg']

# work out what's (roughly) a 10th of the way through the list of files, for progress reporting
perc = int(len(onlyfiles)/10)
if (perc == 0):
	perc = 1

for i in range(len(onlyfiles)):
	# Report progress roughly every 10% of the way through the list of files
	if i % perc == 0:
		print(str(int(10*i/perc))+"%")

	source_file = onlyfiles[i]
	dest_file = source_file

	# variables to hold the creation year/month/day of the photos (used for creating sub-folders)
	dtstring = ""
	y = 0
	m = 0
	d = 0

	if (logging > 1):
		print("\n---------\nfilename = " + source_file)

	# file extension
	extension_end = source_file.rfind('.') + 1
	extension = source_file[extension_end:].upper()
	if (logging > 1):
		print("Extension = " + extension)

	# parsing order: 
	# TODO filename = YYMMDD_HHMMSS.*
	# filename == [IMG_|VID_|PANO_|TRIM_|MVIMG_|SCREENSHOT_PCL_]*
	# filename == [IMG-|VID-]*
	# filename == MOV_*
	# ext == [JPG|JPEG]
	# ext == MP4
	# ext == MOV
	# or can't handle the file
	
	filename_might_have_date = re.search("[0-9][0-9][0,1][0-9][0-3][0-9]",source_file) # YYMMDD
	if (logging > 1):
		print (source_file + " -- check for date in filename: " + str(filename_might_have_date))
	
	if ((source_file[:4].upper() == "IMG_" or source_file[:4].upper() == "VID_" or source_file[:5].upper() == "PANO_" or source_file[:5].upper() == "TRIM_" or source_file[:6].upper() == "MVIMG_" or source_file[:11].upper() == "SCREENSHOT_" or source_file[:4].upper() == "PXL_") and filename_might_have_date): # length check is a rough check that the filename is long enough to have YYMMDD in it
		# Photos from phone have filename in format ("IMG_"|"VID_"|"PANO_"|"TRIM_"|"MVIMG_"|"SCREENSHOT_"|"PXL_")[YYYY][MM][DD]_[HHMMSS].jpg
		# Assumption: no need to do name collision test
		if (logging > 1):
			print("SCENARIO: filename == [IMG_|VID_|PANO_|TRIM_|MVIMG_|SCREENSHOT_|PXL_]*")
		prefix_end = source_file.find('_') + 1

		y = int(source_file[prefix_end:prefix_end+4])
		m = int(source_file[prefix_end+4:prefix_end+6])
		d = int(source_file[prefix_end+6:prefix_end+8])
	elif ((source_file[:4].upper() == "IMG-" or source_file[:4].upper() == "VID-") and filename_might_have_date):
		# WhatsApp images in format ("IMG-"[YYYY][MM][DD]-*.jpg
		# Assumption: no need to do name collision test
		if (logging > 1):
			print("SCENARIO: filename == [IMG-|VID_-]*")
		prefix_end = source_file.find('-') + 1

		y = int(source_file[prefix_end:prefix_end+4])
		m = int(source_file[prefix_end+4:prefix_end+6])
		d = int(source_file[prefix_end+6:prefix_end+8])
	elif (source_file[:4].upper() == "MOV_"):
		# Videos from Xpedia Z5; can use the Windows file last modified date... 
		# UPDATE No we can't! Need to redo this section (and work out which "MOV_*" files this works for) TODO
		if (logging > 1):
			print("SCENARIO: filename == MOV_")
		# dtstring = os.path.getmtime(source_dir + source_file) <-- the old method, but wasn't working for files from Sony Xpedia.
		# print(str(dt))
		# y = int(time.strftime('%Y', time.gmtime(dtstring)))
		# m = int(time.strftime('%m', time.gmtime(dtstring)))
		# d = int(time.strftime('%d', time.gmtime(dtstring)))

		properties = propsys.SHGetPropertyStoreFromParsingName(source_dir + source_file)
		dtstring = str(properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue())
		y = int(dtstring[0:4])
		m = int(dtstring[5:7])
		d = int(dtstring[8:10])
		if (logging > 1):
			print("y/m/d = " + str(y)+"/" + str(m) + "/" + str(d))
	elif (extension == "JPG" or extension == "JPEG"):
		# it's from another source (eg, my old Panasonic Lumix camera)
		# For images, pull date from EXIF
		# For video, pull "Date acquired" directly from the binary
		if (logging > 1):
			print("SCENARIO: ext == [JPG|JPEG]")

		# ctime and mtime aren't what I need - I need Windows "Date acquired", or (better still?) pull information from image or video exif
		# https://stackoverflow.com/questions/45221014/python-exif-cant-find-date-taken-information-but-exists-when-viewer-through-wi
		# use exifread

		f = open(source_dir + source_file, 'rb')
		tags = exifread.process_file(f)
		# TODO what about "Image DateTime" tag? When should I use this?
		if "EXIF DateTimeOriginal" in tags:
			dtstring = str(tags["EXIF DateTimeOriginal"])
			if (logging > 1):
				print("EXIF DateTimeOriginal: " + dtstring)
			y = int(dtstring[0:4])
			m = int(dtstring[5:7])
			d = int(dtstring[8:10])
		else:
			print ("Can't read date information from EXIF for file: " + source_file)
			if (logging > 1): # creates loads of output
				# Remove JPEGThumbnail from dict (as this is enormous)
				if ("JPEGThumbnail" in tags):
					del tags["JPEGThumbnail"]
				print("EXIF tags:")
				pprint.pprint(tags)
			if (not(source_file in unhandled_files_array)):
				unhandled_files_array.append(source_file)

	elif (extension == "MP4"):
		# Logic for videos from Panasonic Lumix camera
		# After trying numerous approaches, finally got this working via direct read of the binary data
		# Note this has only been tested for videos created with my old Panasonic Lumix camera...
		if (logging > 1):
			print("SCENARIO: ext == MP4")

		with open(source_dir + source_file, "rb") as f:
			bytes = f.read()[1:200000] # restrict read to start of file, just for performance reasons
			# Translate from binary to ASCII
			file_data = bytes.decode("ascii",errors="ignore")

			# Data is a little before the second occurance of 'Panasonic'
			# TODO experiment with just doing the same as for .MOV files
			matchstr="Panasonic"
			# Find the first match
			firstmatch = file_data.find(matchstr)
			# Now find the next match
			file_data = file_data [firstmatch+10:]
			secondmatch = file_data.find(matchstr)

			# "Date acquired" starts somewhere close to 50 chars before the match
			# Grab an over-sized substring that we're confident should include the date, and then use regex to pick it out
			search_string = file_data[secondmatch-70:secondmatch-30]
			x = re.search("[12][0-9][0-9][0-9]:[01][0-9]:[0-3][0-9]",search_string)
			if (x):
				# We have a match
				dtstring = x.group(0)
				y = int(dtstring[0:4])
				y = int(dtstring[0:4])
				m = int(dtstring[5:7])
				d = int(dtstring[8:10])
				if (logging > 1):
					print("created date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))		
			else:
				print ("Could not find date for file " + source_file)
				if (not(source_file in unhandled_files_array)):
					unhandled_files_array.append(source_file)
			f.close()
			# Do garbage collection TODO this isn't working, still run out of memory with v.large video files
			gc.collect()

	elif (extension == "MOV"):
		# Logic for videos from iPhone
		if (logging > 1):
			print("SCENARIO: ext == MOV")
	
		with open(source_dir + source_file, "rb") as f:
			bytes = f.read()
			# Translate from binary to ASCII
			file_data = bytes.decode("ascii",errors="ignore")
			# matchstr="Panasonic"
			# There are 2 matches, need to find the second match
			# firstmatch = file_data.find(matchstr)
			# Now find the next match
			# file_data = file_data [firstmatch+10:]
			# secondmatch = file_data.find(matchstr)

			# "Date acquired" starts somewhere close to 50 chars before the match
			# grab an over-sized substring that we're confident should include the date, and then use regex to pick it out
			# search_string = file_data[secondmatch-70:secondmatch-30]
			x = re.search("[12][0-9][0-9][0-9]-[01][0-9]-[0-3][0-9]",file_data)
			if (x):
				# We have a match
				dtstring = x.group(0)
				y = int(dtstring[0:4])
				y = int(dtstring[0:4])
				m = int(dtstring[5:7])
				d = int(dtstring[8:10])
				if (logging > 1):
					print("created date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))		
			else:
				print ("Could not find date for file " + source_file)
				if (not(source_file in unhandled_files_array)):
					unhandled_files_array.append(source_file)
			f.close()
			# Do garbage collection TODO this isn't working, still run out of memory with v.large video files
			gc.collect()

	else:
		# Can't handle this file
		# TODO handle this situation, and don't drop straight into the code below (need to restructure)
		print("Can't handle file " + source_file)
		unhandled_files_array.append(source_file)
		# TODO in this situation, skip over the rest of the logic

	if (logging > 1):
		print("created date " + str(dtstring) + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))
		# TODO dtstring isn't always in the same format (eg, for MOV_*.mp4 files from Sony Xperia), so printing isn't always working properly here

    # TODO Fix this up. This is a hack to get around the fact that sometimes the data pulled from EXIF is incorrect.
	# via chatGTP, I found some code that will pull out year/month/day via getmtime (which I have used previously, but 
	# disabled because it didn't always work)
	if (y == 0): # ie, if we still haven't generated a year value
		# Get the last modification time of a file
		mtime = os.path.getmtime(source_dir + source_file)
		# Convert the timestamp to a datetime object
		modification_datetime = datetime.datetime.fromtimestamp(mtime)
		# Extract year, month, and day
		y = modification_datetime.year
		m = modification_datetime.month
		d = modification_datetime.day
		# Print the results
		if (logging > 1): 
			print(f"ChatGPT - Year: {y}, Month: {m}, Day: {d}")

	# Do some basic validation: non-crazy year (eg, > 1990, less than current year), month in range 1 to 12, day in range 1 to 31 
	# TODO future enhancemend: do completely accurate day check
	if (y < 1990 or y > current_year):
		print("File " + source_file + " has implausible creation year: " + str(y))
		if (not(source_file in unhandled_files_array)):
			unhandled_files_array.append(source_file)
	elif (m < 1 or m > 12):
		print("File " + source_file + " has impossible creation month: " + str(m))
		if (not(source_file in unhandled_files_array)):
			unhandled_files_array.append(source_file)
	elif (d < 1 or d > 31):
		print("File " + source_file + " has impossible creation day: " + str(d))
		if (not(source_file in unhandled_files_array)):
			unhandled_files_array.append(source_file)
	else:
		# TODO make this section respect the 'testing' flag
		# We have acceptable year/month/day creation date for the file
		# Create root folder, if needed
		dest_dir = dest_root_dir
		if not(os.path.isdir(dest_dir)):
			print("create root folder: " + dest_dir)
			os.mkdir(dest_dir)
		
		# create year directory, if needed
		dest_dir = dest_dir + str(y) + "\\"
		if not(os.path.isdir(dest_dir)):
			print("create year dir: " + dest_dir)
			os.mkdir(dest_dir)
			
		# create month directory, if needed
		dest_dir = dest_dir + format(m,'02') + "_" + str(datetime.date(y, m, d).strftime('%B')) + "\\"
		if not(os.path.isdir(dest_dir)):
			print("create month dir: " + dest_dir)
			os.mkdir(dest_dir)

		# now copy the file
		# check if file already there
		
		# Use function already_exists() to check for the file at the destination
		# function checks for accidental name clashes, and changes target name if such a clash exists
		if (already_exists()):
			print("File already exists: " + dest_dir + dest_file)
			duplicate_files += 1
		else:
			if (testing == 0):
				# copy the file
				if (logging > 1):
					print("Copy: " + source_dir + source_file + " -> " + dest_dir + dest_file)
				shutil.copyfile(source_dir + source_file, dest_dir + dest_file)
				# TODO could change copy for move, but this program is attempting to be idempotent
			else:
				if (logging > 1):
					print("TEST MODE: Copy: " + source_dir + source_file + " -> " + dest_dir + dest_file)
			
			# print(".",end='',flush=True) # TODO looked like flush was working, but maybe not...?
			copied_files += 1

	# Testing -- break out of loop
	# if i > 1:
	# 	exit()

print ("\n---------\nFinished. Total files copied = " + str(copied_files) + "; duplicates not copied = " + str(duplicate_files) + "; unhandled files = " + str(str(len(unhandled_files_array))))
if (len(unhandled_files_array)>0):
	print("List of unhandled files:")
	for x in (unhandled_files_array):
		print(x)


