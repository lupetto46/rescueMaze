import RPi_Movement as mov
import SerialIO as sensors
import time

vals = sensors.getSensors()

def getSensors():
	valsLoc = sensors.getSensors()
	for valname in valsLoc:
		if not (valname == "color" or valname == "gyro"):
			if valsLoc[valname] > 30:
				valsLoc[valname] = 10000
			
	return valsLoc

while True:
	print(getSensors())
