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
# Parse all the JSON files, create list of elements, each of which is a triple (id, name, date_taken)
# Go through all image files:
# - find 'id' embedded in the filename : eg, in enhanced-box-three-60_2071343962_o.jpg, id is 2071343962
# - look this id up in the array, find name and date_taken
# - check for matching image in sorted photos:
#   - identify folder that should contain the image <-- NOTE WILL NEED TO ACCOUNT OF MANUALLY RENAMED FOLDERS (IN RECENT YEARS)
#   - if no folder, then create folder 
#   - if no matching image in target folder, then copy into the folder. 
#     Match might be complicated: hopefully can do a name match, but might also need to match against filesize.


# Parse all the JSON files, create list of elements, each of which is a triple (id, name, date_taken)
json_files = []
file_data = []
# r=root, d=directories, f = files
# First find all the date information: create an array of [id, creation_date] pairs
for r, d, f in os.walk(flickr_photo_json_dir):
	for file in f:
		if (file[0:6] == "photo_"):
			# this is JSON file, with date information
			json_files.append(os.path.join(r, file))

# print(str(len(json_files)))

# Show progress through the JSON files
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
		file_data.append([id, name, date_taken])
		# print(file_data)
		# print(file_data[0][2]) <-- access date taken
		# exit()
		# image will be named 'name'_'id'_o.jpg (drop name to all lowercase, replace spaces with hyphens)
		# img = str(data['name']).lower().replace(" ","_") + "_" + str(data['id']).lower() + "_o.jpg"
		# print("File (" + str(data['date_taken']) + ") " + f + ": " + img)
	i += 1
	if i % perc == 0:
		print(str(int(i/perc))+"%")

# print(file_data)
	
exit()

extension_end = file.rfind('.') + 1
extension = file[extension_end:].upper()


if (file[extension_end:].upper() in graphics_extensions):
	print("hi")

exit()








