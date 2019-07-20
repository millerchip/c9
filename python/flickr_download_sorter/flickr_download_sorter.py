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


# Algorithm <-- OLD APPROACH: UPDATE WITH APPROACH USING SQLITE3 DATABASE
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

import sqlite3

conn = sqlite3.connect('E:\\python_sqlite3.db')
c = conn.cursor()
c.execute('SELECT json_data.id, json_data.filepath, json_data.date, image_data.name from json_data INNER JOIN image_data ON json_data.id = image_data.id')
table = c.fetchall()
for row in table:
	# print(row)
	print("id = " + row[0] + ", name = " + row[1] + ", date = " + row[2] + ", path = " + row[3]) # TODO order???
#row = c.fetchone()
#print(row)

exit()

print("Create a database, if it's not already there")
conn = sqlite3.connect('E:\\python_sqlite3.db')
sql_create_json_data_table = """ CREATE TABLE IF NOT EXISTS json_data (
                                        id text PRIMARY KEY,
                                        filepath text NOT NULL,
                                        date text NOT NULL
                                    ); """

sql_create_image_data_table = """ CREATE TABLE IF NOT EXISTS image_data (
                                        id text PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

print("Create tables, if needed")
if conn is not None:
	# create projects table
	print("create tables")
	c = conn.cursor()
	c.execute(sql_create_json_data_table)
	c.execute(sql_create_image_data_table)
	conn.commit()
	# conn.close()
else:
	print("Error! cannot create the database connection.")

# Location of all flickr exported files
flickr_root = "E:\\flickr downloads\\"

# Location for the JSON data
flickr_photo_json_dir = flickr_root + "account data 72157705005691311_265466abac07_part1\\"

# Probably don't need this, I think all files exported from flickr are .jpg
graphics_extensions = ["JPG", "DB", "AVI", "WAV", "GIF", "JP_", "MOV", "PNG", "MP4", "JPEG", "BMP", "MTS", "PEF"]

##################
print("Parse all the JSON files, create list of elements, each of which is a triple (id, name, date_taken)")

# "id": "2071343962" <-- file in flickr export will include this (format seems to roughly be 'name'_'id'_o.jpg, but name is processed (eg, lower case, non-alphabetic characters converted to alphabetic))
# "name": "Enhanced Box Three (60)" <-- original filename, without extension
# eg, enhanced-box-three-60_2071343962_o.jpg

json_files = []
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

print("Write data from JSON files into json_data table")
for f in json_files:
	# TODO process file
	# dir_end = f.rfind('\\') + 1
	# print("Dir = -->" + f[0:dir_end] + "<--; filename = -->" + f[dir_end:] + "<--") 
	
	with open(f) as json_file:  
		data = json.load(json_file)
		id = data['id']
		name = data['name']
		date_taken = data['date_taken']
		
		insert_statement = 'INSERT INTO json_data VALUES(\'' + id + "\', \'" + name + "\', \'" + date_taken + "\')"
		# print(insert_statement)
		c.execute(insert_statement)
	i += 1
	if i % perc == 0:
		print(str(int(i/perc))+"%")
	# testing
	# if i > 100:
	# 	break


# Now commit data to database
conn.commit()

##################

print("Parse all image files, create list of elements (photo_data), each of which is a double (id, full_path_filename)")
# - find 'id' embedded in the filename : eg, in enhanced-box-three-60_2071343962_o.jpg, id is 2071343962
image_files = []
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

print("Write image data into image_data table")
for f in image_files:
	# TODO process file
	# dir_end = f.rfind('\\') + 1
	# print("Dir = -->" + f[0:dir_end] + "<--; filename = -->" + f[dir_end:] + "<--") 
	last_underscore = f.rfind('_') + 1
	truncated_f = f[:last_underscore-1]
	penultimate_underscore = truncated_f.rfind('_') + 1
	id = truncated_f[penultimate_underscore:]
	# print("id = " + id + "; f = " + f)
	insert_statement = 'INSERT INTO image_data VALUES(\'' + id + "\', \'" + f + "\')"
	# print(insert_statement)
	c.execute(insert_statement)

	i += 1
	if i % perc == 0:
		print(str(int(i/perc))+"%")
	# testing
	# if i > 100:
	# 	break

# Now commit data to database
conn.commit()

# Close DB comnection
conn.close()

print("Done")

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








