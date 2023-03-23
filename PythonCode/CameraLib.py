import cv2
from keras.models import load_model
import numpy as np
import os
import time

print("Getting camera\s")
camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)

print("Finished getting camera")

print("Loading model")
model = load_model(os.getcwd()+ "/model/keras_model.h5")
print("Model loaded")

print("Loading class names")
with open("model/labels.txt", "r") as f:
    class_names = f.readlines()
    for class_name in class_names:
        class_names[class_names.index(class_name)] = class_name.split(" ")[1][:-1]
print("Class names loaded: ", class_names)

print(f"Everithing loaded \nCamera1: {camera1.read()[0]} \nCamera2: {camera2.read()[0]}")


def getColors(frame, threshb=127, threshg=100, threshr=127, maxVal=255):
    b,g,r = cv2.split(frame)
    
    b = cv2.threshold(b, threshb, maxVal, cv2.THRESH_BINARY)[1]
    g = cv2.threshold(g, threshg, maxVal, cv2.THRESH_BINARY)[1]
    r = cv2.threshold(r, threshr, maxVal, cv2.THRESH_BINARY)[1]
    
    return cv2.merge((b,g,r))


def getCenter(frame):
    y, x, _ = frame.shape
    
    return int(y/2), int(x/2)


def getPortion(frame, portion):
    y, x, _ = frame.shape
    
    return int(y/portion), int(x/portion)


def bincount_app(a):
    a2D = a.reshape(-1,a.shape[-1])
    col_range = (256, 256, 256) # generically : a2D.max(0)+1
    a1D = np.ravel_multi_index(a2D.T, col_range)
    return np.unravel_index(np.bincount(a1D).argmax(), col_range)


def recognize(model, frame, class_names) -> str:
    image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)

    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    prediction = model.predict(image)
    prediction = np.argmax(prediction)
    return class_names[prediction]


#Ritorna la lettera della camera sinistra
def get_frame_sx():
    """Ritorna la lettera della camera sinistra"""
    ret, frame = camera1.read()
    if not ret:
        return "Camera non trovata"
    frame = frame[::-1]
    center = getCenter(frame)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    ret, thresh = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    
    if thresh[center[0], center[1], 0] == 0:
        return recognize(model, frame, class_names)
    else:
        return "none"


#Ritorna la lettera della camera sinistra
def get_frame_dx():
    """Ritorna la lettera della camera sinistra"""
    ret, frame = camera2.read()
    if not ret:
        return "Camera non trovata"
    frame = frame[::-1]
    center = getCenter(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    ret, thresh = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
    
    if thresh[center[0], center[1], 0] == 0:
        return recognize(model, frame, class_names)
    else:
        return "none"


#Ritorna il colore della camera sinistra
def get_color_sx():
    """Ritorna il colore della camera sinistra"""
    ret, frame = camera1.read()
    if not ret:
        return "Camera non trovata"
    frame = frame[::-1]
    cy, cx = getCenter(frame)
    py, px = getPortion(frame, 10)
    
    y1, x1, y2, x2 = cy - int(py/2), cx - int(px/2), cy + int(py/2), cx + int(px/2)
    
    portion = frame[y1:y2, x1:x2]
    
    colorFrame = getColors(portion)
    
    mostDomColor = np.array(bincount_app(colorFrame))
    
    if np.array_equiv(mostDomColor, np.array([0,0,255])):
        return "red"
    elif np.array_equiv(mostDomColor, np.array([0,255,255])):
        return "yellow"
    elif np.array_equiv(mostDomColor, np.array([0,255,0])):
        return "green"
    else:
        return "none"

#Ritorna il colore della camera sinistra
def get_color_dx():
    """Ritorna il colore della camera sinistra"""
    ret, frame = camera2.read()
    if not ret:
        return "Camera non trovata"
    frame = frame[::-1]
    cy, cx = getCenter(frame)
    py, px = getPortion(frame, 10)
    
    y1, x1, y2, x2 = cy - int(py/2), cx - int(px/2), cy + int(py/2), cx + int(px/2)
    
    portion = frame[y1:y2, x1:x2]
    
    
    
    colorFrame = getColors(portion)
        
    mostDomColor = np.array(bincount_app(colorFrame))
    
    if np.array_equiv(mostDomColor, np.array([0,0,255])):
        return "red"
    elif np.array_equiv(mostDomColor, np.array([0,255,255])):
        return "yellow"
    elif np.array_equiv(mostDomColor, np.array([0,255,0])):
        return "green"
    else:
        return "none"

