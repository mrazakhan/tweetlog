'''
This python scripts takes in the input directory containing 
the python dumps and then copies each file in the directory
into mongodb

After loading the data into mongodb the input file is moved 
from the input directory to the output directory

Additionally, for each user we want to download the information
about his friends and followers as well

'''

import pymongo
import os
connection = pymongo.Connection("localhost", 27017)
tweets_db = connection.tweets
debug=1
def LoadToMongo(input_dir,output_dir):
	# for each file
	# skip the first line as it contains the header
	# put rest of the ines to the mongodb

	files=[]
	for (dirpath, dirnames, filenames) in os.walk(input_dir):
		f.extend(filenames)
		break
	
	for f in files:
		
	
	
if __name__=='__main__':
	
	prog_name, input_dir,output_dir=argv
	
	if debug==1:
		print ' %s called , input_dir: %s, output_dir: %s' %(prog_name, input_dirm output_dir)

	LoadToMongo(input_dir, output_dir)	
	
