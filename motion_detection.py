import cv2


class Camera():

	def __init__(self):
		self.camera = cv2.VideoCapture(0)
		self.first_frame = None
		(self.grabbed, self.frame) = self.camera.read()
		
		print '### CAMERA'
		print self.grabbed
		print self.frame

		cv2.imshow("FEED", self.frame)


if __name__ == "__main__":
	motion_detection = Camera()