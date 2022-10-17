import re
import json
import requests
from bs4 import BeautifulSoup

from pynimeapi.classes.datatype import *
from pynimeapi.classes.color import bcolors

from pynimeapi.downloader.http_downloader import HTTPDownloader
downloader = HTTPDownloader()

from pynimeapi.schedule import GetSchedule
schedule = GetSchedule()


class PyNime:
  def __init__(self, auth: str, gogoanime: str, base_url: str = "https://gogoanime.dk"):
    self.auth_token = auth
    self.gogoanime_token = gogoanime
    self.baseURL = base_url


  def search_anime(self, anime_title: str) -> SearchResultObj:
    '''
    Search anime on given title.
    It will return a list of animes and their url in object.

    '''
    try:
      anime_result = []
      anime_title = anime_title.replace(" ", "%20")
      search_page_link = f'{self.baseURL}/search.html?keyword={anime_title}'
      search_page = requests.get(search_page_link)
      search_page = search_page.content
      soup = BeautifulSoup(search_page, "html.parser")
      result = soup.find_all("div", {"class":"img"})

      for idx, i in enumerate(result):
        anime_result.append(
          SearchResultObj(title=f'{i.contents[1].get("title")}', 
          url=f'{self.baseURL}{i.contents[1].get("href")}'))

      if not anime_result:
        print(f"{bcolors.WARNING}[!] Anime not found!{bcolors.ENDC}")
        return None
      else:
        return anime_result

    except requests.exceptions.ConnectionError:
      print("Network Error.")


  def get_details(self, anime_category_link: str):
    '''
    Get basic anime info/details.
    It will return an object.
    .season        : season of anime aired
    .synopsis      : plot of anime
    .genres        : genres
    .released      : year of released
    .status        : status, ongoing or finished
    .image_url     : anime cover image

    '''
    try:
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
      image_url = image_url

      anime_info_object = AnimeDetailsObj(
        season = season,
        synopsis = synopsis,
        genres= genres,
        released= released,
        status= status,
        image_url = image_url
      )

      return anime_info_object

    except AttributeError:
      print("Invalid argument given!")
    except requests.exceptions.ConnectionError:
      print("Network Error.")


  def get_eps_links(self, anime_category_link: str) -> list:
    '''
    Get total of anime episode available and links per episode.
    It will return a list of links to anime episode page.
    '''
    try:
      eps_list = [] # an empty list for storing links

      r = requests.get(anime_category_link)
      anime_id = re.search(r'<input.+?value="(\d+)" id="movie_id"', r.text).group(1)

      res = requests.get("https://ajax.gogo-load.com/ajax/load-list-episode",
        params = {"ep_start": 0, "ep_end": 9999, "id": anime_id},)

      soup = BeautifulSoup(res.content, "html.parser")
      eps_urls = soup.find_all("a")

      # Append found links to list
      for x in eps_urls:
        eps_list.append(f'{self.baseURL}{(x.get("href")).strip()}')
      eps_list.reverse()

      return eps_list

    except AttributeError:
      print("Invalid argument given!")
    except requests.exceptions.ConnectionError:
      print("Network Error.")


  def get_download_link(self, anime_episode_link: str) -> DownloadLinkObj:
    '''
    Get download link on given anime episode link. Example of anime episode link
    anime_episode_link = 'https://www1.gogoanime.ee/hataraku-maou-sama-2nd-season-episode-6'
    (It's link for anime Hataraku Maou Sama 2nd Season Episode 6)

    To get the download link of the desired resolution, use:
    .link_360 to get 360p download link
    .link_480 to get 480p download link
    and so on... maximum resolution availabe are 1080p.

    '''
    try:
      download_links = DownloadLinkObj()
      token = {
          "auth": self.auth_token,
          "gogoanime": self.gogoanime_token
      }

      r = requests.get(anime_episode_link, cookies = token)
      soup = BeautifulSoup(r.content, "lxml")
      download_div = soup.find("div", {'class': 'cf-download'}).findAll('a')

      for data in download_div:
        video_resulotion = re.search("x([0-9]+)", re.sub(r"[\n\t\s]*","",data.string)).group(1)

        if video_resulotion == "360":
          download_links.link_360 = f'{data["href"]}'

        elif video_resulotion == "480":
          download_links.link_480 = f'{data["href"]}'

        elif video_resulotion == "720":
          download_links.link_720 = f'{data["href"]}'

        elif video_resulotion == "1080":
          download_links.link_1080 = f'{data["href"]}'

      return download_links
    except AttributeError:
      print("Invalid argument given!")
    except requests.exceptions.ConnectionError:
      print("Network Error.")


  def fast_query(self, title: str, episode: int, resolution: int):
    '''
    Fast query to get anime download link.
    It will return download/streamable link.
    '''
    search_anime = self.search_anime(title)

    if search_anime:
      print(f"{bcolors.OKGREEN}[?] Default selection result are 1.{bcolors.ENDC}")
      print(f"{bcolors.OKGREEN}[>] 1 Selected. OK!{bcolors.ENDC}")
      print()

      # detail_anime = self.get_details(search_anime[0].url)
      eps = self.get_eps_links(search_anime[0].url)

      if (episode > len(eps) or episode == 0):
        print(f"{bcolors.WARNING}[!] Unfortunately episode {episode} not released yet.{bcolors.ENDC}")
        print(f"{bcolors.WARNING}[!] Latest episode is episode {len(eps)}.{bcolors.ENDC}")
        return

    else:
      # If search query found nothing, return nothing.
      # function search_anime will print message if nothing found.
      return None

    vid = self.get_download_link(eps[episode - 1])

    if resolution == 360:
      if vid.link_360 == None:
        print(f"{bcolors.WARNING}[!] Link to selected resolution not available.{bcolors.ENDC}")
        return vid.link_360
      else:
        print(f'{bcolors.OKGREEN}[>] Link for {resolution}p{bcolors.ENDC} : {vid.link_360}')
        return vid.link_360

    if resolution == 480:
      if vid.link_480 == None:
        print(f"{bcolors.WARNING}[!] Link to selected resolution not available.{bcolors.ENDC}")
        return vid.link_480
      else:
        print(f'{bcolors.OKGREEN}[>] Link for {resolution}p{bcolors.ENDC} : {vid.link_480}')
        return vid.link_480

    if resolution == 720:
      if vid.link_720 == None:
        print(f"{bcolors.WARNING}[!] Link to selected resolution not available.{bcolors.ENDC}")
        return vid.link_720
      else:
        print(f'{bcolors.OKGREEN}[>] Link for {resolution}p{bcolors.ENDC} : {vid.link_720}')
        return vid.link_720

    if resolution == 1080:
      if vid.link_1080 == None:
        print(f"{bcolors.WARNING}[!] Link to selected resolution not available.{bcolors.ENDC}")
        return vid.link_1080
      else:
        print(f'{bcolors.OKGREEN}[>] Link for {resolution}p{bcolors.ENDC} : {vid.link_1080}')
        return vid.link_1080

    # If resolution is not 360, 480, 720, or 1080 it will return None
    return None


  def get_video(self, video_link: str, file_name: str):
    ''' Remember, all video uploaded on GoGoAnime is mp4 '''

    # Check if file exists
    if downloader.check_if_exists(video_link, file_name):
      # File exists, skip download
      return
    else:
      # Continue download the file
      downloader.download(video_link, file_name)


  def get_schedule(self, unix_time: int):
    schedule.print_schedule(unix_time)
