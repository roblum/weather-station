from camera import Camera
from weather import Weather

class WeatherStation():

	def __init__(self):
		camera = Camera()
		results = camera.detect_motion(
			motion_detected=True,
			display_video_feed=True
		)

if __name__ == "__main__":
	WeatherStation()
