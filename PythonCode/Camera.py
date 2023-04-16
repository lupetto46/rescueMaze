import CameraLib as cam
import cv2


def findLetter():
	letter, conf = imgT()
	
	if letter:
		return letter
	else:
		return "None"

while True:
	
	print(findLetter())

	key = cv2.waitKey(1)
	if key == ord("q"):
		cv2.destroyAllWindows()
		break
	
