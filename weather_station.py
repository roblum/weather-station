from camera import CameraFeatures
from weather import WeatherApi
from settings import MOTION_DETECTED, HOURLY, CONDITIONS


class WeatherStation():

	def __init__(self):
		self.camera = CameraFeatures()

	def check_camera_motion(self):
		# return self.camera.detect_motion()
		return self.camera.detect_face()

	def get_weather_conditions(self):
		if self.check_camera_motion():
			weather = WeatherApi()
			response = weather.return_formatted_weather(5, HOURLY)

			print response


if __name__ == "__main__":
	weather_station = WeatherStation()
	weather_station.get_weather_conditions()
