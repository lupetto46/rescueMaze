import RPi_Movement as mov
import SerialIO as sensors
import time

vals = sensors.getSensors()

#Blu: 2234, 557, 810, 930 || 2261 631 812 913
#Nero: 980, 461, 325, 315
#Bianco Floor: 6004 2103 2245 2023 || 6803 2408 2511 2286 || 6210 2256 2253 2051

def getSensors():
	valsLoc = sensors.getSensors()
	for valname in valsLoc:
		if not (valname == "color" or valname == "gyro"):
			if valsLoc[valname] > 30:
				valsLoc[valname] = 10000
			
	return valsLoc
	
def getColor(vals: dict):
	lux, r,g,b = vals["color"]
	
	if lux < 2000:
		return 2 #Nro
	elif lux < 3000:
		return 1 #Blu
	else:
		return 0 #Bianco


def spara(num: int):
	sensors.printSerial(str(num))
	while True:
		sens = sensors.readSerial()
		#print(sens)
		if sens == "F\r\n":
			print("got response")
			break



def getGyro(vals: dict):
	return vals["gyro"]


def rotateOf(grades: int):
	currentGrades = getGyro(getSensors()) - grades
	
	
	if currentGrades >= 360:
		currentGrades -= 360
	elif currentGrades < 0:
		currentGrades += 360 
	
	grad = getGyro(sensors.getSensors())
	
	error = 2
	if grades < 0:
		print("Sinistra")
		mov.muovi(-15, 15)
	else:
		print("Destra")
		mov.muovi(15, -15)
	
	while not (currentGrades - error < grad < currentGrades + error):
		grad = getGyro(sensors.getSensors())
		print(currentGrades, grad)
	
	mov.muovi(0, 0)

rotateOf(-60)
