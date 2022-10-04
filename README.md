# PyNime
## _Yet simple API wrapper for GoGoAnime_
PyNime is a (simple) straightforward Python3 script to scrape GoGoAnime using Python. 

ToDo:
- [x] Restructure code base to use class code base
- [x] Make downloader (Internal downloader done, but it has slow download speed)
- ~~Play on player like mpv or vlc~~ (I think this function not needed)
- Get top current airing anime (Working on it)

I didn't make this to be able to search by genre, know the popular anime (all time/top ranked anime), and so on. The main purpose of this script is **I want to watch anime on the video player I installed on my computer**, that's all.

I just wanted to make it as simple as possible. If you want anime recommendations, visit anilis, myanimelist, or Reddit (r/AnimeSuggest and others).

The project is still a work in progress, not finished yet. But, the code works well, feel free to take part of the code.

### Getting Started
#### Pre-Requisites
* #### Get Auth and Gogoanime token
    * Go visit GoGoAnime
    * Make an account (please use temp mail) 
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
    auth = "Your auth token",
    gogoanime = "Your gogoanime token",
    base_url = "https://gogoanime.ee")
```
###
>**Note:** GoGoAnime often change their domain, you can change the `base_url` if they change it. Otherwise, leave it blank. The default URL will refer to https://gogoanime.ee


### Search an Anime
You can search anime by title using `search_anime`. It will print anime that found and return result as `SearchResultObj` which contains two argument `title` and `url`.
```python
from pynimeapi import PyNime
api = PyNime(
    auth = "Your auth token",
    gogoanime = "Your gogoanime token",
    base_url = "https://gogoanime.ee")
    
search_result = api.search_anime("yofukashi no uta")

for i in search_result:
    print(i.title) # or
    print(i.url)
```
###
>**Note:** `.url` is an URL to anime category/details page.


### Get Anime Details
You can get a basic details of anime using `get_details`. It will return anime details as `AnimeDetailsObj` or dictonary.
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
    auth = "Your auth token",
    gogoanime = "Your gogoanime token",
    base_url = "https://gogoanime.ee")
    
search_result = api.search_anime("yofukashi no uta")

details = api.get_details(search_result[0].url, desired_output = 'object')
print(details.genres)
print(details.status) # and more...

details = api.get_details(search_result[0].url, desired_output = 'dict')
print(details) # print anime details in dictonary.
```
>**Note:** `get_details` need two input argument.
First argument is `anime_category_link` which need anime category/details page URL. 
Second argument is `desired_output` for selecting the desired output which can accept `object` or `dict`, or leave it blank, the default will return `AnimeDetailsObj`.


### Get Anime Episode Links
Get total of anime episode available and links per episode using `get_eps_links` and return list of URLs.
```python
from pynimeapi import PyNime
api = PyNime(
    auth = "Your auth token",
    gogoanime = "Your gogoanime token",
    base_url = "https://gogoanime.ee")
    
search_result = api.search_anime("yofukashi no uta")

episode_links = api.get_eps_links(search_result[0].url)
print(episode_links[0]) # link to episode 1
print(episode_links[0]) # link to episode 2
# and more...
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
    auth = "Your auth token",
    gogoanime = "Your gogoanime token",
    base_url = "https://gogoanime.ee")
    
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
    auth = "Your auth token",
    gogoanime = "Your gogoanime token",
    base_url = "https://gogoanime.ee")
    
result = api.fast_query("yofukashi no uta", episode = 12, resolution = 480)
print(result)
```
>**Note:** Function will print the possible anime search results (default selection is result number 1) and will return download/streamable link for desired episode and resolution. If desired resolution or episode not available, it will return `None`.