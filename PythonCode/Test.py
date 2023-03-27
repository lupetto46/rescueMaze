import RPi_MovementTest as sens
import time
import os
import cv2


if False: 
	print("Loading model")
	model = load_model(os.getcwd()+ "/model/keras_model.h5")
	print("Model loaded")

	print("Loading class names")
	with open("model/labels.txt", "r") as f:
		class_names = f.readlines()
		for class_name in class_names:
			class_names[class_names.index(class_name)] = class_name.split(" ")[1][:-1]
	print("Class names loaded: ", class_names)

	def recognize(model, frame, class_names) -> str:
		image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

		image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
		image = (image / 127.5) - 1

		prediction = model.predict(image)
		prediction = np.argmax(prediction)
		return class_names[prediction]



cam = cv2.VideoCapture(-1)


def avanti():
	ret, frame = cam.read()
	if not ret:
		return
	frame= frame[::-1]
	
	cv2.imshow("frame", frame)



sens.writeToNano(1)
if False:
	while True:
		avanti()
		
		key = cv2.waitKey(1)
		if key == ord("q"):
			cv2.destroyAllWindows()
			break
	
	

sens.spegniLed()
sens.stop()
