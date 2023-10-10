import re
import json
import yarl
import base64
import certifi
import requests
import lxml.html as htmlparser

from Crypto.Cipher import AES

KEYS_REGEX = re.compile(rb"(?:container|videocontent)-(\d+)")
ENCRYPTED_DATA_REGEX = re.compile(rb'data-value="(.+?)"')

class streamExtractor:
	'''
	Class for getting embed and streamable url
	it will return link to m3u8 playlist.
	'''

	def get_embed_url(self, episode_url):
		content_parsed = htmlparser.fromstring(requests.get(episode_url, verify=certifi.where()).text)
		return f"{content_parsed.cssselect('iframe')[0].get('src')}"


	def get_quality(self, embed_url):
		match = re.search(r"(\d+) P", embed_url)

		if not match:
			return None

		return int(match.group(1))


	def pad(self, data):
		return data + chr(len(data) % 16) * (16 - len(data) % 16)


	def aes_encrypt(self, data: str, *, key, iv):
		return base64.b64encode(
			AES.new(key, AES.MODE_CBC, iv=iv).encrypt(self.pad(data).encode())
		)


	def aes_decrypt(self, data: str, *, key, iv):
		return (
			AES.new(key, AES.MODE_CBC, iv=iv)
			.decrypt(base64.b64decode(data))
			.strip(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10")
		)


	def extract(self, url):
		url = self.get_embed_url(url)
		parsed_url = yarl.URL(url)
		content_id = parsed_url.query['id']
		next_host = f"https://{parsed_url.host}/"

		if url[:2]=="//":
			url = "https:" + url
			streaming_page = requests.get(url).content
		else:
			streaming_page = requests.get(url).content

		encryption_key, iv, decryption_key = (
			_.group(1) for _ in KEYS_REGEX.finditer(streaming_page)
		)

		component = self.aes_decrypt(
			ENCRYPTED_DATA_REGEX.search(streaming_page).group(1),
			key=encryption_key,
			iv=iv,
		).decode() + "&id={}&alias={}".format(
			self.aes_encrypt(content_id, key=encryption_key, iv=iv).decode(), content_id
		)

		_, component = component.split("&", 1)

		ajax_response = requests.get(
			next_host + "encrypt-ajax.php?" + component,
			headers={"x-requested-with": "XMLHttpRequest"},
		)
		content = json.loads(
			self.aes_decrypt(ajax_response.json().get('data'), key=decryption_key, iv=iv)
		)

		def yielder():
			for origin in content.get("source"):
				yield {
					"stream_url": origin.get('file'),
					"quality": self.get_quality(origin.get('label', '')),
				}

			for backups in content.get("source_bk"):
				yield {
					"stream_url": backups.get('file'),
					"quality": self.get_quality(backups.get('label', '')),
				}
		result = list(yielder())
		return result[0]['stream_url']