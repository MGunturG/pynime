import time
from pynimeapi import PyNime

# Init the API
# api = PyNime(
#     auth = "your auth code from cookie",
#     gogoanime = "your gogoanime code from cookie",
#     base_url = "https://gogoanime.dk")

# Init the API
api = PyNime(
    auth = "KbjxHAyV4c6jhfHbI2mLM6Z278Nm40FTiIv8xOdV6QxHkcDS10PoVMGCsrS2NXsZpdQNivMfLU7P95mqT4PhcA%3D%3D",
    gogoanime = "9a8atlbsbl69dfhb0g332ok383",
    base_url = "https://gogoanime.ee")

# Search an anime
anime_title = input("Input anime title: ")
search_result = api.search_anime(anime_title)

## Print anime found
for i in search_result: 
    print(f"{i.title}")


## Select anime from serach result
anime_selection = int(input("Select anime: ")) - 1


# Get anime details from given category url
anime_details = api.get_anime_details(search_result[anime_selection].category_url)
print(anime_details.title)
print(anime_details.season)
print(anime_details.synopsis)
print(anime_details.genres)     # output on list data type. Example : ['Comedy', 'Ecchi', 'Slice of Life']
print(anime_details.released)
print(anime_details.status)
print(anime_details.image_url)


# Get urls for available episodes
# return list of urls
episodes = api.get_episode_urls(search_result[anime_selection].category_url)

## Print all episodes urls
for i in episodes:
    print(i)

## Select episode
episode_selection = int(input("Select episode: ")) - 1


# Get download link from given episode url
download_link = api.get_download_link(episodes[episode_selection])
print(download_link.link_360)
print(download_link.link_480)
print(download_link.link_720)
print(download_link.link_1080)


# Downloading a video
file_name = f'{anime_details.title} - Episode {episode_selection + 1}' # You can edit this
api.download_video(download_link.link_360, file_name) # Downloading 360p video

## or just use grab_download fucntion for fastest query
## it will return download link in string type
download_link = api.grab_download("chanisaw man", 1, 1080)

# Get Schedule
api.get_schedule(int(time.time()))