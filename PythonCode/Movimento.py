from simple_pid import PID
import RPi_Movement as mov
import CameraLib as cam
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
	
	error = 10
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

maxOut = 20
setpoint = 5
	
pid = PID(1, 0.1, 0.05, setpoint=setpoint, output_limits=(-maxOut, maxOut))
#7.0, 0.4, 2.0
pid.tunings = (7.0, 0.4, 0.9)
print("Starting")


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

def ruotaDestra():
	print("Destra")
	mov.muovi(20, 20)
	sleep(0.4)
	mov.muovi(0, 0)
	rotateOf(60)
	start = time.time()
	while time.time() - start < 1.8:
		allinea()
	
def ruotaSinistra():
	mov.muovi(0, 0)
	sleep(0.1)
	mov.muovi(-20, -20)
	sleep(0.3)
	rotateOf(-60)
	notFound = False
	for i in range(100):
		if checkWall(bypass = True):
			break
	else:
		notFound = True
	if not notFound:
		imgT.setDelay()
	while time.time() - start < 1.8:
		allinea()

def allinea():
	if av > 6 and dt < 6:
		pid = PID(1, 0.1, 0.05, setpoint=setpoint, output_limits=(-maxOut, maxOut))
		#7.0, 0.4, 2.0
		pid.tunings = (7.0, 0.4, 2.0)
		pidVal = pid(av)
		sx, dx = 20 + pidVal, 20 - pidVal
	else:
		if av <= 10:
			pidVal = pid(av)
			sx, dx = 20 + pidVal, 20 - pidVal
		elif dt <= 10:
			pidVal = pid(dt)
			sx, dx = 20 - pidVal, 20 + pidVal
		elif dt > 10 and av > 10:
			mov.muovi(30, 10)
			sleep(0.4)
		else:
			sx, dx = 20, 20

def getSensors():
	valsLoc = sensors.getSensors()
			
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





def findLetter():
	letter, conf = imgT(debug=True)
	
	if letter:
		return letter
	else:
		return "None"
		
def checkWall(bypass= False):
	let = findLetter()
	
	mov.muovi(0, 0)
	
	print(let)
	
	if let == "Red":
		mov.lampeggiaLed(2)
		spara(3)
		if not bypass:
			imgT.setDelay()
		return True
	elif let == "S":
		mov.lampeggiaLed(2)
		spara(1)
		if not bypass:
			imgT.setDelay()
		return True
	elif let == "H":
		mov.lampeggiaLed(2)
		spara(3)
		if not bypass:
			imgT.setDelay()
		return True
	else:
		return False

imgT = cam.imageTaker(2.6)

while True:
	try:
		start = time.time()
		vals = getSensors()
		#print(vals)
		av, dt = getDx(vals)
		#print(valForPid)
		# Controllo muri
		print(vals)
		st = time.time()
		checkWall()
		print("time:", time.time() - st)
		
		
		if (getDx(vals)[0] < 12 and getDx(vals)[1] < 12) and (getAv(vals)[0] < 3 and getAv(vals)[1] < 3) and (getSx(vals)[0] < 12 and getSx(vals)[1] < 12): # Tutti Muri
			mov.muovi(0, 0)
			rotateOf(-60)
			for i in range(100):
				if checkWall(bypass = True):
					break
			rotateOf(-60)
			checkWall()
		elif getDx(vals)[0] > 15 and getDx(vals)[1] > 15: # Destra
			ruotaDestra()
		elif (getAv(vals)[0] <= 1 and getAv(vals)[1] <= 1): # Muro avanti
			ruotaSinistra()
		else:
			#print(controllo)
			
			if av > 6 and dt < 6:
				pid = PID(1, 0.1, 0.05, setpoint=setpoint, output_limits=(-maxOut, maxOut))
				#7.0, 0.4, 2.0
				pid.tunings = (7.0, 0.4, 2.0)
				pidVal = pid(av)
				sx, dx = 20 + pidVal, 20 - pidVal
			else:
				if av <= 10:
					pidVal = pid(av)
					sx, dx = 20 + pidVal, 20 - pidVal
				elif dt <= 10:
					pidVal = pid(dt)
					sx, dx = 20 - pidVal, 20 + pidVal
				elif dt > 10 and av > 10:
					mov.muovi(30, 10)
					sleep(0.4)
				else:
					sx, dx = 20, 20
			
			mov.muovi(sx, dx)
		
		
		#print("Time:", time.time() - start)
	except KeyboardInterrupt:
		mov.muovi(0, 0)
		cv2.destroyAllWindows()
		break
