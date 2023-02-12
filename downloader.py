import praw
from prawcore import exceptions
import config
import requests
import os.path
from os import path

# Setup login
reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    password=config.password,
    username=config.username,
    user_agent="Image Downloader for r/EarthPorn v1.0 by byipb"
)
try:
    sub_name = input("Enter subreddit: ")
    sub_exists_list = reddit.subreddits.search_by_name(sub_name, include_nsfw=True, exact=True)
except exceptions.NotFound:
    print("Subreddit: r/"+sub_name+" does not exist.")
       
       
sub_url = "https://www.reddit.com/r/"+sub_name+"/.json"

# Request for JSON of page URL
resp = requests.get(sub_url, headers = {'User-agent': 'byipb imgdl v1.0'}).json()

# Parse JSON
# 1. get proper URLs from response
# 2. remove 'amp;' from all links as these return 403 errors
# 3. write image to file 

# JSON structure of reddit as of January 17, 2023
# ['data']['children'][0]['data']['preview']['images'][0]['source']['url']

# children is a list
# data is a dict | note: there are 2 different 'data' references, this is the second
# preview is a dict
# images is a list

request = resp['data']['children']
img_count = 0
overwrite = ''

for data in request:
	if 'preview' in data['data']:
		for images in data['data']['preview']['images']:
			init_url = images['source']['url']
			clean_url = init_url.replace('amp;','')
						
			if (path.isfile('./images/image%s.jpg' % img_count) and overwrite != 'y'):

				# Skip if filename already exists and user chose to not overwrite previously
				if (overwrite=='n'):
					continue

				overwrite = input('A file named '+'image%s.jpg ' % img_count+'already exists, do you wish to overwrite all files with existing filenames? [y/n] \n')
				if (overwrite=='y'):
					pass
				elif (overwrite=='n'):
					continue
			else:
				continue
					
			# Get image from URL and write to file
			img_data = requests.get(clean_url, stream=True)
			with open('./images/image%s.jpg' % img_count, 'wb') as out_file:
				out_file.write(img_data.content)
			print(clean_url)
	img_count+= 1
	
# possible future ideas:
# - add user input for sub_name [DONE]
# - add checks for images on first page of subreddit
# - add check for existing filename [DONE]
# - put result images in a separate folder [DONE]