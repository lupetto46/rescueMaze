from simple_pid import PID
import RPi_MovementTest as sens
import CameraLib as cam
import time
import math
import os

class ArrayScorrimento:
	
	def __init__(self, maxArrayLen=3):
		self.arrays = []
		self.maxArrayLen = maxArrayLen
	
	def add(self, value):
		if len(self.arrays) + 1 > self.maxArrayLen:
			del self.arrays[0]
		self.arrays.append(value)
	
	def getControll(self):
		cont = 0
		for i in self.arrays:
			if i > 15:
				cont += 1
		
		if cont == len(self.arrays):
			# Niente muro
			return True
		else:
			# Muro
			return False
	def reset(self):
		self.arrays = []

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
    sens.avanti(0,0)
    time.sleep(0.1)
    sens.muovi(-20, 20)
    time.sleep(2.0)

def sinistraFull():
    sens.avanti(0,0)
    time.sleep(0.1)
    sens.muovi(20, -20)
    time.sleep(2.0)

def avanti():
	sens.avanti(20, 20)
	time.sleep(1)
	
foundBlack = False

maxOut = 20

pid = PID(1, 0.1, 0.05, setpoint=10, output_limits=(-maxOut, maxOut))
# 6.0, 0.6, 2.0 
pid.tunings = (7.0, 0.6, 2.0)
stat = Status()


print("Starting")

old_distDx = 0

cubetti = 8

start = time.time()
start_letter = time.time() - 10
start_color = time.time() - 10
foundBlue = False
inizio = True

controll_time = 1
max_error = 2
velocitaDx, velocitaSx = 20, 20
contr = ArrayScorrimento()


with open("log.txt", "a") as f:
	f.write("Nuova run\n")
	while True:
		try:
			f.write("-------------\n")
			print("----------")
			

			colore_terra = sens.readNanoCode()
			time_elapsed_change = round(time.time() - start, 2)
			f.write("Tempo passato allo scorso cambiamento: " + str(time_elapsed_change) + "\n")
			
			print("Colore terra: ", colore_terra)
			
			if colore_terra == 0:
				foundBlue = False
			elif colore_terra == 1 and not foundBlue:
				foundBlack = False
				sens.avanti(20, 20)
				time.sleep(1)
				sens.stop()
				sens.ledBlink()
				
				foundBlue = True
				
			
			#pid_sinistra, pid_destra = (20 + pid_val), (20 - pid_val)
			
			#print(pid_sinistra, pid_destra)
			
			
			dist = sens.distdx(2)
			if dist != 0:
				distDx = dist
			else:
				distDx = 10
			contr.add(distDx)
			print("destra", distDx)
			if inizio or distDx != 0:
				prev_distDx = distDx
			
			pid_val = getPid(distDx)
			print("pid: ", pid_val)
			
			velocitaSx, velocitaDx = (20 + pid_val), (20 - pid_val)
			
			
			
			end = time.time() - start
			controll = contr.getControll()
			print("controll: ", controll)
			
			
			# 
			if (end > controll_time or inizio) or colore_terra == 2:
				sens.muovi(0, 0)
				distAv = sens.distav(2)
				time.sleep(0.06)
				distSx = sens.distsx(2)
				
				inizio = False
				start = time.time()
				print("0.5 secondi passati")
				end_letter = time.time() - start_letter
				end_color = time.time() - start_color
				print("End letter: ", end_letter)
				
				
				if end_letter > 10:
					
					
					lettera = cam.get_frame_sx()
					
					
					
					print("framdx: ", lettera)
					
					
					if lettera == 'S':
						sens.ledBlink(5)
						sens.writeToNano(2)
						cubetti -= 2
						start_letter = time.time()
					elif lettera == 'U':
						sens.ledBlink(5)
						start_letter = time.time()
					elif lettera == 'H':
						sens.ledBlink(5)
						sens.writeToNano(3)
						cubetti -= 3
						start_letter = time.time()
					elif (lettera == "Red" or lettera == "Yellow"):
						sens.ledBlink(5)
						sens.writeToNano(1)
						cubetti -= 2
						start_letter = time.time()
					elif lettera == "None":
						pass
				
				print(distDx, distAv)
				if colore_terra == 2:
					sens.muovi(-20, -20)
					time.sleep(1)
				
				distSx = sens.distsx(2)
				print(distSx)
				
				#if False:
				if (distAv < 10 or colore_terra == 2) and distSx > 10:
					sens.muovi(-20, -20)
					time.sleep(0.5)
					sinistraFull()
				elif (distAv < 10 or colore_terra == 2) and distSx < 15 and distDx < 10:
					
					sens.muovi(-20, -20)
					time.sleep(0.5)
					
					sinistraFull()
					sinistraFull()
				
						
						
						
				
				
			
			f.write("Colore terra: " + str(colore_terra) + "\n")
			# Reazione colore di terra
			
			
			print(velocitaSx, velocitaDx)
			sens.muovi(velocitaSx, velocitaDx)
			#print(os.popen("vcgencmd measure_volts core").read())
			#f.write("Velocità: "+ str(pid_sinistra) + " " + str(pid_destra) + " " + str(pid_val)+"\n")
			
			#print(distDx)
		except KeyboardInterrupt:
			sens.writeToNano(0)
			sens.stopEverything()
			break
			
