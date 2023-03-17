import cv2
from keras.models import load_model
import numpy as np

print("Getting camera\s")
camera1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

print("Finished getting camera")

print("Loading model")
model = load_model("model/keras_model.h5")
print("Model loaded")

print("Loading class names")
with open("model/labels.txt", "r") as f:
    class_names = f.readlines()
    for class_name in class_names:
        class_names[class_names.index(class_name)] = class_name.split(" ")[1][:-1]
print("Class names loaded: ", class_names)

print("starting")
font = cv2.FONT_ITALIC
fps = 0
kernel = np.zeros((420, 640, 3), np.uint8)


def recognize(model, frame, class_names) -> str:
    image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    prediction = model.predict(image)
    prediction = np.argmax(prediction)
    return class_names[prediction]


def get_frame_sx():
    ret, frame = camera1.read()
    if not ret:
        return "Camera non trovata"

    return recognize(model, frame, class_names)


def get_frame_dx():
    ret, frame = camera2.read()
    if not ret:
        return "Camera non trovata"

    return recognize(model, frame, class_names)
