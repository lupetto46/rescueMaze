import serial
import json
import time

arduino = serial.Serial(port='COM5', baudrate=19200, timeout=.1)

def printSerial(command):
    command += '#'
    arduino.flush()
    arduino.write(command.encode())

def readSerial():
    tdata = arduino.readline()

    tdata = tdata.decode("utf-8")
    if tdata != "" and tdata != " " and tdata !="\n":
        bob = json.loads(tdata)
        return bob
    else: 
        return {'gyro': -1}



def send(command):    
    printSerial(command)
    




def main():
    start = time.time()
    first = True
    while True:
        try:
            inz = input(": ")
            send(inz)
            recieved = readSerial()
            print(recieved)
                
            
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()