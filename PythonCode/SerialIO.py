import serial
import time

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)

def printSerial():
    arduino.write(b'sensoredx: 280#')
    
def readSerial():
    tdata = arduino.read_until('#')
    tdata = tdata.decode("utf-8")
    if tdata != "" and tdata != " " and tdata !="\n":
        return tdata
    else:
        return "no data"
    




def main():

    while 1:
        try:
            
            printSerial()
            print(readSerial().strip('#'))
            time.sleep(1.1)
        except KeyboardInterrupt:
            break
        

if __name__ == "__main__":
    main()