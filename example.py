from pynimeapi import PyNime


# Init the API
api = PyNime(
    auth = "Your auth token",
    gogoanime = "Your gogoanime token",
    base_url = "https://gogoanime.ee")


# Search Anime
anime_title = input("Input anime title: ")
search_result = api.search_anime(anime_title)
anime_selection = int(input("Select anime: ")) - 1


# Get Anime Details
anime_details = api.get_details(search_result[anime_selection].url)
print(f'Details of {search_result[anime_selection].title}')
print(anime_details.season)
print(anime_details.synopsis)
print(anime_details.genres)
print(anime_details.released)
print(anime_details.status)
print(anime_details.image_url)


# Get Episode Link
anime_links = api.get_eps_links(search_result[anime_selection].url)
print(f'Total Episode available : {len(anime_links)}') # Get total episode available

# Print all links to their episodes (not video download link)
for i in anime_links: 
	print(i)

episode_selection = int(input("Select episode: ")) - 1


# Get Download Link
download_link = api.get_download_link(anime_links[episode_selection])
print(download_link.link_360)
print(download_link.link_480)
print(download_link.link_720)
print(download_link.link_1080)