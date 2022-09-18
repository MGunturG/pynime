class SearchResultObj:
	def __init__(self, title: str, url: str):
		self.title = title
		self.url = url

class AnimeDetailsObj:
	def __init__(
		self, 
		season: str, 
		synopsis: str, 
		genres: list, 
		released: int, 
		status: str, 
		total_episode: int,
		image_url: str):
		self.season = season
		self.synopsis = synopsis
		self.genres = genres
		self.released = released
		self.status = status
		self.total_episode = total_episode
		self.image_url = image_url
