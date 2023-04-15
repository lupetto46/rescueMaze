import RPi_Movement as mov
import SerialIO as sens
import time

def sleep(time_in_seconds: float):
	start = time.time()
	while time.time() - start < time_in_seconds:
		sens.getSensors()

def rotateOf(grades: int):
	currentGrades = getGyro(sensors.getSensors()) - (grades - offset)
	
	
	if currentGrades >= 360:
		currentGrades -= 360
	elif currentGrades < 0:
		currentGrades += 360 
	
	grad = getGyro(sensors.getSensors())
	
	error =4
	if grades < 0:
		print("Sinistra")
		mov.muovi(-10, 10)
	else:
		print("Destra")
		mov.muovi(10, -10)
	
	while not (currentGrades - error < grad < currentGrades + error):
		grad = getGyro(sensors.getSensors())
	
	mov.muovi(0, 0)

straightDegree = sens.getSensors()["gyro"]
offset = straightDegree - sens.getSensors()["gyro"]

while True:
	vals = sens.getSensors()
	
	print(vals["avDx"] ,vals["dtDx"],(vals["avDx"] + vals["dtDx"]) / 2)
	
