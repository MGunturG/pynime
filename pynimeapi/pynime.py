import re
import os
import json
import m3u8
import time
import shutil
import requests

import threading
import concurrent.futures

from bs4 import BeautifulSoup

from pynimeapi.classes.datatype import *
from pynimeapi.schedule import GetSchedule
from pynimeapi.streaming.url_handler import streamUrl
from pynimeapi.streaming.playlist_parser import PlaylistParser
from pynimeapi.downloader.http_downloader import HTTPDownloader


class PyNime:
    def __init__(self, base_url: str = "https://gogoanime.ar"):
        self.baseURL = base_url  # domain of GoGoAnime. please update regularly

    # TODO: Hello Yoshi, you can use https://ajax.gogo-load.com/site/loadAjaxSearch?keyword={query} to search anime
    def search_anime(self, anime_title: str) -> SearchResultObj:
        ''' Search anime on given title.
            It will return a list of animes and their url in object.
        '''
        try:
            anime_result = []
            anime_title = anime_title.replace(" ", "%20")
            search_page_link = f'{self.baseURL}/search.html?keyword={anime_title}'
            search_page = requests.get(search_page_link)
            search_page = search_page.content
            soup = BeautifulSoup(search_page, "html.parser")
            result = soup.find_all("div", {"class": "img"})

            for idx, i in enumerate(result):
                anime_result.append(
                    SearchResultObj(title=f'{i.contents[1].get("title")}',
                                    category_url=f'{self.baseURL}{i.contents[1].get("href")}'))

            if not anime_result:
                print(f"[!] Anime not found!")
                return None
            else:
                return anime_result

        except Exception as e:
            print(e)

    def get_anime_details(self, anime_category_url: str):
        ''' Get basic anime info/details.
            It will return an object:
                .season        : season of anime aired
                .synopsis      : plot of anime
                .genres        : genres
                .released      : year of released
                .status        : status, ongoing or finished
                .image_url     : anime cover image
        '''
        try:
            detail_page = requests.get(anime_category_url)
            soup = BeautifulSoup(detail_page.text, "html.parser")
            info_body = soup.find("div", {"class": "anime_info_body_bg"})
            image_url = info_body.find("img")["src"]
            other_info = info_body.find_all("p", {"class": "type"})

            title = info_body.find("h1").text.strip()
            season = other_info[0].text.replace("\n", "").replace("Type: ", "")
            synopsis = other_info[1].text.replace("\n", "")
            genres = [
                x["title"]
                for x in BeautifulSoup(str(other_info[2]), "html.parser").find_all("a")
            ]
            released = other_info[3].text.replace("Released: ", "")
            status = other_info[4].text.replace("\n", "").replace("Status: ", "")
            image_url = image_url

            anime_info = AnimeDetailsObj(
                title=title,
                season=season,
                synopsis=synopsis,
                genres=genres,
                released=released,
                status=status,
                image_url=image_url
            )

            return anime_info

        except Exception as e:
            print(e)

    def get_episode_urls(self, anime_category_url: str) -> list:
        ''' Get total of anime episode available and urls per episode.
            It will return a list of urls to anime episode page.
        '''
        try:
            eps_list = list()  # an empty list for storing links

            r = requests.get(anime_category_url)
            anime_id = re.search(r'<input.+?value="(\d+)" id="movie_id"', r.text).group(1)

            res = requests.get("https://ajax.gogo-load.com/ajax/load-list-episode",
                               params={"ep_start": 0, "ep_end": 9999, "id": anime_id}, )

            soup = BeautifulSoup(res.content, "html.parser")
            eps_urls = soup.find_all("a")

            # Append found links to list
            for x in eps_urls:
                eps_list.append(f'{self.baseURL}{(x.get("href")).strip()}')
            eps_list.reverse()

            return eps_list

        except Exception as e:
            print(e)

    def get_stream_urls(self, anime_episode_url: str):
        ''' Get streaming url on given anime episode page.
            It will return urls and their video resolution in JSON format.
        '''
        playlist = PlaylistParser()
        urlhandle = streamUrl(anime_episode_url)
        stream_urls = urlhandle.stream_url()

        result = playlist.parser(stream_urls)

        return result

    def grab_stream(self, anime_title: str, episode: int, resolution=1080):
        ''' It just a shortcut for retrieve the streaming url.
            As default, it will get the best resolution whics is 1080p.
        '''
        resolution = str(resolution)
        playlist = PlaylistParser()

        search_anime = self.search_anime(anime_title)

        if search_anime:
            eps = self.get_episode_urls(search_anime[0].category_url)

            # error handling if selected episode not available
            if (episode > len(eps) or episode == 0):
                print(f"[!] Unfortunately episode {episode} not released yet.")
                print(f"[!] Latest episode is episode {len(eps)}.")
                return None

        else:
            return None

        urlhandle = streamUrl(eps[episode - 1])
        stream_urls = urlhandle.stream_url()

        result = playlist.parser(stream_urls)

        if resolution in result:
            return result[resolution]
        else:
            print(f"[!] Available resolution are {list(result.keys())}. {resolution} not available.")
            return None

    def download_video(self, stream_url: str, filename: str):
        ''' This download function is using internal download function I made.
            Does not have good performance, but it's works.

            It will download ts file, please use converter to convert-
            -downloaded ts file to any video format you want.

            *all video player support playing ts file.
        '''

        segment_validator = PlaylistParser()
        downloader = HTTPDownloader()
        playlist = m3u8.load(stream_url)

        # create list to store video urls
        playlist_segments = list()
        for url in playlist.segments:
            playlist_segments.append(url.uri)

        filename = f"{filename}.ts"  # file will be saved as ts file

        # check if file and temp folder exists
        # if they exists, delete them
        if os.path.exists(filename):
            os.remove(filename)

        if os.path.exists("temp"):
            shutil.rmtree("temp")

        # if they don't exists, create new temp folder
        # for new downloading session
        os.mkdir("temp")

        # download ts files, save it to temp folder
        # folder "temp" automaticly created by "http_downloader.py" as default.
        #
        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread_complete = 0
            total_downloaded_bytes = 0
            files = list()

            for thread_result in executor.map(downloader.download, playlist_segments):
                downloaded_filename, current_downloaded_byte = thread_result

                total_downloaded_bytes += current_downloaded_byte
                thread_complete += 1
                files.append(downloaded_filename)

                downloader.progress_bar(
                    iteration=thread_complete,
                    total=int(len(playlist_segments)),
                    prefix='Downloading',
                    suffix=f'Complete - Downloaded bytes : {total_downloaded_bytes // 10 ** 6} MB.',
                    length=30,
                )

        sorted(files)  # just to ensure file order is appropriate

        # merging downloaded ts files into single ts file
        with open(filename, 'wb') as merged_ts:
            for i, ts_file in enumerate(files):
                if os.path.exists(ts_file):  # check if all files are downloaded
                    with open(ts_file, 'rb') as ts_file_to_merge:
                        shutil.copyfileobj(ts_file_to_merge, merged_ts)
                        ts_file_to_merge.close()
                else:
                    print("[!] Some file missing, aborting.")
                    break

            shutil.rmtree("temp")  # delete folder and files inside them after finished

    def get_schedule(self, unix_time: int):
        schedule.print_schedule(unix_time)
