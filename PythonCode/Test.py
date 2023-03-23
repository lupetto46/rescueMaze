import RPi_Movement as sens
import time
from simple_pid import PID

def sinistraFull():
    sens.avanti(0,0)
    time.sleep(0.1)
    sens.sinistra(20)
    time.sleep(3.55)

sinistraFull()
