from simple_pid import PID
import RPi_Movement as mov
#import CameraLib as cam
import SerialIO as sensors
import time

def sleep(time_in_seconds: float):
	start = time.time()
	while time.time() - start < time_in_seconds:
		sensors.getSensors()

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

def getColor(vals: dict):
	c, r, g, b = vals["color"]
	
	return c, r, g, b

def rotateOf(grades: int):
	currentGrades = getGyro(sensors.getSensors()) - grades
	
	
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
		print(currentGrades, grad)
	
	mov.muovi(0, 0)
	
	
vals = sensors.getSensors()
gyroOffset = getGyro(vals)

maxOut = 20
	
pid = PID(1, 0.1, 0.05, setpoint=6, output_limits=(-maxOut, maxOut))
#7.0, 0.4, 2.0
pid.tunings = (7.0, 0.4, 0.5)
print("Starting")

print(getColor(vals))
while True:
	try:
		straightDegree = vals["gyro"]
		offset = straightDegree - vals["gyro"]
		break
	except:
		pass


while True:
	try:
		start = time.time()
		vals = sensors.getSensors()
		#print(vals)
		offset = straightDegree - vals["gyro"]
		av, dt = getDx(vals)
		valForPid = (av+dt) / 2
		pidVal = pid(valForPid)
		print(valForPid)
		# Controllo muri
		if getDx(vals)[0] > 15 and getDx(vals)[1] > 15: # Destra
			mov.muovi(20, 20)
			sleep(0.2)
			rotateOf(90)
			straightDegree = sensors.getSensors()["gyro"]
			mov.muovi(40, 40)
			sleep(1)
			pid = PID(1, 0.1, 0.05, setpoint=4, output_limits=(-maxOut, maxOut))
			#7.0, 0.4, 2.0
			pid.tunings = (7.0, 0.4, 1.0)
		elif getAv(vals)[0] < 8 and getAv(vals)[1] < 8: # Muro avanti
			mov.muovi(0, 0)
			sleep(0.4)
			mov.muovi(0, 0)
			rotateOf(-90)
			straightDegree = sensors.getSensors()["gyro"]
			mov.muovi(40, 40)
			sleep(1)
			pid = PID(1, 0.1, 0.05, setpoint=4, output_limits=(-maxOut, maxOut))
			#7.0, 0.4, 2.0
			pid.tunings = (7.0, 0.4, 1.0)
		else:
			sx, dx = 20 + pidVal, 20 - pidVal
			mov.muovi(sx, dx)
		
		#print("Time:", time.time() - start)
	except KeyboardInterrupt:
		mov.muovi(0, 0)
		break
