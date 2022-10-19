import m3u8
import requests

class playlist:
	'''
	This class is for handling m3u8 playlist. Extract the 
	playlist to able stream from mpv or other player.
	'''
	def __init__(self, playlist_url):
		self.playlist_url = playlist_url

	def extract_m3u8(self):
		return None

