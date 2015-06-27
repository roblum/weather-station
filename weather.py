import requests
from keys import API_KEY #temp

BASE_URL = "http://api.wunderground.com/api/{0}/conditions/q/{1}/{2}.json"
STATE = "NY"
LOCATION = "New_York"

def make_request():
	response = requests.get(BASE_URL.format(API_KEY, STATE, LOCATION))
	print response._content

if __name__ == "__main__":
	make_request()