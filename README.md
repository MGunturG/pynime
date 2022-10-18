# PyNime
## _Yet simple API wrapper for GoGoAnime_
PyNime is a (simple) straightforward Python3 script to scrape GoGoAnime using Python. 

ToDo:
- [x] Restructure code base to use class code base
- [x] Make downloader (Internal downloader done, but it has slow download speed)
- ~~Play on player like mpv or vlc~~ (I think this function not needed)
- Get top current airing anime (Working on it)

The project is a work in progress, not finished yet. But, the code works well, feel free to take part of the code.

### Getting Started
#### Pre-Requisites
* #### Get Auth and Gogoanime token
    * Go visit GoGoAnime
    * Create an account (please use temp mail) 
    * Do a verification stuff until you can login 
    * After login, open Web Developer Tools (CTRL + SHIFT +I)
    * Go to Storage Inspector
    * Look for Auth and Gogoanime cookies

### Example Usage of API
###
### Authorize the API
First, you need to initialize the PyNime class. 
```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
```
###
>**Note:** GoGoAnime often change their domain, you can change the `base_url` if they change it. Otherwise, leave it blank. The default URL will refer to https://gogoanime.dk


### Search an Anime
You can search anime by title using `search_anime`. It will print anime that found and return result as `SearchResultObj` which contains two argument `title` and `url`.
```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
    
search_result = api.search_anime("yofukashi no uta")

for i in search_result:
    print(i.title) # or
    print(i.url)
```
###
>**Note:** `.url` is an URL to anime category/details page.


### Get Anime Details
You can get a basic details of anime using `get_details`. It will return anime details as `AnimeDetailsObj`.
Details of anime contains :
* season
* synopsis
* genres
* released
* status
* image_url
```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
    
search_result = api.search_anime("yofukashi no uta")

details = api.get_details(search_result[0].url)
print(details.genres)
print(details.status) # and more...
```
>**Note:** `get_details` input argument is `anime_category_link` which need anime category/details page URL, it will return `AnimeDetailsObj`.


### Get Anime Episode Links
Get total of anime episode available and links per episode using `get_eps_links` and return list of URLs.
```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
    
search_result = api.search_anime("yofukashi no uta")

episode_links = api.get_eps_links(search_result[0].url)
print(episode_links[0]) # link to episode 1
print(episode_links[1]) # link to episode 2
# and more... (array start from 0 btw)
```


### Get Download Link
You can simply get the streamable and downloadable links of a specific episode of an Anime by it's episode URL (get it using `get_eps_links`). This function will return `DownloadLinkObj`.
`DownloadLinkObj` has following arguments.
* link_360
* link_480
* link_720
* link_1080
```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
    
search_result = api.search_anime("yofukashi no uta")

episode_links = api.get_eps_links(search_result[0].url)
print(episode_links[0]) # link to episode 1

eps_one_download = api.get_download_link(episode_links[0])
print(eps_one_download.link_360)
print(eps_one_download.link_480)
# and more...
```


### Fast Query!
For `fast_query`, this function will return a download link based on the input. This will simplfy all of function above.
```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
    
result = api.fast_query("yofukashi no uta", episode = 12, resolution = 480)
print(result)
```
>**Note:** Function will print the possible anime search results (default selection is result number 1) and will return download/streamable link for desired episode and resolution. If desired resolution or episode not available, it will return `None`.


### Get Schedule
Get the schedule from today to a week ahead.
```python
import time
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")

current_time = int(time.time())
    
api.get_schedule(current_time) # just simple call
```
>**Note:** Need UNIX in integer. Return nothing, this funtion only print the schedule. Will fix later.