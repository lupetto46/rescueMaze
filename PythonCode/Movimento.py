from simple_pid import PID
import RPi_Movement as mov
#import CameraLib as cam
import SerialIO as sensors
import time

def getDx(vals: dict):
	av, dt = vals["avDx"], vals["dtDx"]
	
	return av, dt

def getSx(vals: dict):
	av, dt = vals["avSx"], vals["dtSx"]
	
	return av, dt

def getAv(vals: dict):
	sx, dx = vals["sxAv"], vals["dxAv"]
	
	return sx, dx

def getGyro(vals: dict):
	return vals["gyro"]

def rotateOf(grades: int):
	currentGrades = getGyro(sensors.getSensors()) - grades
	
	
	if currentGrades >= 360:
		currentGrades -= 360
	elif currentGrades < 0:
		currentGrades += 360 
	
	grad = getGyro(sensors.getSensors())
	
	offSet =4
	if grades < 0:
		print("Sinistra")
		mov.muovi(-10, 10)
	else:
		print("Destra")
		mov.muovi(10, -10)
	
	while not (currentGrades - offSet < grad < currentGrades + offSet):
		grad = getGyro(sensors.getSensors())
	
	mov.muovi(0, 0)
	
	
vals = sensors.getSensors()
gyroOffset = getGyro(vals)

maxOut = 20
	
pid = PID(1, 0.1, 0.05, setpoint=4, output_limits=(-maxOut, maxOut))
pid.tunings = (7.0, 0.4, 2.0)
print("Starting")



while True:
	try:
		vals = sensors.getSensors()
		av, dt = getDx(vals)
		print("Av:", av)
		pidVal = pid(av)

		dx, sx = 20 + pidVal, 20 - pidVal

		print("Velictà ruote:",dx, sx)
		
		
		if getDx(vals)[0] > 10 and getDx(vals)[1] > 10:
			time.sleep(0.3)
			rotateOf(90)
			mov.muovi(40, 40)
			time.sleep(1)
		elif getAv(vals)[0] < 8 and getAv(vals)[1] < 8:
			mov.muovi(0, 0)
			rotateOf(-90)
		
		mov.muovi(dx, sx)
	except KeyboardInterrupt:
		mov.muovi(0, 0)
		break
