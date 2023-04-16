import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

led = 23
#Motori destra
N1 = 12
N2 = 13
#Motori sinistra
N3 = 19
N4 = 18

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


def accendiLed():
    GPIO.output(led, True)
    
def spegniLed():
    GPIO.output(led, False)

def lampeggiaLed(volte: int):
    for i in range(volte):
        accendiLed()
        time.sleep(0.4)
        spegniLed()
        time.sleep(0.4)

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
        sinistra(-1*sinistra_, destra_)
    elif sinistra_ > 0 and destra_ < 0:
        destra(sinistra_, -1*destra_)
    elif sinistra_ < 0 and destra_ < 0:
        indietro(-1*sinistra_, -1*destra_)
        
if __name__ == "__main__":
    P1.ChangeDutyCycle(0)
    P2.ChangeDutyCycle(50)
    time.sleep(2)
        
