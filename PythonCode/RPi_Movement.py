import RPi.GPIO as GPIO
import time
import Bluetin_Echo as sensor

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

N1 = 12
N2 = 13
N3 = 18
N4 = 19

sensorDx = sensor.Echo(trigDx, echoDx)
sensorSx = sensor.Echo(trigSx, echoSx)
sensorAv = sensor.Echo(trigAv, echoAv)

GPIO.setup(bit1, GPIO.IN)
GPIO.setup(bit2, GPIO.IN)

GPIO.setup(led, GPIO.OUT)

GPIO.setup(N1, GPIO.OUT)
GPIO.setup(N2, GPIO.OUT)
GPIO.setup(N3, GPIO.OUT)
GPIO.setup(N4, GPIO.OUT)

P1 = GPIO.PWM(N1, 1000)
P2 = GPIO.PWM(N2, 1000)
P3 = GPIO.PWM(N3, 1000)
P4 = GPIO.PWM(N4, 1000)

P1.start(0)
P2.start(0)
P3.start(0)
P4.start(0)

def ledBlink(iterations=1):
    for i in range(iterations):
        GPIO.output(led, True)
        time.sleep(0.3)
        GPIO.output(led, False)
        time.sleep(0.3)
        

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
    
    distance = sensorDx.read('cm', 5)
    
    if round_float is not None:
        distance = round(distance, round_float)

    return distance

    

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
    time.sleep(0.2)

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

def destra(velocita):
    P1.ChangeDutyCycle(0)
    P2.ChangeDutyCycle(velocita)

    P4.ChangeDutyCycle(velocita)
    P3.ChangeDutyCycle(0)

def sinistra(velocita):
    P2.ChangeDutyCycle(0)
    P1.ChangeDutyCycle(velocita)

    P3.ChangeDutyCycle(velocita)
    P4.ChangeDutyCycle(0)

def stopEverything():
    sensorAv.stop()
    sensorDx.stop()
    sensorSx.stop()
    GPIO.cleanup()
