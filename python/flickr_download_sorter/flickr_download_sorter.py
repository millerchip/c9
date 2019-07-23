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

import re

import sqlite3

#################################
# Algorithm <-- OLD APPROACH: UPDATE WITH APPROACH USING SQLITE3 DATABASE
# Parse all the JSON files, create table of (photo_id, name, date_taken)
# Parse all image files, create table of (photo_id, full_path_filename) 
# Parse all sorted photos, create table of (unique ID, filepath, name)
# TODO 
# Join JSON_data and image_data on photo_id
# - find 'id' embedded in the filename : eg, in enhanced-box-three-60_2071343962_o.jpg, id is 2071343962
# Go through all photo_data:
# - look this photo_data.id up in the json_data, find name and date_taken
# - check for matching image in sorted photos:
#   - identify folder that should contain the image <-- NOTE WILL NEED TO ACCOUNT OF MANUALLY RENAMED FOLDERS (IN RECENT YEARS)
#   - if no folder, then create folder 
#   - if no matching image in target folder, then copy into the folder. 
#     Match might be complicated: hopefully can do a name match, but might also need to match against filesize.
#################################

# Extensions for graphics files, that we'll want to process
graphics_extensions = ["JPG", "DB", "AVI", "WAV", "GIF", "JP_", "MOV", "PNG", "MP4", "JPEG", "BMP", "MTS", "PEF"]

# Location of all flickr exported files
flickr_root = "E:\\flickr downloads\\"

# Root folder for existing sorted photos
sorted_photos_dir = "D:\\sorted_photos\\"

################
# MAIN PROGRAM #
################

# Create database connection, and cursor
conn = sqlite3.connect('E:\\python_sqlite3.db')
if conn is not None:
	c = conn.cursor()
else:
	print("Error! cannot create the database connection.")
	exit()

# create table of all images in sorted_photos
def create_sorted_photos_table ():
	print("Start create_sorted_photos_table")

	# SQL to create a table, if needed
	sql_create_table = """ CREATE TABLE IF NOT EXISTS sorted_photos (
											id int PRIMARY KEY,
											filepath text NOT NULL,
											name text NOT NULL
										); """

	# Check DB connection and cursor set up OK
	if conn is None:
		print("Database connection not properly set up")
		return None
	if c is None:
		print("Database cursor not set up")
		return None

	# Create table
	c.execute(sql_create_table)
	conn.commit()

	# Now write the full list of photos into the table
	# r=root, d=directories, f = files
	i = 0
	for r, d, f in os.walk(sorted_photos_dir):
		for file in f:
			extension_end = file.rfind('.') + 1
			extension = file[extension_end:].upper()
			if (extension in graphics_extensions):
				i += 1
				# Take care of apostrophes in path (in theory they could be in filename too, but in practice they're not)
				insert_statement = "INSERT INTO sorted_photos VALUES(" + str(i) + ", \"" + r.replace("\'","\\\'") + "\", \"" + file + "\")"
				# print(insert_statement)
				c.execute(insert_statement)
				# commit every hundred records
				if i % 1000 == 0:
					print("Records written: " + str(i))
					conn.commit()
				
	# Commit any remaining changes to database
	conn.commit()

	print("Finished create_sorted_photos_table; total records written = " + str(i))
	return None


# create table of data from the JSON files
def create_json_data_table ():
	print("Start create_json_data_table")
	# Location for the JSON data
	flickr_photo_json_dir = flickr_root + "account data 72157705005691311_265466abac07_part1\\"

	# SQL to create a table, if needed
	sql_create_table = """ CREATE TABLE IF NOT EXISTS json_data (
										photo_id text PRIMARY KEY,
										name text NOT NULL,
										date text NOT NULL
                                    ); """

	# Check DB connection and cursor set up OK
	if conn is None:
		print("Database connection not properly set up")
		return None
	if c is None:
		print("Database cursor not set up")
		return None

	# Create table
	c.execute(sql_create_table)
	conn.commit()

	# print("Parse all the JSON files, create list of elements, each of which is a triple (id, name, date_taken)")
	# "id": "2071343962" <-- file in flickr export will include this (format seems to roughly be 'name'_'id'_o.jpg, but name is processed (eg, lower case, non-alphabetic characters converted to alphabetic))
	# "name": "Enhanced Box Three (60)" <-- original filename, without extension
	# eg, enhanced-box-three-60_2071343962_o.jpg

	json_files = []
	# r=root, d=directories, f = files
	# First find all the date information: create an array of [id, creation_date] pairs
	print("Find all JSON files")
	for r, d, f in os.walk(flickr_photo_json_dir):
		for file in f:
			if (file[0:6] == "photo_"):
				# this is JSON file, with date information
				json_files.append(os.path.join(r, file))
	
	print("Write data from JSON files into json_data table")
	i = 0
	for f in json_files:
		# TODO process file
		# dir_end = f.rfind('\\') + 1
		# print("Dir = -->" + f[0:dir_end] + "<--; filename = -->" + f[dir_end:] + "<--") 
		
		with open(f) as json_file:  
			i += 1
			data = json.load(json_file)
			id = data['id']
			name = data['name']
			date_taken = data['date_taken']
			
			insert_statement = 'INSERT INTO json_data VALUES(\'' + id + "\', \'" + name + "\', \'" + date_taken + "\')"
			# print(insert_statement)
			c.execute(insert_statement)
			# commit every hundred records
			if i % 100 == 0:
				print("Records written: " + str(i))
				conn.commit()
				
	# Commit any remaining changes to database
	conn.commit()

	print("Finished create_json_data_table; total records written = " + str(i))
	return None


# create table of all images in flickr_root
def create_images_data_table ():
	print("Start create_images_data_table")

	# SQL to create a table, if needed
	sql_create_table = """ CREATE TABLE IF NOT EXISTS image_data (
											photo_id text PRIMARY KEY,
											path_plus_name text NOT NULL
										); """

	# Check DB connection and cursor set up OK
	if conn is None:
		print("Database connection not properly set up")
		return None
	if c is None:
		print("Database cursor not set up")
		return None

	# Create table
	c.execute(sql_create_table)
	conn.commit()

	# print("Parse all image files, create list of elements (photo_data), each of which is a double (id, full_path_filename)")
	image_files = []
	# r=root, d=directories, f = files
	# First find all the date information: create an array of [id, creation_date] pairs
	for r, d, f in os.walk(flickr_root):
		for file in f:
			extension_end = file.rfind('.') + 1
			extension = file[extension_end:].upper()
			if (extension in graphics_extensions):
				# this is an image file
				image_files.append(os.path.join(r, file))

	# print (image_files)

	# print("Write image data into image_data table")
	i = 0
	for f in image_files:
		i += 1
		# find 'id' embedded in the filename : eg, in enhanced-box-three-60_2071343962_o.jpg, id is 2071343962
		last_underscore = f.rfind('_') + 1
		truncated_f = f[:last_underscore-1]
		penultimate_underscore = truncated_f.rfind('_') + 1
		id = truncated_f[penultimate_underscore:]
		# print("id = " + id + "; f = " + f)
		insert_statement = 'INSERT INTO image_data VALUES(\'' + id + "\', \'" + f + "\')"
		# print(insert_statement)
		c.execute(insert_statement)
		# commit every hundred records
		if i % 100 == 0:
			print("Records written: " + str(i))
			conn.commit()
				
	# Commit any remaining changes to database
	conn.commit()

	print("Finished create_images_data_table; total records written = " + str(i))
	return None


# populate tables
# uncomment to re-create tables; note however that these subroutines don't blank out the tables, so do that by hand (or modify the code)
# create_sorted_photos_table()
# create_json_data_table()
# create_images_data_table()


#DEVELOPMENT WORK BELOW HERE

"""
# Find all the non-JPG files
c.execute('SELECT * FROM image_data WHERE name NOT LIKE \'%.jpg\'')
table = c.fetchall()
for row in table:
	print(row)
	# print("id = " + row[0] + ", name = " + row[1] + ", date = " + row[2] + ", path = " + row[3]) # TODO order???
"""

c.execute('SELECT json_data.photo_id, json_data.name, json_data.date, image_data.path_plus_name from json_data INNER JOIN image_data ON json_data.photo_id = image_data.photo_id')
table = c.fetchall()
i = 0
for row in table:
	i += 1
	print(row)
	# print("id = " + row[0] + ", name = " + row[1] + ", date = " + row[2] + ", path = " + row[3]) # TODO order???
	if i > 5:
		break
#row = c.fetchone()
#print(row)


print ("done")

# Close DB comnection
conn.close()

exit()








