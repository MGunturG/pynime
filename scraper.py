import re
import json
import requests
from bs4 import BeautifulSoup

from data_classes import *

'''
Client also need to install lxml library

Installaion: pip install lxml

or visit https://pypi.org/project/lxml/ and https://lxml.de/installation.html
'''

baseURL = "https://gogoanime.ee"


def SearchAnime(anime_title: str) -> SearchResultObj:
  '''
  Search anime on given title.
  Output is list of animes in object.

  Example of usage:
  >>> result = SearchAnime("Yofukashi no Uta")
  1 | Yofukashi no Uta
  2 | Yofukashi no Uta (Dub)
  >>> print(len(result))
  2
  >>> result[0].title
  'Yofukashi No Uta'

  '''
  anime_links = []
  anime_title = anime_title.replace(" ", "%20")
  search_page_link = f'{baseURL}/search.html?keyword={anime_title}'
  search_page = requests.get(search_page_link)
  search_page = search_page.content
  soup = BeautifulSoup(search_page, "html.parser")
  result = soup.find_all("div", {"class":"img"})

  for idx, i in enumerate(result):
    # anime_links.append(f'{baseURL}{i.contents[1].get("href")}')
    anime_links.append(SearchResultObj(title=f'{i.contents[1].get("title")}', url=f'{baseURL}{i.contents[1].get("href")}'))
    print(f'{idx+1} | {i.contents[1].get("title")}')

  return anime_links


def GetAnimeDetails(anime_category_link: str, desired_output: str):
  '''
  Get anime info/details.

  Usage of desired_output:
  1. desired_output = "dict"
  2. desired_output = "object"

  If using desired_output as "object" you no need to parse the dictonary,
  just call .title to get anime title

  Example :
  >>> anime_detailsObj = GetAnimeDetails("http://gogoanime.ee/....", desired_output="object")
  >>> print(anime_detailObj.genres)
  ['Romance', 'Ecchi']
  
  
  >>> anime_detailsDict = GetAnimeDetails("http://gogoanime.ee/....", desired_output="dict")
  >>> print(anime_detailDict)
  {
    "season": "Summer 2022 Anime",
    "synopsis": "Plot Summary: Second season of Hataraku Maou-sama!",
    "genres": ["Comedy", "Demons", "Fantasy", "Romance", "Supernatural"],
    "release_year": 2022,
    "status": "Ongoing",
    "total_episode": 12,
    "image_url": "https://gogocdn.net/cover/hataraku-maou-sama-2nd-season.png",
  }

  '''

  detail_page = requests.get(anime_category_link)
  soup = BeautifulSoup(detail_page.text, "html.parser")
  info_body = soup.find("div", {"class": "anime_info_body_bg"})
  image_url = info_body.find("img")["src"]
  other_info = info_body.find_all("p", {"class": "type"})

  season = other_info[0].text.replace("\n", "").replace("Type: ", "")
  synopsis = other_info[1].text.replace("\n", "")
  genres = [
    x["title"]
    for x in BeautifulSoup(str(other_info[2]), "html.parser").find_all("a")
  ]
  released = other_info[3].text.replace("Released: ", "")
  status = other_info[4].text.replace("\n", "").replace("Status: ", "")
  total_episode = len(GetAnimeEps(anime_category_link))
  image_url = image_url

  if desired_output == "dict":
    anime_info_dict = {
        "season": season,
        "synopsis": synopsis,
        "genres": genres,
        "release_year": released,
        "status": status,
        "total_episode": total_episode,
        "image_url": image_url
    }

    return anime_info_dict

  else:
    anime_info_object = AnimeDetailsObj(
      season = season,
      synopsis = synopsis,
      genres= genres,
      released= released,
      status= status,
      total_episode= total_episode,
      image_url = image_url
    )

    return anime_info_object


def GetAnimeEps(anime_category_link: str) -> list:
  '''
  Get total of anime episode available and links per episode

  Expected output (example):
  [
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-1",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-2",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-3",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-4",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-5",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-6",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-7",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-8",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-9",
    "https://gogoanime.ee/hataraku-maou-sama-2nd-season-episode-10",
  ]

  '''
  eps_list = []
  r = requests.get(anime_category_link)
  anime_id = re.search(r'<input.+?value="(\d+)" id="movie_id"', r.text).group(1)
  res = requests.get("https://ajax.gogo-load.com/ajax/load-list-episode",params={"ep_start": 0, "ep_end": 9999, "id": anime_id},)
  soup = BeautifulSoup(res.content, "html.parser")
  eps_urls = soup.find_all("a")

  for x in eps_urls:
    eps_list.append(f'{baseURL}{(x.get("href")).strip()}')
  eps_list.reverse()

  return eps_list


def GetDownloadURL(anime_episode_link: str) -> dict:
  '''
  Get download link on given anime episode link. Example of anime episode link
  anime_episode_link = https://www1.gogoanime.ee/hataraku-maou-sama-2nd-season-episode-6

  For this function data as :
  1. auth 
  2. token
  are needed. This data are mandatory! Here is the Example:

  token = {
      "auth": (your auth token in string),
      "gogoanime": (your gogoanime token in string),
  }

  Expected output in dictonary (example):
  {
    "640x360": "https://gogodownload.net/download.php?url=aHR0cHM6LyAdeqwrwedffryretgsdFrsftrsvfsfsr9jZG54MDAawehyfcghysfdsDGDYdgdsfsdfwstdgdsgtertQuYW5pY2FjaGUubmV0L3VzZXIxMzQyL2EzNTBiYWJjZWU4OGQ3MTRmYjcxNTEyMGJlNjZmYmI2L0VQLjYudjAuMTY2MDgzNjAxMS4zNjBwLm1wND90b2tlbj1wTndHOXNGWnU1eWZISEFBeEdrM093JmV4cGlyZXM9MTY2MzQxMzU3MyZpZD0xOTA2OTMmdGl0bGU9KDY0MHgzNjAtZ29nb2FuaW1lKWhhdGFyYWt1LW1hb3Utc2FtYS0ybmQtc2Vhc29uLWVwaXNvZGUtNi5tcDQ=",
    "854x480": "https://gogodownload.net/download.php?url=aHR0cHM6LyAawehyfcghysfdsDGDYdgdsfsdfwstdgdsgtert9AdrefsdsdfwerFrefdsfrersfdsrfer36343534jZG54MDQuYW5pY2FjaGUubmV0L3VzZXIxMzQyL2EzNTBiYWJjZWU4OGQ3MTRmYjcxNTEyMGJlNjZmYmI2L0VQLjYudjAuMTY2MDgzNjAxMS40ODBwLm1wND90b2tlbj1sbXhRanFpNUQ1SldWaG5aTmNxYmhnJmV4cGlyZXM9MTY2MzQxMzU3MyZpZD0xOTA2OTMmdGl0bGU9KDg1NHg0ODAtZ29nb2FuaW1lKWhhdGFyYWt1LW1hb3Utc2FtYS0ybmQtc2Vhc29uLWVwaXNvZGUtNi5tcDQ=",
    "1280x720": "https://gogodownload.net/download.php?url=aHR0cHM6LyAdeqwrwedffryretgsdFrsftrsvfsfsr9jZG54MDURASDGHUSRFSJGYfdsffsderFStewthsfSFtrftesdfQuYW5pY2FjaGUubmV0L3VzZXIxMzQyL2EzNTBiYWJjZWU4OGQ3MTRmYjcxNTEyMGJlNjZmYmI2L0VQLjYudjAuMTY2MDgzNjAxMS43MjBwLm1wND90b2tlbj1aczVfYVhkQ0RDRXlqa0VEZnVRaV9BJmV4cGlyZXM9MTY2MzQxMzU3MyZpZD0xOTA2OTMmdGl0bGU9KDEyODB4NzIwLWdvZ29hbmltZSloYXRhcmFrdS1tYW91LXNhbWEtMm5kLXNlYXNvbi1lcGlzb2RlLTYubXA0",
    "1920x1080": "https://gogodownload.net/download.php?url=aHR0cHM6LyAdeqwrwedffryretgsdFrsftrsvfsfsr9jZG54MDAdrefsdsdfwerFrefdsfrersfdsrfer36343534QuYW5pY2FjaGUubmV0L3VzZXIxMzQyL2EzNTBiYWJjZWU4OGQ3MTRmYjcxNTEyMGJlNjZmYmI2L0VQLjYudjAuMTY2MDgzNjAxMS4xMDgwcC5tcDQ/dG9rZW49VjZXdG1MR29lSzhZTS1iSU9fV3VqdyZleHBpcmVzPTE2NjM0MTM1NzMmaWQ9MTkwNjkzJnRpdGxlPSgxOTIweDEwODAtZ29nb2FuaW1lKWhhdGFyYWt1LW1hb3Utc2FtYS0ybmQtc2Vhc29uLWVwaXNvZGUtNi5tcDQ=",
  }

  '''

  download_links = dict()

  # Free Auth Token
  token = {
      "auth":"Tmfe5Hkx6rIDZDsahKL3zaBF%2BoPUl1s561%2F9P%2FzIKGkT9WCB%2F4%2FbY56dYyRIb7qfOT0HI4XHT1GxDWwGudoK2Q%3D%3D",
      "gogoanime":"scluq0bchc8ebkph4gep514gd7",
  }

  r = requests.get(anime_episode_link, cookies=token)
  soup = BeautifulSoup(r.content, "lxml")
  download_div = soup.find("div", {'class': 'cf-download'}).findAll('a')

  for data in download_div:
    download_links[re.sub(r"[\n\t\s]*","",data.string)] = data['href']

  return download_links

