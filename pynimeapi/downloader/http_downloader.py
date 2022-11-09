import os
import sys
import time
import requests

from pynimeapi.classes.color import bcolors

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
		
		try:
			with requests.get(source, headers = self.headers, stream = True) as r:
				if r.status_code == 200:
					print(f"{bcolors.OKGREEN}[>] Link available.{bcolors.ENDC}")

					if os.path.exists(saved_filename):
						if abs(os.path.getsize(saved_filename) - int(r.headers.get('content-length'))) < 1:
							print(f"{bcolors.WARNING}[!] File already downloaded.{bcolors.ENDC}")
							return True # skipping download
						else:
							print(f"{bcolors.WARNING}[!] Current downloaded file have different size, file maybe corrupted. Redownloading.{bcolors.ENDC}")
							return False # continue to download

				else:
					# Link expired or gone HTTP ERROR 410 (Gone).
					print(f"{bcolors.FAIL}[!] Link not found or expired.{bcolors.ENDC}")
					return True # skipping download

		except Exception as e:
			print(e)


	def download(self, source, save_filename):
		'''
		To be clear, using internal downloader (this function) might be have slow download speed.
		I recommend user to copy link download and download the file using external downloader such Internet Download Manager (IDM).
		'''
		
		download_filename = f'{save_filename}.mp4' # all videos uploaded on gogoanime is mp4 format
		
		''' To calculate download speed, we need to know how much
		time passed (elapsed time).
		
		Download speed = downloaded bytes / elapsed time
		and elapsed time is (start_time - current time)

		'''
		start_time = time.time()

		try:
			with requests.get(source, headers = self.headers, stream = True) as r:
				r.raise_for_status()
				file_size = r.headers.get('content-length')

				with open(download_filename, 'wb') as f:
					print(f"{bcolors.OKBLUE}[*]{bcolors.ENDC} Downloading {download_filename}")
					downloaded_byte = 0 # Initial downloaded bytes is always zero byte.
					file_size = int(file_size)
					print(f'{bcolors.OKBLUE}[*]{bcolors.ENDC} File size: {file_size//10**6} MB.') # convert bytes (B) to megabytes (MB), bytes that are divided by 10^6

					for chunk in r.iter_content(chunk_size = self.chunksize):
						downloaded_byte += len(chunk)
						f.write(chunk) # write file to disk.

						done = int(50 * downloaded_byte / file_size)
						download_speed = downloaded_byte / (time.time() - start_time) / 10**6
						sys.stdout.write("\r[*][%s%s] Status: %d%% | Speed: %.2f MB/s" % ('=' * done, ' ' * (50 - done), int(downloaded_byte/file_size * 100), download_speed))
						sys.stdout.flush()

			return download_filename
		except Exception as e:
			print(e)
		finally:
			print("\n[!] Download finished.")
