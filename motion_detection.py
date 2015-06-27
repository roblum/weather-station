import cv2


class Camera():

	def __init__(self):
		self.camera = cv2.VideoCapture(0)
		self.first_frame = None
		self.video_active = True

		self.video_feed()

	def video_feed(self):
		while self.video_active:
			(self.grabbed, self.frame) = self.camera.read()

			self.on_video_capture_error()
			self.display_video_feed()
			self.exit_trigger()

		self.camera.release()
		cv2.destroyAllWindows()

	def on_video_capture_error(self):
		if not self.grabbed:
			self.video_active = False

	def display_video_feed(self):
		cv2.imshow("Video Feed", self.frame)		

	def exit_trigger(self):
		if cv2.waitKey(1) & 0xFF == ord("q"):
			self.video_active = False

if __name__ == "__main__":
	motion_detection = Camera()