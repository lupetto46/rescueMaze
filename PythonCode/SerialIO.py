import serial
import json
import time

arduino = serial.Serial(port='COM5', baudrate=19200, timeout=.1)

def printSerial(command: str):
    command += '#'
    arduino.flush()
    print("sending:", command)
    arduino.write(command.encode())

def readSerial():
    tdata = arduino.readline()

    tdata = tdata.decode("utf-8")
    if tdata != "" and tdata != " " and tdata !="\r\n":
        #bob = json.loads(tdata)
        return tdata
    else: 
        return {'gyro': -2}



    




def main():
    while True:
        try:
            printSerial("get")
            recieved = readSerial()
            print(recieved)
                
            
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()