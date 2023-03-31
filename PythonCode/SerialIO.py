import serial
import json
import time

arduino = serial.Serial(port='COM4', baudrate=19200, timeout=.1)

def printSerial(command):
    arduino.write(bytes(command, "utf-8"))

def readSerial():
    tdata = arduino.readline()

    tdata = tdata.decode("utf-8")
    if tdata != "" and tdata != " " and tdata !="\n":
        return tdata
    else: 
        return "no data"

def send():
    printSerial()
    return readSerial().strip('#')

def recieve():
    readed = readSerial().splitlines()
    return readed



def main():
    while True:
        try:
            #send()
            recieved = recieve()
            if recieved != -1:
                print(recieved)
                
            
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()