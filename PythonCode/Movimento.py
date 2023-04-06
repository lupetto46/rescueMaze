from simple_pid import PID
import RPi_Movement as mov
#import CameraLib as cam
import SerialIO as sensors

def getDx():
	vals = sensors.getSensors()
	#print(vals)
	av= vals["avDx"]
	dt = vals["dtDx"]
	
	return av, dt

maxOut = 30
	
pid = PID(1, 0.1, 0.05, setpoint=0, output_limits=(-maxOut, maxOut))

print("Starting")

while True:
	av, dt = getDx()
	print(av, dt)
	
