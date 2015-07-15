from camera import CameraFeatures
from weather import Weather
from settings import MOTION_DETECTED, HOURLY, CONDITIONS


class WeatherStation():

	def __init__(self):
		self.camera = CameraFeatures()

	def check_camera_motion(self):
		report = self.camera.detect_motion()

		if report is MOTION_DETECTED:
			return True

	def get_weather_conditions(self):
		if self.check_camera_motion():
			weather = Weather()
			response = weather.return_formatted_weather(5, HOURLY)

			print response


if __name__ == "__main__":
	weather_station = WeatherStation()
	weather_station.get_weather_conditions()
