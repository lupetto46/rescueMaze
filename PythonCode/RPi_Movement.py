import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

trigDx = 17
echoDx = 27
trigAv = 23  # 16
echoAv = 24  # 18
trigSx = 5
echoSx = 6

N1 = 12
N2 = 13
N3 = 18
N4 = 19

GPIO.setup(N1, GPIO.OUT)
GPIO.setup(N2, GPIO.OUT)
GPIO.setup(N3, GPIO.OUT)
GPIO.setup(N4, GPIO.OUT)

GPIO.setup(trigDx, GPIO.OUT)
GPIO.setup(echoDx, GPIO.IN)

GPIO.setup(trigAv, GPIO.OUT)
GPIO.setup(echoAv, GPIO.IN)

GPIO.setup(trigSx, GPIO.OUT)
GPIO.setup(echoSx, GPIO.IN)

P1 = GPIO.PWM(N1, 400)
P2 = GPIO.PWM(N2, 400)
P3 = GPIO.PWM(N3, 400)
P4 = GPIO.PWM(N4, 400)

P1.start(0)
P2.start(0)
P3.start(0)
P4.start(0)

def distav():
    GPIO.output(trigAv, True)
    time.sleep(0.00001)
    GPIO.output(trigAv, False)

    start_time = 0
    end_time = 0

    while GPIO.input(echoAv) == 0:
        start_time = time.time()
    while GPIO.input(echoAv) == 1:
        end_time = time.time()
        if end_time - start_time > 100000:
            break

    time_elapsed = end_time - start_time

    distance = (time_elapsed * 34300) / 2
    
    time.sleep(0.1)

    return int(distance)

def distdx():
    print(GPIO.input(echoDx))
    GPIO.output(trigDx, True)
    time.sleep(0.00001)
    GPIO.output(trigDx, False)
    
    start_time = 0
    end_time = 0
    print(GPIO.input(echoDx))
    while GPIO.input(echoDx) == 0:
        start_time = time.time()
        print(start_time)
    while GPIO.input(echoDx) == 1:
        end_time = time.time()
        #print(end_time, "-", start_time, "=", end_time-start_time)
        if end_time - start_time > 100000:
            break

    time_elapsed = end_time - start_time

    distance = (time_elapsed * 34300) / 2
    
    time.sleep(0.1)

    return int(distance)

    

def distsx():
    GPIO.output(trigSx, True)
    time.sleep(0.00001)
    GPIO.output(trigSx, False)

    start_time = 0
    end_time = 0

    while GPIO.input(echoSx) == 0:
        start_time = time.time()
    while GPIO.input(echoSx) == 1:
        end_time = time.time()
        
        if end_time - start_time > 100000:
            break

    time_elapsed = end_time - start_time

    distance = (time_elapsed * 34300) / 2
    
    time.sleep(0.1)

    return int(distance)

    

def stop():
    P1.ChangeDutyCycle(0)
    P2.ChangeDutyCycle(0)

    P4.ChangeDutyCycle(0)
    P3.ChangeDutyCycle(0)
    time.sleep(0.2)

def avanti(velocita):
    P1.ChangeDutyCycle(velocita)
    P2.ChangeDutyCycle(0)

    P4.ChangeDutyCycle(velocita)
    P3.ChangeDutyCycle(0)

def indietro(velocita):
    P2.ChangeDutyCycle(velocita)
    P1.ChangeDutyCycle(0)

    P3.ChangeDutyCycle(velocita)
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
