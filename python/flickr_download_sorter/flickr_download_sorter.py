#! python3

# Some libraries that I imported into the photo sorter (may well need them here as well)
import os
import shutil
import datetime
import time
import sys

import json

from datetime import datetime as dt # don't understand why I need this, but I can't call fromtimestamp without it

current_year = datetime.datetime.now().year

# regex
import re

flickr_root = "E:\\flickr downloads\\"

flickr_photo_json_dir = flickr_root + "account data 72157705005691311_265466abac07_part1\\"

# Probably don't need this, I think all files exported from flickr are .jpg
graphics_extensions = ["JPG", "DB", "AVI", "WAV", "GIF", "JP_", "MOV", "PNG", "MP4", "JPEG", "BMP", "MTS", "PEF"]


# "id": "2071343962" <-- file in flickr export will include this (format seems to roughly be 'name'_'id'_o.jpg, but name is processed (eg, lower case, non-alphabetic characters converted to alphabetic))
# "name": "Enhanced Box Three (60)" <-- original filename, without extension
# eg, enhanced-box-three-60_2071343962_o.jpg

# Algorithm
# Parse all the JSON files, create list of elements (json_data), each of which is a triple (id, name, date_taken)
# Parse all image files, create list of elements (photo_data), each of which is a double (id, full_path_filename) 
# - find 'id' embedded in the filename : eg, in enhanced-box-three-60_2071343962_o.jpg, id is 2071343962
# Go through all photo_data:
# - look this photo_data.id up in the json_data, find name and date_taken
# - check for matching image in sorted photos:
#   - identify folder that should contain the image <-- NOTE WILL NEED TO ACCOUNT OF MANUALLY RENAMED FOLDERS (IN RECENT YEARS)
#   - if no folder, then create folder 
#   - if no matching image in target folder, then copy into the folder. 
#     Match might be complicated: hopefully can do a name match, but might also need to match against filesize.


# Parse all the JSON files, create list of elements, each of which is a triple (id, name, date_taken)
json_files = []
json_data = []
# r=root, d=directories, f = files
# First find all the date information: create an array of [id, creation_date] pairs
for r, d, f in os.walk(flickr_photo_json_dir):
	for file in f:
		if (file[0:6] == "photo_"):
			# this is JSON file, with date information
			json_files.append(os.path.join(r, file))

# Set up for showing progress as we work through the list of files
perc = int(len(json_files)/100)
if (perc == 0):
	perc = 1
i = 0

for f in json_files:
	# TODO process file
	# dir_end = f.rfind('\\') + 1
	# print("Dir = -->" + f[0:dir_end] + "<--; filename = -->" + f[dir_end:] + "<--") 
	
	with open(f) as json_file:  
		data = json.load(json_file)
		id = data['id']
		name = data['name']
		date_taken = data['date_taken']
		json_data.append([id, name, date_taken])
		# print(json_data)
		# print(json_data[0][2]) <-- access date taken
		# exit()
		# image will be named 'name'_'id'_o.jpg (drop name to all lowercase, replace spaces with hyphens)
		# img = str(data['name']).lower().replace(" ","_") + "_" + str(data['id']).lower() + "_o.jpg"
		# print("File (" + str(data['date_taken']) + ") " + f + ": " + img)
	i += 1
	if i % perc == 0:
		print(str(int(i/perc))+"%")
		# break

print(json_data)


# Parse all image files, create list of elements (photo_data), each of which is a double (id, full_path_filename) 
# - find 'id' embedded in the filename : eg, in enhanced-box-three-60_2071343962_o.jpg, id is 2071343962
image_files = []
image_data = []
# r=root, d=directories, f = files
# First find all the date information: create an array of [id, creation_date] pairs
for r, d, f in os.walk(flickr_root):
	for file in f:
		
		if (file[-3:] == "jpg"):
			# this is an image file
			image_files.append(os.path.join(r, file))
# print (image_files)

# Set up for showing progress as we work through the list of files
perc = int(len(image_files)/100)
if (perc == 0):
	perc = 1
i = 0
print("here")
for f in image_files:
	# TODO process file
	# dir_end = f.rfind('\\') + 1
	# print("Dir = -->" + f[0:dir_end] + "<--; filename = -->" + f[dir_end:] + "<--") 
	last_underscore = f.rfind('_') + 1
	truncated_f = f[:last_underscore-1]
	penultimate_underscore = truncated_f.rfind('_') + 1
	id = truncated_f[penultimate_underscore:]
	# print("id = " + id + "; f = " + f)
	image_data.append([id, f])
	i += 1
	if i % perc == 0:
		print(str(int(i/perc))+"%")
		# break
print (image_data)

exit()

for f in image_files:
	with open(f) as image_file:
		# TODO process image
		print("image_file = " + str(image_file))
		# image_data.append([id, full_path_filename])
	i += 1
	if i % perc == 0:
		print(str(int(i/perc))+"%")


exit()








