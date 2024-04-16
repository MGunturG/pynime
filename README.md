# PyNime
## _Yet simple API wrapper for GoGoAnime_

PyNime is a (simple) straightforward Python3 script to scrape GoGoAnime using Python.

The project is a work in progress, not finished yet. But, the code works well, feel free to take part of the code.

## Status

Please visit [PyNime Benchmark](https://github.com/yoshikuniii/pynime_benchmark) for API status.

## What Can be Done?

- [Search anime by title](https://github.com/yoshikuniii/pynime#1-initialize-the-api)
- [Get anime details](https://github.com/yoshikuniii/pynime#2-search-an-anime)
- [Get airing episode urls](https://github.com/yoshikuniii/pynime#3-get-anime-details)
- [Get streaming url (m3u8)](https://github.com/yoshikuniii/pynime#4-get-anime-episode-urls)
- [Show airing schedule](https://github.com/yoshikuniii/pynime#5-get-streaming-urls)
-  ~~Download anime~~
- [Get schedule](https://github.com/yoshikuniii/pynime#7-get-schedule)
- [Get recent anime](https://github.com/yoshikuniii/pynime#8-extra-get-recent-uploaded-anime)

## Example Usage of API

For complete code, see `example.py`.
<p align="center">
<img src="https://github.com/yoshikuniii/pynime/blob/main/pynimeapi/raw/demo.gif"></p>

## How To Install?
Minimum Python version 3.8+
It will install the dependencies automatically.
```sh
pip install git+https://github.com/yoshikuniii/pynime.git
```

## 1. Initialize the API

First, you need to initialize the PyNime class.

```Python
from pynimeapi import PyNime
api = PyNime(base_url = "https://anitaku.to")
```

> **Note:** GoGoAnime often change their domain, you can change the `base_url` if they change it. Otherwise, leave it blank. The default URL will refer to https://anitaku.to/. More info visit https://gogotaku.info/

## 2. Search an Anime

You can search anime by title using `search_anime`. It will return result as `SearchResultObj` which contains two argument `title` and `category_url`.

```Python
...
search_result = api.search_anime(anime_title = "yofukashi no uta")

# print list
for i in search_result:
    print(i.title) # or
    print(i.category_url)
```

>  **Note:**  `.category_url` is an URL to anime details page. Used for function that need `anime_category_url` as input.  

## 3. Get Anime Details

You can get a basic details of anime using `get_anime_details` function. It will return anime details as `AnimeDetailsObj`.
Details of anime contains :

- title
- season
- synopsis
- genres
- released
- status
- image_url

```Python
...
search_result = api.search_anime(anime_title = "yofukashi no uta")

anime_details = api.get_anime_details(search_result[0].category_url) # using search_result on index 0
print(anime_details.title)
print(anime_details.season)
print(anime_details.synopsis)
print(anime_details.genres) # for genres, output is a list. Example : ['Comedy', 'Ecchi', 'Slice of Life']
print(anime_details.status)
print(anime_details.image_url)
```

>  **Note:** Function `get_anime_details` input argument is `anime_category_url` which need anime details page URL.  

## 4. Get Anime Episode URLs

Get total of anime episode available and url per episode using `get_episode_urls`. Will return list of URLs.

```Python
...
search_result = api.search_anime(anime_title = "yofukashi no uta")

episode_urls = api.get_episode_urls(anime_category_url = search_result[0].category_url) # again, using search_result on index 0
print(episode_urls[0]) # link to episode 1
print(episode_urls[1]) # link to episode 2
# and more... (array start from 0 btw)

# or you can do this instead
for url in episode_urls:
    print(url)

# to get total episode available just call len()
print(len(episode_urls)) # 12
```

## 5. Get Streaming URLs

Get streaming URL. The URL is link to M3U8 file. We have two function for this.

```Python
...
# First function
stream_urls = api.get_stream_urls(anime_episode_url = episode_urls[0]) # get streaming URL for first episode
print(stream_urls) # output as json, keys are resolution of the stream video

# Get available video res
print(list(stream_urls.keys()))

# Second function
# this function just a simple way to get streaming URL
grab_stream_url = api.grab_stream(anime_title = "yofukashi no uta", episode = 1, resolution = 1080)
print(grab_stream_url)
```

## ~~6. Download~~
Download function is now depreciated, will be fixed in the future.

~~To be clear, using internal downloader (this function) might be have slow download speed. I recommend user to copy link download and download the file using external downloader.~~

```Python
...
resolution = 1080
episode_selection = 1  # this means episode 2
api.download_video(stream_url = stream_urls[resolution], filename = f"{anime_details.title}_EP{episode_selection + 1}_{resolution}p")
```

>  ~~**Note:** Recommended download manager XTREME DOWNLOAD MANAGER (XDM). Github : https://github.com/subhra74/xdm~~  

## 7. Get Schedule

Get the schedule from today to a week ahead.

```python
...
api.get_schedule() # just simple call
```

>  **Note:** Need UNIX in integer. Return nothing, this function only print the schedule. Will fix later.  

## 8. Extra, get recent uploaded anime

This function will return 20 anime title of animes in list from GoGoAnime main page.

```Python
...
# Get recent uploaded anime
recent_anime = api.get_recent_release(page=1)

for anime in recent_anime:
# print first 20 anime recently uploaded on GoGoAnime homepage
    print(f"{anime.title} [EP : {anime.latest_episode}] [URL : {anime.latest_episode_url}]")
```
