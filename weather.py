import requests
from keys import API_KEY #temp

BASE_URL = "http://api.wunderground.com/api/{0}/conditions/q/{1}/{2}.json"
STATE = "NY"
LOCATION = "New_York"

class Weather():

	def __init__(self):
		self.make_request()

	def make_request(self):
		response = requests.get(BASE_URL.format(API_KEY, STATE, LOCATION))
		print response._content
		# return response._content

	def format_hourly(self):
		pass
