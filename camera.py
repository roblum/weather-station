import cv2
import datetime


class Camera():

	def __init__(self):
		self.camera = cv2.VideoCapture(0)
		self.base_frame = None

	def video_feed(self, **kwargs):
		self.set_video_state("Video Activated")
		
		while self.video_active:
			(self.grabbed, self.frame) = self.camera.read()
			self.gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
			self.gray_frame = cv2.GaussianBlur(self.gray_frame, (21, 21), 0)

			if self.base_frame is None:
				self.set_base_frame(self.gray_frame)				

			self.display_video_text()

			for feature in kwargs:
				if kwargs[feature] is True:
					getattr(self, feature)()

			self.on_video_capture_error()
			self.exit_trigger(self.gray_frame)

	def detect_motion(self, **kwargs):
		self.video_active = True
		self.video_feed(**kwargs)

		if self.video_state is "Motion Detected":
			return self.video_state

	def motion_detected(self):
		self.set_video_state("No Motion Detected")
		self.frame_delta = cv2.absdiff(self.base_frame, self.gray_frame)
		self.thresh = cv2.threshold(self.frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
		self.thresh = cv2.dilate(self.thresh, None, iterations=2)
		(cnts, _) = cv2.findContours(
			self.thresh.copy(), 
			cv2.RETR_EXTERNAL, 
			cv2.CHAIN_APPROX_SIMPLE
		)

		for c in cnts:
			if cv2.contourArea(c) < 500:
				(x, y, w, h) = cv2.boundingRect(c)
				cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				self.set_video_state("Motion Detected")
				self.video_active = False

	def display_video_text(self):
		cv2.putText(self.frame, 
			self.text, 
			(10, 20), 
			cv2.FONT_HERSHEY_SIMPLEX, 
			0.5, 
			(0, 0, 255), 
			2
		)
		cv2.putText(self.frame, 
			datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), 
			(10, self.frame.shape[0] - 10), 
			cv2.FONT_HERSHEY_SIMPLEX, 
			0.35, 
			(0, 0, 255), 
			1
		)

	def set_video_state(self, text):
		self.video_state = text
		self.text = text

	def set_base_frame(self, gray_frame):
		self.base_frame = gray_frame

	def on_video_capture_error(self):
		if not self.grabbed:
			self.kill_video()

	def display_video_feed(self):
		cv2.imshow("Thresh", self.thresh)
		cv2.imshow("Frame Delta", self.frame_delta)
		cv2.imshow("Video Feed", self.frame) # Last window shows on top	
	
	def kill_video(self):
		self.video_active = False
		self.camera.release()
		cv2.destroyAllWindows()

	def exit_trigger(self, gray_frame):
		if cv2.waitKey(1) & 0xFF == ord("q"):
			# self.kill_video()
			self.set_base_frame(gray_frame)
