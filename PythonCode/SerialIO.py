import serial

arduino = serial.Serial(port='COM5', baudrate=19200, timeout=.1)

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