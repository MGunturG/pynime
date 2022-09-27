import os
import sys
import time
import requests

class HTTPDownloader:
	def __init__(self):
		self.chunksize = 16384
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
		}

	def check_if_exists(self, source, saved_filename):
		'''
		This function will check if file already downloaded or not.

		'''
		saved_filename = f'{saved_filename}.mp4' # all videos uploaded on gogoanime is mp4 format
		with requests.get(source, headers=self.headers, stream=True) as r:
			if r.status_code == 200:
				print("Link available.")

				if os.path.exists(saved_filename):
					if abs(os.path.getsize(saved_filename) - int(r.headers.get('content-length'))) < 1:
						print("File already downloaded.")
						return True # skipping download
					else:
						print("Downloaded file have different size, file maybe corrupted.")
						return False # continue to download
			else:
				# Link expired
				print("Link not found or expired.")
				return True # skipping download


	def download(self, source, save_filename):
		'''
		To be clear, using internal downloader (this function) might be slow.
		I recommend user to copy link download and download the file using-
		-external downloader such Internet Download Manager (IDM).
		'''
		download_filename = f'{save_filename}.mp4' # all videos uploaded on gogoanime is mp4 format
		with requests.get(source, headers=self.headers, stream=True) as r:
			r.raise_for_status()
			file_size = r.headers.get('content-length')
			with open(download_filename, 'wb') as f:
				print(f"Downloading {save_filename}...")
				downloaded_byte = 0
				file_size = int(file_size)
				for chunk in r.iter_content(chunk_size = self.chunksize):
					downloaded_byte += len(chunk)
					f.write(chunk)

					done = int(50 * downloaded_byte / file_size)
					sys.stdout.write("\r[%s%s] %d%%" % ('=' * done, ' ' * (50 - done), int(downloaded_byte/file_size * 100)))
					sys.stdout.flush()

		return download_filename