import re
import os
import m3u8

from urllib.parse import urlparse


class PlaylistParser():
    def __init__(self):
        self.regex_pattern = r"x[0-9]+"  # regex for searching video resolution

    def parser(self, playlist_url: str):
        try:
            playlist = m3u8.load(playlist_url)
            playlist_string = playlist.dumps()

            if playlist.is_variant:
                # find available resolution
                find_resolution = re.findall(self.regex_pattern, playlist_string)
                find_resolution = [i.replace("x", "") for i in find_resolution]

                # get url base
                url_parse = urlparse(playlist_url)
                url_base = os.path.dirname(
                    f"{url_parse.scheme}://{url_parse.netloc}{url_parse.path}"
                )

                stream = {}
                for index, resolution in enumerate(find_resolution):
                    stream[resolution] = f"{url_base}/{playlist.playlists[index].uri}"

                return stream

            else:
                return playlist_url
        except Exception as e:
            print(e)

    @staticmethod
    def validate_segment_url(segment_url: str, playlist_url: str):
        try:
            url_parse = urlparse(playlist_url)
            url_base = os.path.dirname(
                f"{url_parse.scheme}://{url_parse.netloc}{url_parse.path}"
            )

            if is_url(segment_url):
                return segment_url
            else:
                return f"{url_base}/{segment_url}"
        except Exception as e:
            print(e)

    @staticmethod
    def is_url(url: str):
        regex = re.compile(r"^(?:http|ftp)s?://"  # http:// or https://
                           r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
                           r"localhost|"  # localhost...
                           r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
                           r"(?::\d+)?"  # optional port
                           r"(?:/?|[/?]\S+)$", re.IGNORECASE, )
        return re.match(regex, url) is not None
