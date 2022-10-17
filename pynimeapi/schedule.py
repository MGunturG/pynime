import json
import time
import requests

from datetime import datetime
from collections import defaultdict
from pynimeapi.color_classes import bcolors

''' Currently on testing if the schedule are correct because the schedule from this
	API different with schedule form animixplay.

	My assumptions this API return a legal airing schedule, meanwhile GoGoAnime, animixplay, etc
	is not 'LEGAL' anime streaming website so there is some delay for them to adding subtitle and uploading
	the videos.

	There is plus-minus 2h delay. For now, I'll leave just like this.
'''

# GraphQL Query for anime schedule
gql = """query (
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

# anilist API backend URL
url = "https://graphql.anilist.co"


def arrange_template(data):
	''' Convert JSON data from iter_schedule to Python dictonary fromat. '''
	template = defaultdict(lambda: defaultdict(list))

	for airing in data[::1]:
		datetime_object = datetime.fromtimestamp(airing.get("airingAt", 0) + 2 * 60 * 60) # Add 2 hour
		template[format(datetime_object, "%b. %d, %A")][
			(format(datetime_object, "%X"), datetime_object)
		].append({
			"name": airing.get("media", {}).get("title", {}).get("userPreferred"),
			"episode": airing.get('episode', 0)
			})

	return template


def iter_schedule(unix_time):
	''' Getting anime schedule via Anilist using their GraphQL API. '''
	page = 1
	unix_time = int(unix_time)	# current date
	week_end = unix_time + 24 * 7 * 60 * 60 # date for 7 days from today

	variables = {
	"weekStart": unix_time,
	"weekEnd": week_end,	
	"page": page
	}

	data = {}

	# Getting JSON data from Anilis GraphQL API
	while data.get("pageInfo", {}).get("hasNextPage", True): # Loop until there is no more anime schedule on the API return
		schedule_data = requests.post(
			url,
			json = {
				"query": gql,
				"variables": {
					"weekStart": unix_time,
					"weekEnd": week_end,
					"page": page
				}
			}
		)

		data = schedule_data.json().get("data", {}).get("Page", {})
		page += 1

		yield from data.get("airingSchedules", [])

# Print the Schedule

def print_schedule():
	for date_format, child_component in arrange_template(list(iter_schedule(int(time.time())))).items():
		print(f"{bcolors.HEADER}[>] On {date_format} {bcolors.ENDC}") # !! Please make this colorized text output so user can notice the date
		for (time_format, _), anime_component in sorted(
			child_component.items(),key = lambda component: component[0][1], reverse = False):
			print(f"\t{time_format} - {{}}".format( # FORMAT IS ANIME_TITLE [NEXT EPISODE AIRING]
				"\n\t\t - ".join(f"{anime['name']} [{anime['episode']}]" for anime in anime_component)))
			'''
			Expected output from this are 
			00:00:00 - Anime_Title [Next_Airing_Episode]
			'''
		# print("\n")
