import requests
from keys import API_KEY #temp
from settings import HOURLY, CONDITIONS

BASE_URL = "http://api.wunderground.com/api/{0}/{1}/q/{2}/{3}.json"
STATE = "NY"
LOCATION = "New_York"


class Weather():

	def make_request(self, **kwargs):
		response = requests.get(BASE_URL.format(
			API_KEY, 
			kwargs.get('condition', CONDITIONS), 
			STATE, 
			LOCATION
		))
		return response._content

	def format_hourly(self):
		response = self.make_request(condition=HOURLY)

		return response

	def format_conditions(self):
		response = self.make_request(condition=CONDITIONS)

		return response

