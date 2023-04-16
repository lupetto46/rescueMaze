import serial
import json
import time

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=19200, timeout=1)

def printSerial(command: str):
    command += '\n'
    arduino.flush()
    arduino.write(command.encode())

def readSerial():
    arduino.flushInput()
    dataInput = arduino.readline()
    
    
    dataInput = dataInput.decode("utf-8")
    
    
    while dataInput == '\r\n':
        dataInput = arduino.readline()
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
        
