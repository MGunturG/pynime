import re
import json
import requests

from datetime import datetime
from collections import defaultdict

from pynimeapi.classes.datatype import *
from pynimeapi.classes.color import bcolors

class GetSchedule:
	def __init__(self):
		# anilist API backend URL
		self.url = "https://graphql.anilist.co"

		# GraphQL Query for anime schedule
		self.gql = """query (
		        $weekStart: Int,
		        $weekEnd: Int,
		        $page: Int,
		){
		    Page(page: $page) {
		        pageInfo {
		                hasNextPage
		                total
		        }
		        airingSchedules(
		                airingAt_greater: $weekStart
		                airingAt_lesser: $weekEnd
		        ) {
		            id
		            episode
		            airingAt
		            timeUntilAiring
		            media { title { userPreferred } }
		            media { status }
		        }
		    }
		}"""


	def arrange_template(self, data):
		''' Convert JSON data from iter_schedule to Python dictonary fromat. '''
		template = defaultdict(lambda: defaultdict(list))

		for airing in data[::1]:
			datetime_object = datetime.fromtimestamp(airing.get("airingAt", 0))
			template[format(datetime_object, "%b. %d, %A")][
				(format(datetime_object, "%X"), datetime_object)
			].append({
				"name": airing.get("media", {}).get("title", {}).get("userPreferred"),
				"episode": airing.get('episode', 0)
				})

		return template


	def iter_schedule(self, unix_time: int):
		''' Getting anime schedule via Anilist using their GraphQL API. '''
		page = 1
		data = {} # Empty dict for storing temp data

		query = self.gql
		week_start = unix_time	# current date
		week_end = unix_time + 24 * 7 * 60 * 60 # date for 7 days from today

		# Getting JSON data from Anilis GraphQL API
		while data.get("pageInfo", {}).get("hasNextPage", True): # Loop until there is no more anime schedule on the API return
			schedule_data = requests.post(
				self.url,
				json = {
					"query": query,
					"variables": {
						"weekStart": week_start,
						"weekEnd": week_end,
						"page": page
					}
				}
			)

			data = schedule_data.json().get("data", {}).get("Page", {})
			page += 1

			yield from data.get("airingSchedules", [])


	def print_schedule(self, unix_time: int):
		for date_format, child_component in self.arrange_template(list(self.iter_schedule(unix_time))).items():
			print(f"{bcolors.HEADER}[>] On {date_format} {bcolors.ENDC}") # Print date and days
			
			# Code below for prints airing time and title of anime airing that time
			for (time_format, _), anime_component in sorted(
				child_component.items(),key = lambda component: component[0][1], reverse = False):
				print(f"\t{time_format} - {{}}".format(
					"\n\t\t - ".join(f"{anime['name']} [{anime['episode']}]" for anime in anime_component)))
				'''
				Expected output from this function:
				00:00:00 - Anime_Title [Next_Airing_Episode]
				'''
