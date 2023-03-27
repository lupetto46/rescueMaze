import RPi.GPIO as GPIO
import time
import Bluetin_Echo as sensor
import math

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

trigDx = 17
echoDx = 27
trigAv = 23  # 16
echoAv = 24  # 18
trigSx = 5
echoSx = 6
led = 26

bit1 = 25
bit2 = 16

bit1nano = 1
bit2nano = 7

N1 = 12
N2 = 13
N3 = 18
N4 = 19

sensorDx = sensor.Echo(trigDx, echoDx)
sensorSx = sensor.Echo(trigSx, echoSx)
sensorAv = sensor.Echo(trigAv, echoAv)

GPIO.setup(bit1nano, GPIO.OUT)
GPIO.setup(bit2nano, GPIO.OUT)

GPIO.setup(bit1, GPIO.IN)
GPIO.setup(bit2, GPIO.IN)

GPIO.setup(led, GPIO.OUT)

GPIO.setup(N1, GPIO.OUT)
GPIO.setup(N2, GPIO.OUT)
GPIO.setup(N3, GPIO.OUT)
GPIO.setup(N4, GPIO.OUT)

P1 = GPIO.PWM(N1, 50)
P2 = GPIO.PWM(N2, 50)
P3 = GPIO.PWM(N3, 50)
P4 = GPIO.PWM(N4, 50)

P1.start(0)
P2.start(0)
P3.start(0)
P4.start(0)

GPIO.output(bit1nano, False)
GPIO.output(bit2nano, False)

def accendiLed():
    GPIO.output(led, True)
    
def spegniLed():
    GPIO.output(led, False)

def ledBlink(iterations=1):
    start = time.time()
    while time.time() - start < 5: 
        accendiLed()
        time.sleep(0.3)
        spegniLed()
        time.sleep(0.3)
    spegniLed()
        

def readNanoCode():
    bit1val, bit2val = GPIO.input(bit1), GPIO.input(bit2)
    
    code = bit2val + (2 * bit1val)
    return code

def distav(round_float = None):
    if False:
        GPIO.output(trigAv, True)
        time.sleep(0.00001)
        GPIO.output(trigAv, False)

        start_time = 0
        end_time = time.time()

        while GPIO.input(echoAv) == 0:
            start_time = time.time()
            if start_time - end_time > 1:
                print(start_time - end_time)
                break
        while GPIO.input(echoAv) == 1:
            end_time = time.time()
            if end_time - start_time > 1:
                break

        time_elapsed = end_time - start_time

        distance = (time_elapsed * 34300) / 2
    
    distance = sensorAv.read('cm', 5)
    
    if round_float is not None:
        distance = round(distance, round_float)
    
    return distance

def distdx(round_float = None):
    if False:
        GPIO.output(trigDx, True)
        time.sleep(0.00001)
        GPIO.output(trigDx, False)
        
        start_time = 0
        end_time = time.time()
        while GPIO.input(echoDx) == 0:
            start_time = time.time()
            if start_time - end_time > 1:
                print(start_time - end_time)
                break
        while GPIO.input(echoDx) == 1:
            end_time = time.time()
            if end_time - start_time > 1:
                break

        time_elapsed = end_time - start_time

        distance = (time_elapsed * 34300) / 2
    
    distance = sensorDx.read('cm', 2)
    
    if round_float is not None:
        distance = round(distance, round_float)

    return distance




def writeToNano(val):
    if val == 1:
        GPIO.output(bit1nano, True)
        GPIO.output(bit2nano, False)
    elif val == 2:
        GPIO.output(bit1nano, False)
        GPIO.output(bit2nano, True)
    elif val == 3:
        GPIO.output(bit1nano, True)
        GPIO.output(bit2nano, True)
    else:
        GPIO.output(bit1nano, False)
        GPIO.output(bit2nano, False)
    time.sleep(0.1)
    start = time.time()
    end = time.time()
    while readNanoCode() != 3:
        print("No nano response")
    GPIO.output(bit1nano, False)
    GPIO.output(bit2nano, False)


def distsx(round_float = None):
    if False:
        GPIO.output(trigSx, True)
        time.sleep(0.00001)
        GPIO.output(trigSx, False)

        start_time = 0
        end_time = time.time()

        while GPIO.input(echoSx) == 0:
            start_time = time.time()
            if start_time - end_time > 1:
                print(start_time - end_time)
        while GPIO.input(echoSx) == 1:
            end_time = time.time()
            
            if end_time - start_time > 1:
                break

        time_elapsed = end_time - start_time

        distance = (time_elapsed * 34300) / 2
    
    distance = sensorSx.read('cm', 5)
    
    if round_float is not None:
        distance = round(distance, round_float)
    
    return distance



def stop():
    P1.ChangeDutyCycle(0)
    P2.ChangeDutyCycle(0)

    P4.ChangeDutyCycle(0)
    P3.ChangeDutyCycle(0)

def avanti(destra, sinistra):
    P1.ChangeDutyCycle(destra)
    P2.ChangeDutyCycle(0)

    P4.ChangeDutyCycle(sinistra)
    P3.ChangeDutyCycle(0)

def indietro(destra, sinistra):
    P2.ChangeDutyCycle(destra)
    P1.ChangeDutyCycle(0)

    P3.ChangeDutyCycle(sinistra)
    P4.ChangeDutyCycle(0)

def destra(destra, sinistra):
    P1.ChangeDutyCycle(0)
    P2.ChangeDutyCycle(destra)

    P4.ChangeDutyCycle(sinistra)
    P3.ChangeDutyCycle(0)

def sinistra(destra, sinistra):
    P2.ChangeDutyCycle(0)
    P1.ChangeDutyCycle(destra)

    P3.ChangeDutyCycle(sinistra)
    P4.ChangeDutyCycle(0)

def stopEverything():
    GPIO.setmode(GPIO.BCM)
    sensorAv.stop()
    sensorDx.stop()
    GPIO.cleanup()



def muovi(sinistra_, destra_):
    if sinistra_ >= 0 and destra_ >= 0:
        avanti(sinistra_, destra_)
    elif sinistra_ < 0 and destra_ > 0:
        destra(-1*sinistra_, destra_)
    elif sinistra_ > 0 and destra_ < 0:
        sinistra(sinistra_, -1*destra_)
    elif sinistra_ < 0 and destra_ < 0:
        indietro(-1*sinistra_, -1*destra_)
        
