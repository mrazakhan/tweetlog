'''
This python scripts takes in the input directory containing 
the python dumps and then copies each file in the directory
into mongodb

After loading the data into mongodb the input file is moved 
from the input directory to the output directory

Additionally, for each user we want to download the information
about his friends and followers as well

'''
from sys import argv, exit
import pymongo

import json
import os
from bson import json_util
connection = pymongo.Connection("localhost", 27017)
tweets_db = connection.tweets
debug=1
def LoadToMongo(input_dir,output_dir):
	# for each file
	# skip the first line as it contains the header
	# put rest of the ines to the mongodb

	files=[]
	for (dirpath, dirnames, filenames) in os.walk(input_dir):
		files.extend(filenames)
		break
	if not os.path.isdir(output_dir):
		os.mkdir(output_dir)	
	for f in files:
		print ' Processing file %s \n' %(f)
		for r in open(input_dir+f).readlines():
			
			tweets_db.tweets_table.insert(json.loads(r))
	
		os.rename(input_dir+f, output_dir+f)
if __name__=='__main__':
	
	if len(argv)!=3:
		print ' Invalid number of args'
		print ' pt2_mongo.py input_dir output_dir'
		exit(-1)
	prog_name, input_dir,output_dir=argv
	
	if not input_dir.endswith('/'):
		input_dir+='/'

	if not output_dir.endswith('/'):
		output_dir+='/'
	if debug==1:
		print ' %s called , input_dir: %s, output_dir: %s' %(prog_name, input_dir,output_dir)

	LoadToMongo(input_dir, output_dir)	
	
