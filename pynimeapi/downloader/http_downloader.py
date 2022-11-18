import os
import re
import sys
import time
import requests

class HTTPDownloader:
	def __init__(self):
		self.chunksize = 16384
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
		}

	def remove_forbiden_string(self, input_string):
	    ''' Remove char that forbiden while creating a file such as ? * | etc
	    '''
	    new_string = re.sub('[:><?/|* ]+', '', input_string)
	    return new_string

	def progress_bar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', print_end = '\r'):
		''' Make CLI progressbar.
			source = https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters

			@params:
				iteration   - Required  : current iteration (Int)
				total       - Required  : total iterations (Int)
				prefix      - Optional  : prefix string (Str)
				suffix      - Optional  : suffix string (Str)
				decimals    - Optional  : positive number of decimals in percent complete (Int)
				length      - Optional  : character length of bar (Int)
				fill        - Optional  : bar fill character (Str)
				print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
		'''
		percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
		filled_length = int(length * iteration // total)
		bar = fill * filled_length + '-' * (length - filled_length)
		print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = print_end)
		if iteration == total:
			print()

	def download(self, url, download_folder_path = 'temp'):
		''' To be clear, using internal downloader (this function) might be have slow download speed.
			I recommend user to copy link download and download the file using external downloader such Internet Download Manager (IDM).

			But I recommend XTREME DOWNLOAD MANAGER (XDM).
			Github : https://github.com/subhra74/xdm
		'''
		retries = 0
		max_retry = 3

		save_filename = f"{download_folder_path}/{self.remove_forbiden_string(os.path.basename(url))}"

		while retries < max_retry:
			try:
				with requests.get(url, headers = self.headers, stream = True) as req:
					req.raise_for_status() # check connection status, if return code 200 (which means OK) then continue
					file_size = req.headers.get('content-length') # get file size (bytes)

					with open(save_filename, 'wb') as downloaded_file:
						downloaded_byte = 0 # Initial downloaded bytes is always zero byte.
						file_size = int(file_size)

						for chunk in req.iter_content(chunk_size = self.chunksize):
							downloaded_byte += len(chunk)
							downloaded_file.write(chunk) # write file to disk.

						downloaded_file.close()

				return save_filename, downloaded_byte
				break # break from while loop
			except Exception as e:
				# retries handling. If connection fail, retries until reach max_retry
				retries += 1
				if retries == max_retry:
					raise e

				# error log
				print(e)
				print("[!] Retrying...")
