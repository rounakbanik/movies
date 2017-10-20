import requests
import bs4
import sys
import os
import time
import json
from api import API_KEY
from pprint import pprint

base_url = "https://api.themoviedb.org/3/movie/"

json_file = open('../data/recommendation_metadata.json', 'a')

beginning = int(input("Enter Opening Page: "))
end = int(input("Enter Closing Page: "))

with open('data/links.csv', 'r') as f:
	for count,line in enumerate(f):
		if count > beginning and count <= end:
			line = line.split(',')
			tmdbId = line[2]
			if len(tmdbId) == 0:
				print("Movie doesn't exist is TMDB Database.")
				continue
			url = base_url + tmdbId + "/recommendations"  + "?api_key=" + API_KEY

			print("Requesting Movie Number: " + str(count))
			res = requests.get(url)

			if res.status_code == 404:
				print("Movie doesn't exist is TMDB Database.")
				continue
			elif res.status_code == 500:
				print("Internal Server Error.")
				continue
			elif res.status_code == 429:
				print("Time out. Waiting for 10 seconds")
				time.sleep(10)
				res = requests.get(url)
			else:
				res.raise_for_status()

			js = dict(json.loads(res.text))
			js["id"] = tmdbId
			json_file.write(str(json.dumps(js)))
			#pprint(json.loads(res.text))



json_file.write(' ]')
json_file.close()


