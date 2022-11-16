class SearchResultObj:
	def __init__(self, title: str, category_url: str):
		self.title = title
		self.category_url = category_url

class AnimeDetailsObj:
	def __init__(
		self, season: str, title: str,
		synopsis: str, genres: list, 
		released: int, status: str, 
		image_url: str):
		self.title = title
		self.season = season
		self.synopsis = synopsis
		self.genres = genres
		self.released = released
		self.status = status
		self.image_url = image_url