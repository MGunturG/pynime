import os
import json
import base64
import requests
import functools

from pathlib import Path
from urllib.parse import urlparse, parse_qsl, urlencode, urljoin
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

from Crypto.Cipher import AES

class streamUrl:
	'''
	Class for getting embed and streamable url
	it will return link to m3u8 playlist.
	''' 

	def __init__(self, anime_episode_link, video_quality):
		self.qual = video_quality # "best" or "worst"
		self.episode_link = anime_episode_link
		self.session = requests.Session()
		retry = Retry(connect = 3, backoff_factor = 0.5)
		adapter = HTTPAdapter(max_retries = retry)
		self.session.mount("http://", adapter)
		self.session.mount("https://", adapter)
		self.ajax_url = "/encrypt-ajax.php?"
		self.enc_key_api = "https://raw.githubusercontent.com/justfoolingaround/animdl-provider-benchmarks/master/api/gogoanime.json"
		self.mode = AES.MODE_CBC
		self.size = AES.block_size
		self.padder = "\x08\x0e\x03\x08\t\x03\x04\t"
		self.pad = lambda s: s + chr(len(s) % 16) * (16 - len(s) % 16)
		keys = self.get_encryption_keys()
		self.iv = keys["iv"]
		self.key = keys["key"]
		self.second_key = keys["second_key"]

	def embed_url(self):
		r = self.session.get(self.episode_link)
		soup = BeautifulSoup(r.content, "html.parser")
		link = soup.find("a", {"class": "active", "rel": "1"})
		embed_url = f'https:{link["data-video"]}'
		return embed_url

	@functools.lru_cache()
	def get_encryption_keys(self):
		return {
			_: __.encode()
			for _, __ in self.session.get(self.enc_key_api).json().items()
		}

	def aes_encrypt(self, data, key):
		return base64.b64encode(AES.new(key, self.mode, iv=self.iv).encrypt(self.pad(data).encode()))

	def aes_decrypt(self, data, key):
		return (AES.new(key, self.mode, iv = self.iv).decrypt(base64.b64decode(data)).strip(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10"))

	def get_data(self, embed_url):
		r = self.session.get(embed_url)
		soup = BeautifulSoup(r.content, "html.parser")
		crypto = soup.find("script", {"data-name": "episode"})
		return crypto["data-value"]

	def stream_url(self, embed_url):
		parsed = urlparse(embed_url)
		self.ajax_url = parsed.scheme + "://" + parsed.netloc + self.ajax_url

		data = self.aes_decrypt(self.get_data(embed_url), self.key).decode()
		data = dict(parse_qsl(data))

		id = urlparse(embed_url).query
		id = dict(parse_qsl(id))["id"]
		enc_id = self.aes_encrypt(id, self.key).decode()
		data.update(id = enc_id)

		headers = {
			"x-requested-with": "XMLHttpRequest",
			"referer": embed_url,
		}

		r = self.session.post(self.ajax_url + urlencode(data) + f"&alias={id}", headers = headers)

		json_resp = json.loads(self.aes_decrypt(r.json().get("data"), self.second_key))

		source_data = [x for x in json_resp["source"]]

		streams = []
		for i in source_data:
			if "m3u8" in i["file"] or i["type"] == "hls":
				type = "hls"
			else:
				type = "mp4"
		quality = i["label"].replace(" P", "").lower()
		streams.append({"file": i["file"], "type": type, "quality": quality})

		filtered_q_user = list(filter(lambda x: x["quality"] == self.qual, streams))

		if filtered_q_user:
			stream = list(filtered_q_user)[0]
		elif self.qual == "best" or self.qual == None:
			stream = streams[-1]
		elif self.qual == "worst":
			stream = streams[0]
		else:
			print("quality not avalible, using default")
			stream = streams[-1]

		return stream['file']