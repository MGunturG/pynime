# PyNime
## _Yet simple API wrapper for GoGoAnime_
PyNime is a (simple) straightforward Python3 script to scrape GoGoAnime using Python. 
The project is a work in progress, not finished yet. But, the code works well, feel free to take part of the code.

### What can be done
* Search anime by name
* Get anime details
* Get airing episode urls
* Get download and/or streaming url
* Show airing schedule
* Download anime

### Getting Started
#### Pre-Requisites
* #### Get Auth and Gogoanime token
    * Go visit GoGoAnime
    * Create an account (please use temp mail) 
    * Do a verification stuff until you can login 
    * After login, open Web Developer Tools (CTRL + SHIFT +I)
    * Go to Storage Inspector
    * Look for Auth and Gogoanime cookies
> You can use this library without getting GoGoAnime cookies/token, this cookies/token necessary for only getting [download links](https://github.com/yoshiumikuni/pynime#get-download-link), otherwise no need.


### Example Usage of API
#### Authorize the API
First, you need to initialize the PyNime class.

```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
```

>**Note:** GoGoAnime often change their domain, you can change the `base_url` if they change it. Otherwise, leave it blank. The default URL will refer to https://gogoanime.dk


#### Search an Anime
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

>**Note:** `.url` is an URL to anime category/details page.


#### Get Anime Details
You can get a basic details of anime using `get_details`. It will return anime details as `AnimeDetailsObj`.
Details of anime contains :
* title
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

details = api.get_anime_details(search_result[0].url)
print(details.genres)
print(details.status) # and more...
```

>**Note:** `get_anime_details` input argument is `anime_category_link` which need anime category/details page URL, it will return `AnimeDetailsObj`.


#### Get Anime Episode Links
Get total of anime episode available and links per episode using `get_episode_urls` and return list of URLs.

```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
    
search_result = api.search_anime("yofukashi no uta")

episode_links = api.get_episode_urls(search_result[0].url)
print(episode_links[0]) # link to episode 1
print(episode_links[1]) # link to episode 2
# and more... (array start from 0 btw)
```


#### Get Download Link
You can simply get the streamable and downloadable links of a specific episode of an Anime by it's episode URL (get it using `get_episode_urls`). This function will return `DownloadLinkObj`.
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

episode_links = api.get_episode_urls(search_result[0].url)
print(episode_links[0]) # link to episode 1

eps_one_download = api.get_download_link(episode_links[0])
print(eps_one_download.link_360)
print(eps_one_download.link_480)
# and more...
```


#### Quickly Grab Download Link
For `grab_download`, this function will return a download link based on the input. This will simplfy all of function above.

```python
from pynimeapi import PyNime
api = PyNime(
    auth = "your auth code from cookie",
    gogoanime = "your gogoanime code from cookie",
    base_url = "https://gogoanime.dk")
    
result = api.grab_download("yofukashi no uta", episode = 12, resolution = 480)
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
