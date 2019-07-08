#! python3

# I uninstalled Python 2.7 pyserial-2.7, Python 2.7.13 (64-bit), Python 3.7.1 (32-bit), Python 3.7.3 (64-bit), Python Launcher

# Written on home Windows10 PC
# execute using "py C:\Users\colin\Desktop\sort_photos_into_folders.py" (may not need the full path)
# TODO Make this OS-independent (file naming conventions)

# TODO with changes to use exif information, might need to execute using "python.exe C:\Users\colin\Desktop\sort_photos_into_folders.py"

# TODO if more than one photo take on a day, create a sub-folder for that day?
# OR option to create sub-folders for days

import os
import shutil
import datetime
import time
import sys

# import sys # may only be needed for debugging

from datetime import datetime as dt # don't understand why I need this, but I can't call fromtimestamp without it

# from PIL import Image

# need a library for video files: options include pytaglib (still being developed),
# which requires Cython, and Windows SKD 8.1 (https://developer.microsoft.com/en-us/windows/downloads/sdk-archive)
# im = Image.open("E:\\ubuntu photos\\2015\\P1030793.MP4")

# im = Image.open("D:\\sorted_photos\\2019\\06_June\\P1090440.JPG")

# get the date
# format is 2019:05:18 16:02:57

# IMAGES
# WORKING Return Exif tags for image 
# UPDATE suddenly it won't import exifread; when the import was working, this code was working
# Thought https://medium.com/@dirk.avery/pytest-modulenotfounderror-no-module-named-requests-a770e6926ac5 might help, but I don't have pytest installed
# I ended up uninstalling all of Python, re-installing, and then it worked

import exifread
# import ExifRead
# from ExifRead import process_file
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
# Approaches to take:
# 1) Read date acquired from file, using Python library.
# I've tried numerous libraries, so far without luck
#
# 2) Read data from Windows, since Windows Explorer is able to display the "Date acquired" field
# The Python 'os' library doesn't provide access to date acquired
# understanding the windows date field: https://superuser.com/questions/147525/what-is-the-date-column-in-windows-7-explorer-it-matches-no-date-column-from/335901#335901
#
# 3) Use a Python API onto another tool, eg, ffmpeg
# (I haven't properly explored this option yet)
# http://ffmpeg.org/ffmpeg-formats.html#Metadata-1 suggests ffmpeg's metadata extractor won't give me what I need
#
# 4) Read the binary data directly from the file
# https://groups.google.com/forum/#!topic/uk.tech.broadcast/CtG52oFTgW4 has some information on file offsets here
#




"""
P1030793.MP4: offset 25552 ( 2013:11:02 10:47:30 2013:11:02 10:47:30)
P1030821.MP4: offset 28016
P1030845.MP4: offset 31392
P1030857.MP4: offset 51184
Think if I find "Panasonic   j", then read from 52bytes before "P" for 10 bytes, translate each byte into ANSI ASCII, and I'll get a string like 2013:12:18
https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte
"""

# This works, but if I try to read to 28 bytes, I hit this error:
# UnicodeDecodeError: 'ascii' codec can't decode byte 0xbb in position 26: ordinal not in range(128)... but setting errors="ignore" seems to work
print("Opening binary file")
# testfile="E:\\ubuntu photos\\2015\\P1030793.MP4" # 2013:11:02
# testfile="E:\\ubuntu photos\\2015\\P1040809.MP4" # 2014:11:01
testfile="E:\\ubuntu photos\\2015\\P1040709.mp4" # 2014:10:26

# WORKS! But only for Panasonic Lumix created videos...
with open(testfile, "rb") as f:
    bytes = f.read()[1:500000] # restrict read to start of file, just for performance reasons
    startoffile = bytes.decode("ascii",errors="ignore")
    # print(startoffile)
	# find match with "Panasonic   j"... doesn't seem to work (problems with spaces, which perhaps aren't spaces?)
	# So instead, find second match with "Panasonic"
    # print("Length of string = " + str(len(startoffile)))
    matchstr="Panasonic"
    firstmatch = startoffile.find(matchstr)
    # print("firstmatch = " + str(firstmatch))
    # print("100 chars either side of first match = -->" + startoffile[firstmatch-100:firstmatch+100] + "<--") 
	# Now find the next match
    startoffile = startoffile [firstmatch+10:]
    # print("Length of rest of string = " + str(len(startoffile)))
    secondmatch = startoffile.find(matchstr)
    # print("secondmatch = " + str(secondmatch))
    # print("100 chars either side of second match = -->" + startoffile[secondmatch-100:secondmatch+100] + "<--")
    dtstring = startoffile[secondmatch-50:secondmatch-40] # format is YYYY:MM:DD
    # print("testfile " + testfile + ": date = -->" + dtstring + "<--")
    y = int(dtstring[0:4])
    y = int(dtstring[0:4])
    m = int(dtstring[5:7])
    d = int(dtstring[8:10])
    print("Test video = " + testfile)
    print("created date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))
    # print(type(startoffile))
    f.close()
print("Finishing binary file read")
exit()  



# Try another tack: use Python to read Windows file information
"""
print("Trying pathlib")
from pathlib import Path
current_dir = Path('E:\\ubuntu photos\\2015\\P1030793.MP4')
for path in current_dir.iterdir():
	info = path.stat()
	print(info.st_mtime)
print("exiting")
"""

"""
# Print some of the other dates from https://docs.python.org/3/library/os.html
# Problem is, it seems that Windows pulls the "date acquired" field displayable in Windows Explorer, from the file itself
# So the OS library used below is limited to standard date fields, none of which matches "date acquired" that can be seen in Windows Explorer
from datetime import datetime
from os import scandir

def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%d %b %Y')
    return formated_date

def get_files():
    dir_entries = scandir('E:\\ubuntu photos\\2015\\')
    for entry in dir_entries:
        if entry.is_file():
            info = entry.stat()
            print("file " + entry.name + " : st_atime = " + convert_date(info.st_atime))
            print("file " + entry.name + " : st_ctime = " + convert_date(info.st_ctime))
            print("file " + entry.name + " : st_mtime = " + convert_date(info.st_mtime))

get_files()

exit()
"""

# pytaglib
# can't get pytaglib to install; might be this issue https://github.com/supermihi/pytaglib/issues/49
# UPDATE Am trying manual install, as per instructions at https://pypi.org/project/pytaglib/
# have installed C++ build tools, and ccake, and msbuild
# had to use the msbuild cmd prompt to run msbuild: quite a number of compiler warnings
# ... and then run into endless link problems, which I've failed to resolve.


# enzyme
# won't do MP4's https://github.com/Diaoul/enzyme/issues/24

# tinytag 
# doesn't do the tags I need https://pypi.org/project/tinytag/#description
# https://github.com/googleapis/google-cloud-python/issues/3884 said to run pip install --upgrade setuptools



"""
# mp4file
# https://pypi.org/project/mp4file/0.2/#description is ancient, and v0.2
# no documentation!
# importing the library, and then running help(mp4file) lists the package contents: atom, atomsearch, atomsearch_test, mp4file
# https://github.com/billnapier/mp4file/blob/master/src/example.py for sample code

# import mp4file
# from mp4file.mp4file import Mp4File
# file = mp4file.Mp4File("E:\\ubuntu photos\\2015\\P1030793.MP4")

# from mp4file.mp4file import Mp4File
print("Trying module mp4file")
import mp4file
# from mp4file.mp4file import Mp4File

file = mp4file.mp4file("E:\\ubuntu photos\\2015\\P1030793.MP4")
title = mp4file.find_metadata_atom(file, 'title')
print("title = " + title)
exit()
"""



"""
# this works, but doesn't return any creation date metadata... and also, the script never exits! Bizarre!
import imageio
# https://www.programcreek.com/python/example/104521/imageio.get_reader
# reader = imageio.get_reader('imageio:cockatoo.mp4')
reader = imageio.get_reader("D:\\sorted_photos\\2016\\01_January\\VID_20160123_180829.mp4", 'ffmpeg') # a smaller file
metadata = reader.get_meta_data()
print(metadata)
print("now exit...")
exit()
"""


"""
import pims
# from https://github.com/soft-matter/pims/blob/master/examples/loading%20video%20frames.ipynb
v = pims.Video("D:\\sorted_photos\\2016\\01_January\\VID_20160123_180829.mp4")
v
# Should print some information, but doesn't
# type(v) fails, as does trying to print v
print("now exit...")
sys.exit()
"""



"""
# TODO try https://github.com/imageio/imageio-ffmpeg (or another FFmpeg wrapper, as suggested at https://python-forum.io/Thread-Getting-EXIF-data-from-image-AND-video-files)
# TODO https://pypi.org/project/ffmpeg/#description
print("imageio_ffmpeg:") 
import imageio_ffmpeg
reader = imageio_ffmpeg.read_frames("E:\\ubuntu photos\\2015\\P1030793.MP4")
print(type(reader)) # this prints <class 'generator'>
# print("#frames = " + str(reader.count_frames()))
"""

print("now exit...")
sys.exit()


# TODO try https://docs.mikeboers.com/pyav/develop/index.html
# TODO check for other libraries in https://scikit-image.org/docs/dev/user_guide/video.html
# TODO https://smarnach.github.io/pyexiftool/ to get exiftool... which I've installed, but I don't seem to be able to import the module... and it looks like you need a running copy of exiftool, which is a bit of a faff
# https://pypi.org/project/av/: once again, linking problems
# http://www.pymedia.org/tut/ pymedia -- not installable via pip, can download an .exe installer... but it requires python 2.7
# https://pypi.org/project/hachoir-metadata/1.3.3/#description ran into install problems
# understanding the windows date field: https://superuser.com/questions/147525/what-is-the-date-column-in-windows-7-explorer-it-matches-no-date-column-from/335901#335901
# mp4file https://github.com/billnapier/mp4file/blob/master/src/example.py

#files = 'E:\\ubuntu photos\\2015\\P1030793.MP4'
#infile = open(files, 'r')
#with exiftool.ExifTool() as et:
#    metadata = et.get_metadata(files)
#    print metadata

"""
filename = 'E:\\ubuntu photos\\2015\\P1030793.MP4'
created = os.stat(filename).st_ctime
dtstring = str(dt.fromtimestamp(created))
# file date format will be YYYY-MM-DD HH:MM:SS
y = int(dtstring[0:4])
m = int(dtstring[5:7])
d = int(dtstring[8:10])
print(filename + ": " + "created date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))
		
modified = os.stat(filename).st_mtime
dtstring = str(dt.fromtimestamp(modified))
# file date format will be YYYY-MM-DD HH:MM:SS
y = int(dtstring[0:4])
m = int(dtstring[5:7])
d = int(dtstring[8:10])
print(filename + ": " + "modified date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))

accessed = os.stat(filename).st_atime
dtstring = str(dt.fromtimestamp(accessed))
# file date format will be YYYY-MM-DD HH:MM:SS
y = int(dtstring[0:4])
m = int(dtstring[5:7])
d = int(dtstring[8:10])
print(filename + ": " + "accessed date " + dtstring + ": d,m,y = " + str(d) + "," + str(m) + "," + str(y))
"""

#import atom
#from mp4file.mp4file import Mp4File

#file = mp4file.Mp4File('E:\\ubuntu photos\\2015\\P1030793.MP4')

exit()


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








