"""
Version 2 does not use tweepy

"""
#!/usr/bin/env python
import sys, os
import traceback
import csv
import twitter
from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

import datetime
import dateutil.tz
from sys import argv

consumer_key="P8joRY0TqzliQOijOeAZvQ"
consumer_secret="XWdgCqhh77jA9U2orKsLJBNK8C8h4qwYesiOi61goM"
access_token="2246602044-bst3A05437YMnVTMvbpMwx5ztNZFlViYznUp5EU"
access_secret="PptUTWU320Cif1yMhkrN7gUhYGcohvq0V4I3BeVajFavH111"
token_file = '../out/twitter.oauth'
token_path ='../out/'
out_path='../dump/'
app_name = 'SeattleLog'

debug=1
files_per_tweet=10
words = 'seattle'
"""
Login method requires to enter a pin code only once then it stores it in a file that can be used again and again
"""

def login():
	try:
		(oauth_token, oauth_token_secret)= read_token_file(token_file)
	except IOError, e:
		(oauth_token, oauth_token_secret)=oauth_dance (app_name, consumer_key, consumer_secret)

	if not os.path.isdir(token_path):
		os.mkdir(token_path)
	
	write_token_file(token_file, oauth_token, oauth_token_secret)

	return twitter.Twitter(domain ='api.twitter.com', api_version='1.1', auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret, consumer_key, consumer_secret))

def get_twitter_stream():

	try:
		(oauth_token, oauth_token_secret)= read_token_file(token_file)
	except IOError, e:
		(oauth_token, oauth_token_secret)=oauth_dance (app_name, consumer_key, consumer_secret)

		if not os.path.isdir(token_path):
			os.mkdir(token_path)
	
		write_token_file(token_file, oauth_token, oauth_token_secret)

	return twitter.TwitterStream(auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret, consumer_key, consumer_secret))
	
def dump_tweets(log_file=0):
	tweetlist=[]
	tweetfieldset=set()

	
	ts = get_twitter_stream()


	res = ts.statuses.filter(track=words)
	
	for r in res:
		if (len(tweetlist)<files_per_tweet):
			print len(tweetlist),
			tweetlist.append(r)
			tweetfieldset = tweetfieldset.union(r.keys())

			if debug==1:
				if r[u'text']:
					print (r[u'text'])
		else:
			break
	
	datetime_now=datetime.datetime.now().strftime("%H:%M_%m-%d-%Y")

	if log_file==1:
		if not os.path.isdir(out_path):
			os.mkdir(out_path)

		localtz = dateutil.tz.tzlocal()
		tzn=localtz.tzname(datetime.datetime.now())

		fname = out_path+datetime_now+'-'+tzn+'.json'

		f = open(fname, 'w')

		#dw = csv.DictWriter(f, fieldnames = list(tweetfieldset))

		#dw.writeheader()

		for r2 in tweetlist:
		#	dw.writerow({k:v.encode('utf8') if isinstance(v,unicode) else v for k,v in r2.items()}) 
			items=[]
			for k, v in r2.items():
				val =v.encode('utf8') if isinstance(v,unicode) else v
				items.append('{0}:{1}'.format(k,val))
			f.write(','.join(items)+'\n')		
		f.close()




if __name__ == '__main__':

	log_file=0
	if(len(argv)>1):
		log_file=int(argv[1])
		print ' Setting log_file to ', log_file
	while True:
		try :
			dump_tweets(log_file)
		except Exception as e:
			traceback.print_exc()
