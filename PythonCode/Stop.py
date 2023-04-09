import RPi_Movement as sens
import SerialIO as sensors

sens.muovi(0, 0)

while True:
	print(sensors.getSensors())
