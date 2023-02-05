import praw
import config
import requests

# Setup login
reddit = praw.Reddit(
    client_id="config.client_id",
    client_secret="config.client_secret",
    password="config.password",
    username="config.username",
    user_agent="Image Downloader for r/EarthPorn v1.0 by byipb"
)

sub_name = "EarthPorn"

# Request for JSON of page URL
resp = requests.get("https://www.reddit.com/r/earthporn/.json", headers = {'User-agent': 'byipb imgdl v1.0'}).json()

# Parse JSON
# 1. get proper URLs from response
# 2. remove 'amp;' from all links as these return 403 errors
# 3. write image to file 

# JSON structure of reddit as of January 17, 2023
# ['data']['children'][0]['data']['preview']['images'][0]['source']['url']

# children is a list
# data is a dict | note: there are 2 different 'data' references, this is the inner one
# preview is a dict
# images is a list

request = resp['data']['children']
img_count = 0

for data in request:
	if 'preview' in data['data']:
		for images in data['data']['preview']['images']:
			init_url = images['source']['url']
			clean_url = init_url.replace('amp;','')
			
			# Get image from URL and write to file
			img_data = requests.get(clean_url, stream=True)
			with open('image%s.jpg' % img_count, 'wb') as out_file:
				out_file.write(img_data.content)
			print(clean_url)
	img_count+= 1
	
# possible future ideas:
# - add user input for sub_name 
# - add checks for images on first page of subreddit
# - add check for existing filename