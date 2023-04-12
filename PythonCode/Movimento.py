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
	currentGrades = getGyro(getSensors()) - grades
	
	
	if currentGrades >= 360:
		currentGrades -= 360
	elif currentGrades < 0:
		currentGrades += 360 
	
	grad = getGyro(sensors.getSensors())
	
	error = 8
	if grades < 0:
		print("Sinistra")
		mov.muovi(-15, 15)
	else:
		print("Destra")
		mov.muovi(15, -15)
	
	while not (currentGrades - error < grad < currentGrades + error):
		grad = getGyro(sensors.getSensors())
		#print(currentGrades, grad)
	
	mov.muovi(0, 0)
	
	
vals = sensors.getSensors()
gyroOffset = getGyro(vals)

maxOut = 20
setpoint = 3
	
pid = PID(1, 0.1, 0.05, setpoint=setpoint, output_limits=(-maxOut, maxOut))
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


def controlloMassimo(val1, val2):
	if val1 > val2:
		return -1
	elif val1 < val2:
		return 1
	else:
		return 0

sx, dx = 0, 0

class every:
	def __init__(self, number):
		self.num = number
		self.curNum = 0
		self.prevNum = 0
		
	def __call__(self, number):
		self.curNum += 1
		
		if self.curNum == self.num:
			self.prevNum = number
			self.curNum = 0
			return number
		else:
			return self.prevNum

ev = every(10)

def allinea(sx, dx):
	return sx == dx

def ruotaDestra():
	print("Destra")
	mov.muovi(20, 20)
	sleep(0.4)
	mov.muovi(0, 0)
	rotateOf(90)
	mov.muovi(20, 20)
	sleep(1.8)
	
def ruotaSinistra():
	mov.muovi(0, 0)
	sleep(0.1)
	mov.muovi(-20, -20)
	sleep(0.5)
	rotateOf(-90)
	mov.muovi(20, 20)
	sleep(1.8)

def getSensors():
	valsLoc = sensors.getSensors()
			
	return valsLoc

while True:
	try:
		start = time.time()
		vals = getSensors()
		#print(vals)
		offset = straightDegree - vals["gyro"]
		av, dt = getDx(vals)
		controllo = ev(controlloMassimo(dt, av))
		#print(valForPid)
		# Controllo muri
		print(vals)
		
		if (getDx(vals)[0] < 12 and getDx(vals)[1] < 12) and (getAv(vals)[0] < 1 and getAv(vals)[1] < 1) and (getSx(vals)[0] < 12 and getSx(vals)[1] < 12): # Tutti Muri
			mov.muovi(0, 0)
			sleep(0.1)
			mov.muovi(-20, -20)
			sleep(0.5)
			rotateOf(180)
		elif getDx(vals)[0] > 15 and getDx(vals)[1] > 15: # Destra
			ruotaDestra()
		elif (getAv(vals)[0] <= 1 and getAv(vals)[1] <= 1): # Muro avanti
			ruotaSinistra()
		else:
			#print(controllo)
			if setpoint - 3 < av < setpoint + 3:
				pass 
			if controllo == 1 and av <= 15:
				pidVal = pid(av)
				sx, dx = 20 + pidVal, 20 - pidVal
			elif controllo == -1 and dt <= 15:
				pidVal = pid(dt)
				sx, dx = 20 - pidVal, 20 + pidVal
			else:
				pidVal = pid(av)
				sx, dx = 20 + pidVal, 20 - pidVal
			
			mov.muovi(sx, dx)
		
		
		
		#print("Time:", time.time() - start)
	except KeyboardInterrupt:
		mov.muovi(0, 0)
		break
