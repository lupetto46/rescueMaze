import serial
import json

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=19200, timeout=.1)

def printSerial(command: str):
    command += '#'
    arduino.flush()
    arduino.write(command.encode())

def readSerial():
    dataInput = arduino.readline()

    dataInput = dataInput.decode("utf-8")
    if dataInput != "" and dataInput != " " and dataInput !="\r\n":
        return dataInput
    else: 
        return -1

def getJson():
    readed = readSerial()
    if readed != -1:
        return json.loads(readed)

def getSensors():
    recieved = getJson()
    if recieved == None:
        return None
    if recieved != -1:
        return recieved
        
