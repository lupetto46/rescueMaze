import cv2
import numpy as np
import os
import time
import tflite_runtime.interpreter as tflite

class imageTaker:
    def __init__(self, timeBetween: float):
        """Dependences: \n
        import time\n
        import cv2\n
        import numpy as np\n
        from keras.models import load_model"""
        self.timeBetween = timeBetween
        print("Loading model...")
        self.interpreter = tflite.Interpreter(model_path="model/model.tflite")
        self.interpreter.allocate_tensors()
        print("Loading camera...")
        self.capture = cv2.VideoCapture(0)
        print("Loading class names...")
        self.labels = [x.strip("\n") for x in open("model/labels.txt")]
        print("Finished loading labels: ", self.labels)
        self.prevTime = 0
        
        
    def __call__(self, debug=False):
        ret, image = self.capture.read()
        image = image[::-1]
        
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        
        if debug:
            cv2.imshow("Webcam Image", image)
            cv2.waitKey(1)
        
        if time.time() - self.prevTime > self.timeBetween:
            # Show the image in a window
            

            # Make the image a numpy array and reshape it to the models input shape.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            input_details = self.interpreter.get_input_details()
            
            width = input_details[0]['shape'][2]
            height = input_details[0]['shape'][1]
            
            
            
            image = np.asarray(image, dtype=np.uint8).reshape(1, width, height, 3)
            
            # Normalize the image array
            
            
            
            
            output_details = self.interpreter.get_output_details()
            
            
            # Predicts the model
            self.interpreter.set_tensor(input_details[0]['index'], image)
            self.interpreter.invoke()

            # Get the result 
            output_data = self.interpreter.get_tensor(output_details[0]['index'])
            confidence = np.max(output_data) / 255
            #print(self.interpreter.get_tensor(output_details[0]['quantization_parameters']["scales"]))
            label = self.labels[np.argmax(output_data[0])]
            
            if confidence > 0.97:
                return label, confidence
            else:
                return False, False
        else:
            return "None", 0

    def setDelay(self):
            self.prevTime = time.time()
    
    def takeImg(self):
        self.capture.read()


