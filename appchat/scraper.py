import requests
from bs4 import BeautifulSoup as BS
import os

def get_data(query):
	url = 'https://www.youtube.com/results?search_query=' + query
	r = requests.get(url)

	html = r.text
	soup = BS(html)

	h3 = soup.find_all('a', class_='yt-uix-tile-link')
	
	for ix in h3:
		print ix.text, ix['href']

	# 10
	video_url = 'https://www.youtube.com' + h3[10]['href']
	os.system('youtube-dl ' + video_url)


get_data(query='django tutorial')
