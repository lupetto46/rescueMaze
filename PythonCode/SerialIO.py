import serial
import time

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)

def readArduino():
    tdata = arduino.readline()
    tdata = tdata.decode("utf-8")
    tdata = tdata[:-2]
    return tdata

time.sleep(1)


while True:
    try:
        print(readArduino())
    except KeyboardInterrupt:
        break