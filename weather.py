import requests
import json

from keys import API_KEY #temp
from settings import HOURLY, CONDITIONS

BASE_URL = "http://api.wunderground.com/api/{0}/{1}/q/{2}/{3}.json"
STATE = "NY"
LOCATION = "New_York"


class WeatherApi():

	def make_request(self, **kwargs):
		response = requests.get(BASE_URL.format(
			API_KEY, 
			kwargs.get('condition', CONDITIONS), 
			STATE, 
			LOCATION
		))

		return response._content

	def return_formatted_weather(self, amt_of_hours, type_of_forecast):
		response = json.loads(self.make_request(condition=type_of_forecast))

		next_hours = []
		for hour in xrange(amt_of_hours):
			if response['hourly_forecast'][hour]:
				next_hours.append(self.weather_factory(
					response['hourly_forecast'][hour],
					type_of_forecast
				))
		
		return next_hours

	def weather_factory(self, forecast, type_of_forecast):
		if type_of_forecast is HOURLY:
			return self.hour_format(forecast)
		# elif type_of_forecast is CONDITIONS:
		# 	return self.conditions_format(forecast)

	def hour_format(self, forecast):
		military_hour = int(forecast['FCTTIME']['hour']) #['hour']

		if military_hour > 12:
			military_hour = 12 - military_hour

		conditions = {
			'hour': military_hour,
			'temperature': forecast['temp']['english'],
			'precipitation': forecast['pop'],
			'icon': forecast['icon'],
			'icon_url': forecast['icon_url'],
		}

		return conditions
