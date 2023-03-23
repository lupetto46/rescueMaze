from simple_pid import PID
import RPi_Movement as sens
#import CameraLib as cam
import time

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
    sens.destra(20)
    time.sleep(3.45)

def sinistraFull():
    sens.avanti(0,0)
    time.sleep(0.1)
    sens.sinistra(20)
    time.sleep(3.45)
	

foundBlack = False


print("Starting")

pid = PID(1, 0.1, 0.05, setpoint=0, output_limits=(-30, 30))
pid.tunings = (3.0, 0.6, 2)
stat = Status()

start = time.time()
foundBlue = False

with open("log.txt", "a") as f:
	f.write("Nuova run\n")
	while True:
		try:
			f.write("-------------\n")

			distDx = sens.distdx(2)
			time.sleep(0.1)
			distSx = sens.distsx(2)
			
			error = distDx - distSx
			colore_terra = sens.readNanoCode()
			#letteraDx = cam.get_frame_dx()
			#letteraSx = cam.get_frame_sx()
			#coloreDx = cam.get_color_dx()
			#coloreSx = cam.get_color_sx()
			
			#print("PID Components: ", pid.components)
			#print("destra:", letteraDx, coloreDx)
			#print("sinistra:", letteraSx, coloreSx)
			
			#print("Colore terra:",colore_terra)
			f.write("Distanza destra: " + str(distDx) + "\n")
			f.write("Errore: " + str(error) + "\n")
			#print(time.time() - start)
			#start = time.time()
			pid_val = round(getPid(error), 3) * 0.8
			time_elapsed_change = round(time.time() - start, 2)
			f.write("Tempo passato allo scorso cambiamento: " + str(time_elapsed_change) + "\n")
			if stat(error):
				f.write("CambiataDirezione") 
				start = time.time()
				pid = PID(1, 0.1, 0.05, setpoint=6.5, output_limits=(-30, 30))
				pid.tunings = (3.0, 0.6, 2)
			
			pid_sinistra, pid_destra = (30 + pid_val), (30 - pid_val)
			
			
			f.write("Colore terra: " + str(colore_terra) + "\n")
			# Reazione colore di terra
			if colore_terra == 0:
				foundBlue = False
			elif colore_terra == 1 and not foundBlue:
				foundBlack = False
				f.write("Aspettando 5 secondi" + "\n")
				sens.stop()
				foundBlue = True
				time.sleep(5)
			elif colore_terra == 2:
				f.write("Bloccato\n")
				foundBlack = True
			
			
			#print(os.popen("vcgencmd measure_volts core").read())
			f.write("Velocità: "+ str(pid_sinistra) + " " + str(pid_destra) + " " + str(pid_val)+"\n")
			distAv = sens.distav(2)
			#print(distDx)
			if distDx > 25:
				f.write("Scelto Destra\n")
				destraFull()
				pid = PID(1, 0.1, 0.05, setpoint=6.5, output_limits=(-30, 30))
				pid.tunings = (3.0, 0.6, 2)
			elif distAv > 20:
				f.write("Scelto Avanti\n")
				sens.avanti(pid_sinistra, pid_destra)
			elif distSx > 25:
				f.write("Scelto Sinistra\n")
				sinistraFull()
				pid = PID(1, 0.1, 0.05, setpoint=6.5, output_limits=(-30, 30))
				pid.tunings = (3.0, 0.6, 2)
			elif distDx < 25 and distAv < 20 and distSx < 25:
				f.write("Scelto 180\n")
				destraFull()
				destraFull()
				pid = PID(1, 0.1, 0.05, setpoint=6.5, output_limits=(-30, 30))
				pid.tunings = (3.0, 0.6, 2)
		except KeyboardInterrupt:
			sens.stopEverything()
			break
			
