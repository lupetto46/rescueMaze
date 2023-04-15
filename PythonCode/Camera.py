import cv2

camera = cv2.VideoCapture(0)

while True:
	ret, frame = camera.read()
	frame = frame[::-1]
	
	cv2.imshow("frame", frame)
	
	
	key = cv2.waitKey(1)
	if key == ord("q"):
		cv2.destroyAllWindows()
		break
