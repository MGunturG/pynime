# PyNime
## _Yet simple API wrapper for GoGoAnime_
PyNime is a (simple) straightforward Python3 script to scrape GoGoAnime using Python.
The project is a work in progress, not finished yet. But, the code works well, feel free to take part of the code.

### What can be done
* Search anime by name
* Get anime details
* Get airing episode urls
* Get streaming url (m3u8)
* Show airing schedule
* Download anime

### Getting Started
~~#### Pre-Requisites~~
* ~~#### Get Auth and Gogoanime token~~
    * ~~Go visit GoGoAnime~~
    * ~~Create an account (please use temp mail)~~
    * ~~Do a verification stuff until you can login~~
    * ~~After login, open Web Developer Tools (CTRL + SHIFT +I)~~
    * ~~Go to Storage Inspector~~
    * ~~Look for Auth and Gogoanime cookies~~
> ~~You can use this library without getting GoGoAnime cookies/token, this cookies/token necessary for only getting [download links](https://github.com/yoshiumikuni/pynime#get-download-link), otherwise no need.~~

> We no longer use user cookies login details, for privacy.

### Example Usage of API

#### Authorize the API
First, you need to initialize the PyNime class.

```Python
from pynimeapi import PyNime
api = PyNime(base_url = "https://gogoanime.ar")
```

>**Note:** GoGoAnime often change their domain, you can change the `base_url` if they change it. Otherwise, leave it blank. The default URL will refer to https://gogoanime.ar


#### Search an Anime
You can search anime by title using `search_anime`. It will ~~print anime that found and~~ return result as `SearchResultObj` which contains two argument `title` and `url`.

```Python
...
search_result = api.search_anime(anime_title = "yofukashi no uta")

# print list
for i in search_result:
    print(i.title) # or
    print(i.url)
```

>**Note:** `.url` is an URL to anime details page. Used for function that need `anime_category_url` as input.


#### Get Anime Details
You can get a basic details of anime using `get_anime_details` function. It will return anime details as `AnimeDetailsObj`.
Details of anime contains :
* title
* season
* synopsis
* genres
* released
* status
* image_url

```Python
...
search_result = api.search_anime(anime_title = "yofukashi no uta")

details = api.get_anime_details(search_result[0].url) # using search_result on index 0
print(details.genres)
print(details.status) # and more...
```

>**Note:** Function `get_anime_details` input argument is `anime_category_url` which need anime details page URL.


#### Get Anime Episode URLs
Get total of anime episode available and url per episode using `get_episode_urls`. Will return list of URLs.

```Python
...
search_result = api.search_anime(anime_title = "yofukashi no uta")

episode_urls = api.get_episode_urls(anime_category_url = search_result[0].url) # again, using search_result on index 0
print(episode_urls[0]) # link to episode 1
print(episode_urls[1]) # link to episode 2
# and more... (array start from 0 btw)

# to get total episode available just call len()
print(len(episode_urls)) # 12
```
#### Get Streaming URLs
Get streaming URL. The URL is link to M3U8 file. We have two function for this.
```Python
...
# First function
stream_urls = api.get_stream_urls(anime_episode_url = episodes[episode_urls[0]) # get streaming URL for first episode
print(stream_urls) # output as json, keys are resolution of the stream video

# Second fucntion
# this function just a simple way to get streaming URL
grab_stream_url = api.grab_stream(anime_title = "yofukashi no uta", episode = 1, resolution = 1080)
print(grab_stream_url)
```
#### Download
To be clear, using internal downloader (this function) might be have slow download speed. I recommend user to copy link download and download the file using external downloader.
```Python
...
resolution = 1080
episode_selection = 1
api.download_video(stream_url = stream_urls[resolution], filename = f"{details.title}_EP{episode_selection}_{resolution}p")
```

>**Note:** Recommended download manager XTREME DOWNLOAD MANAGER (XDM). Github : https://github.com/subhra74/xdm
#### Get Schedule
Get the schedule from today to a week ahead.

```python
import time
...
current_time = int(time.time())
api.get_schedule(current_time) # just simple call
```

>**Note:** Need UNIX in integer. Return nothing, this function only print the schedule. Will fix later.
