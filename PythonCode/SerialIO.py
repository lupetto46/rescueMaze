import serial
import time

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)

def printSerial():
    arduino.write(b'Ciao dal computer')

def readSerial():
    tdata = arduino.read_until('#')

    tdata = tdata.decode("utf-8")
    tdata.strip("\n")
    if tdata != "" and tdata != " " and tdata !="\n":
        return tdata
    else: 
        return "no data"

def send():
    printSerial()
    time.sleep(1.1)
    print(readSerial().strip('#'))

def recieve():
    print(readSerial().strip('#'))
    time.sleep(1.1) 



def main():
    while True:
        try:
            #send()
            recieve()
        except KeyboardInterrupt:
            break


if name == "main":
    main()