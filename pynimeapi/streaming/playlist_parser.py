import re
import os
import m3u8

from urllib.parse import urlparse

class PlaylistParser():
	def __init__(self):
		self.regex_pattern = r"x[0-9]+"

	def parser(self, playlist_url: str):
		playlist = m3u8.load(playlist_url)
		playlist_string = playlist.dumps()

		if playlist.is_variant:
			# find available resolution
			find_resolution = re.findall(self.regex_pattern, playlist_string)
			find_resolution = [i.replace("x","") for i in find_resolution]

			# get uri base
			url_parse = urlparse(playlist_url)
			uri_base = os.path.dirname(
				f"{url_parse.scheme}://{url_parse.netloc}{url_parse.path}"
			)

			stream = {}
			for index, resolution in enumerate(find_resolution):
				stream[resolution] = f"{uri_base}/{playlist.playlists[index].uri}"

			return stream

		else:
			return playlist_url

