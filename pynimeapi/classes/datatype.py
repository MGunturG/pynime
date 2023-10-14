class SearchResultObj:
	def __init__(self, title: str, category_url: str, picture_url: str):
		self.title = title
		self.category_url = category_url
		self.picture_url = picture_url

	def __str__(self):
		return f"title: {self.title} | category_url: {self.category_url}"

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

class RecentAnimeObj:
	def __init__(self, title, latest_episode, latest_episode_url, picture_url):
		self.title = title
		self.latest_episode = latest_episode
		self.latest_episode_url = latest_episode_url
		self.picture_url = picture_url
