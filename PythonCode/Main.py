from simple_pid import PID
import RPi_Movement as sens
#import CameraLib as cam
import time
import os

class Status:
	def __init__(self):
		self.prev = 0
	
	def __call__(self, num):
		#print("Controlling:", self.prev, num)
		resp = None
		if self.prev < 0 and num < 0:
			
			resp = False
		elif self.prev < 0 and num > 0:
			resp = True
		elif self.prev > 0 and num > 0:
			resp = False
		elif self.prev > 0 and num < 0:
			resp = True
		
		self.prev = num
		
		return resp

def getPid(distanza):
	pid_val = round(pid(distanza), 2)
	
	return pid_val
	

def destraFull():
	sens.avanti(10,10)
	time.sleep(0.7)
	sens.avanti(0, 80)
	
	time.sleep(3.4)
	sens.stop()
	time.sleep(0.1)
	sens.avanti(30, 30)
	time.sleep(0.7)

def sinistraFull():
	sens.avanti(10,10)
	time.sleep(0.1)
	sens.avanti(80, 0)
	
	time.sleep(3.4)
	sens.stop()
	time.sleep(0.1)
	sens.avanti(30, 30)
	time.sleep(0.7)

foundBlack = False


print("Starting")

pid = PID(1, 0.1, 0.05, setpoint=6.5, output_limits=(-30, 30))

pid.tunings = (3.0, 0.6, 1.2)
stat = Status()

start = time.time()
foundBlue = False

def PID_f(dist):
	if 6 < dist < 7:
		return 40, 40
	elif dist < 6:
		return 40, 20
	elif dist > 7:
		return 20, 40

while True:
	try:
		print("-------------")

		distDx = sens.distdx(2)
		
		colore_terra = sens.readNanoCode()
		#letteraDx = cam.get_frame_dx()
		#letteraSx = cam.get_frame_sx()
		#coloreDx = cam.get_color_dx()
		#coloreSx = cam.get_color_sx()
		
		#print("PID Components: ", pid.components)
		#print("destra:", letteraDx, coloreDx)
		#print("sinistra:", letteraSx, coloreSx)
		
		#print("Colore terra:",colore_terra)
		print("Distanza destra: ", distDx)
		
		#print(time.time() - start)
		#start = time.time()
		pid_val = round(getPid(distDx), 3) * 0.8
		time_elapsed_change = round(time.time() - start, 2)
		print("Tempo passato allo scorso cambiamento: ", time_elapsed_change)
		if stat(pid_val):
			print("CambiataDirezione")
			start = time.time()
		
		pid_sinistra, pid_destra = (30 + pid_val), (30 - pid_val)
		
		#if time_elapsed < 1.5:
		
		if pid_sinistra > 50:
			pid_sinistra = 50
		elif pid_sinistra < 0:
			pid_sinistra = 10
		
		if pid_destra > 50:
			pid_destra = 50
		elif pid_destra < 0:
				pid_destra = 10
		#else:
			#pid_sinistra, pid_destra = 30, 30
		
		print("Colore terra: ",colore_terra)
		# Reazione colore di terra
		if colore_terra == 0:
			foundBlue = False
		elif colore_terra == 1 and not foundBlue:
			foundBlack = False
			print("Aspettando 5 secondi")
			sens.stop()
			foundBlue = True
			time.sleep(5)
		elif colore_terra == 2:
			print("Bloccato")
			foundBlack = True
		
		
		#print(os.popen("vcgencmd measure_volts core").read())
		print("Velocità: ", pid_sinistra, pid_destra, pid_val)
		distAv = sens.distav(2)
		print(distAv)
		if distDx > 25:
			print("Scelto la destra")
			destraFull()
		elif distAv > 40 and not foundBlack:
			print("Scelto avanti")
			sens.avanti(pid_sinistra, pid_destra)
		elif sens.distsx(2) > 25:
			print("Scelta la sinistra")
			sinistraFull()
		elif distAv < 20:
			break
		else:
			print("Bloccato")
			while distAv < 40:
				distAv = sens.distav(2)
				print("Bloccato", distAv)
				sens.destra(20)
				time.sleep(0.3)
		
					
	except KeyboardInterrupt:
		sens.stopEverything()
		break
		
