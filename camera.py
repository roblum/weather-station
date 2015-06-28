import cv2
import datetime


class Camera():

	def __init__(self):
		self.camera = cv2.VideoCapture(0)
		self.first_frame = None
		self.video_active = True

		self.video_feed()

	def video_feed(self):
		while self.video_active:
			(self.grabbed, self.frame) = self.camera.read()
			self.text = "No Motion Detected"

			gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
			gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

			if self.first_frame is None:
				self.set_first_frame(gray_frame)				

			self.on_video_capture_error()
			self.display_video_feed()
			self.exit_trigger()

		self.camera.release()
		cv2.destroyAllWindows()

	def set_first_frame(self, gray_frame):
		self.first_frame = gray_frame

	def on_video_capture_error(self):
		if not self.grabbed:
			self.video_active = False

	def reset_first_frame(self, gray_frame):
		self.set_first_frame(gray_frame)

	def display_video_feed(self):
		cv2.imshow("Video Feed", self.frame)		

	def exit_trigger(self):
		if cv2.waitKey(1) & 0xFF == ord("q"):
			self.video_active = False

if __name__ == "__main__":
	motion_detection = Camera()