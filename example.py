from pynimeapi import PyNime

# Init the API
api = PyNime(base_url="https://gogoanimeapp.com")

# Search an anime
anime_title = input("Input anime title: ")
search_result = api.search_anime(anime_title=anime_title)

# check if we found anime we want
if search_result is None:
    raise SystemExit(0)

# Print anime found
for i, animes in enumerate(search_result):
    print(f"{i} | {animes.title}")

# Select anime from serach result
anime_selection = int(input("Select anime: "))

# Get anime details from given category url
anime_details = api.get_anime_details(anime_category_url=search_result[anime_selection].category_url)
print(anime_details.title)
print(anime_details.season)
print(anime_details.synopsis)
print(anime_details.genres)  # output on list data type. Example : ['Comedy', 'Ecchi', 'Slice of Life']
print(anime_details.released)
print(anime_details.status)
print(anime_details.image_url)

# Get urls for available episodes
# return list of urls
episode_urls = api.get_episode_urls(anime_category_url=search_result[anime_selection].category_url)

## Print all episodes urls
for i, url in enumerate(episode_urls):
    print(f"{i + 1} | {url}")

## Select episode
episode_selection = int(input("Select episode: ")) - 1

## look for stream urls
stream_urls = api.get_stream_urls(anime_episode_url=episode_urls[episode_selection])
print(stream_urls)  # output as json, keys are resolution of the stream video

## fast query for grabbing stream url
grab_stream_url = api.grab_stream(anime_details.title, episode=1, resolution=1080)
print(grab_stream_url)

'''
Download function is now depreciated, will be fixed in the future
'''
# Download video. Video will be saved as TS file format.
# print(f"Available resolution : {list(stream_urls.keys())}")
# resolution = str(input("Select resolution: "))
# api.download_video(stream_url = stream_urls[resolution], filename = f"{anime_details.title}_EP{episode_selection + 1}_{resolution}p")

# Get recent uploaded anime
recent_anime = api.get_recent_release(page=1)

for anime in recent_anime:
    # print first 20 anime recently uploaded on GoGoAnime homepage
    print(f"{anime.title} [EP : {anime.latest_episode}] [URL : {anime.latest_episode_url}]")

# Get Schedule
api.get_schedule()
