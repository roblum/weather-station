import cv2
import datetime

from settings import CAMERA_ACTIVATED, NO_MOTION_DETECTED, MOTION_DETECTED


class Camera():

	def __init__(self):
		self.camera = cv2.VideoCapture(0)
		self.video_text = CAMERA_ACTIVATED

	def capture_frame(self):
		(self.curr_grabbed, self.curr_frame) = self.camera.read()
		self.curr_gray_frame = cv2.cvtColor(self.curr_frame, cv2.COLOR_BGR2GRAY)
		self.curr_gray_frame = cv2.GaussianBlur(self.curr_gray_frame, (21, 21), 0)

	def display_text_on_frame(self):
		cv2.putText(self.curr_frame, # Show Feed State as video_text
			self.video_text,
			(10, 20),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.5,
			(0, 0, 255),
			2
		)
		cv2.putText(self.curr_frame, # Show Timestamp
			datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
			(10, self.curr_frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.35,
			(0, 0, 255),
			1
		)

	def display_frame_feed(self):
		# cv2.imshow("Thresh", self.thresh) # Only for detect_motion
		# cv2.imshow("Frame Delta", self.frame_delta) # Only for detect_motion
		cv2.imshow("Video Feed", self.curr_frame) # Last window shows on top

	def on_frame_capture_error(self):
		if not self.curr_grabbed:
			self.kill_camera()

	def exit_trigger(self):
		if cv2.waitKey(1) & 0xFF == ord("q"):
			self.kill_camera() # kill switch

	def kill_camera(self):
		self.is_recording = False
		self.camera.release()
		cv2.destroyAllWindows()


class CameraFeatures(Camera):

	def detect_motion(self):
		self.is_recording = True
		self.set_base_frame(None)

		while self.is_recording:
			self.capture_frame()

			if self.base_frame is None:
				self.set_base_frame(self.curr_gray_frame)

			self.detect_face()
			# if self.compare_frames() is False:
			# 	self.kill_camera()
			# 	return MOTION_DETECTED

			self.display_text_on_frame()
			self.display_frame_feed()
			self.on_frame_capture_error()
			self.exit_trigger()

	def set_base_frame(self, gray_frame):
		self.base_frame = gray_frame

	def compare_frames(self):
		self.video_text = NO_MOTION_DETECTED
		self.frame_delta = cv2.absdiff(self.base_frame, self.curr_gray_frame)
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
				cv2.rectangle(self.curr_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				self.video_text = MOTION_DETECTED
				return False

	def detect_face(self):
		faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

		faces = faceCascade.detectMultiScale(
		    self.curr_gray_frame,
		    scaleFactor=1.1,
		    minNeighbors=5,
		    minSize=(30, 30),
		    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)

		print "Found {0} faces!".format(len(faces))

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
		    cv2.rectangle(self.curr_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
