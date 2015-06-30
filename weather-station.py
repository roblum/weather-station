from camera import Camera
from weather import Weather
from settings import MOTION_DETECTED


class WeatherStation():

	def __init__(self):
		self.camera = Camera()

	def get_hourly_weather(self):
		report = self.camera.detect_motion(
			motion_detected=True,
			display_video_feed=True
		)

		if report is MOTION_DETECTED:
			weather = Weather()
			response = weather.format_hourly()
			print '### WEATHER HOURLY'
			print response

	def get_weather_conditions(self):
		report = self.camera.detect_motion(
			motion_detected=True,
			display_video_feed=True
		)
		
		if report is MOTION_DETECTED:
			weather = Weather()
			response = weather.format_conditions()
			print '### WEATHER CONDITIONS'
			print response


if __name__ == "__main__":
	weather_station = WeatherStation()
	# weather_station.get_hourly_weather()
	weather_station.get_weather_conditions()
