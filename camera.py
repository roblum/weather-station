import cv2
import datetime

from settings import VIDEO_ACTIVATED, NO_MOTION_DETECTED, MOTION_DETECTED


class Camera():

	def __init__(self):
		self.camera = cv2.VideoCapture(0)
		# self.base_frame = None

	def video_feed(self, **kwargs):
		(grabbed, frame) = self.camera.read()
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

		self.display_video_text(frame, kwargs.get('video_text'))
		self.on_video_capture_error(grabbed)
		self.display_video_feed(frame)
		self.exit_trigger(gray_frame)

		return frame, gray_frame

	def detect_motion(self):
		self.base_frame = None
		self.is_recording = True
		video_text = NO_MOTION_DETECTED

		while self.is_recording:
			frame, gray_frame = self.video_feed(video_text=video_text) 

			if self.base_frame is None:
				self.base_frame = gray_frame

			if self.motion_detected(frame, gray_frame) is MOTION_DETECTED: 
				# self.set_video_state(MOTION_DETECTED) 
				video_text = MOTION_DETECTED
				self.is_recording = False 
				return MOTION_DETECTED

			# if self.video_state is MOTION_DETECTED:
				# return self.video_state

	def motion_detected(self, frame, gray_frame):
		self.set_video_state(NO_MOTION_DETECTED)
		self.frame_delta = cv2.absdiff(self.base_frame, gray_frame)
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
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				# self.set_video_state(MOTION_DETECTED)
				# self.is_recording = False
				return MOTION_DETECTED

	def display_video_text(self, frame, video_text=VIDEO_ACTIVATED):
		cv2.putText(frame, 
			video_text, 
			(10, 20), 
			cv2.FONT_HERSHEY_SIMPLEX, 
			0.5, 
			(0, 0, 255), 
			2
		)
		cv2.putText(frame, 
			datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), 
			(10, frame.shape[0] - 10), 
			cv2.FONT_HERSHEY_SIMPLEX, 
			0.35, 
			(0, 0, 255), 
			1
		)

	def set_video_state(self, condition):
		self.video_state = condition
		self.video_text = condition

	def set_base_frame(self, gray_frame):
		self.base_frame = gray_frame

	def on_video_capture_error(self, grabbed):
		if not grabbed:
			self.kill_video()

	def display_video_feed(self, frame):
		# cv2.imshow("Thresh", self.thresh) # Only for detect_motion
		# cv2.imshow("Frame Delta", self.frame_delta) # Only for detect_motion
		cv2.imshow("Video Feed", frame) # Last window shows on top	
	
	def kill_video(self):
		self.is_recording = False
		self.camera.release()
		cv2.destroyAllWindows()

	def exit_trigger(self, gray_frame):
		if cv2.waitKey(1) & 0xFF == ord("q"):
			# self.kill_video()
			self.set_base_frame(gray_frame) # reset first frame
