from time import sleep
import RPi.GPIO as GPIO


pulse = 500/1000000     #Minimum delay needed for generating a pulse

no_pulse_x_fov = 200    #Number of steps needed for advancing a FOV in x direction
no_pulse_y_fov = 150    #Number of steps needed for advancing a FOV in y direction

CW = 1     # Clockwise Rotation Motor
CCW = 0    # Counterclockwise Rotation

DIRx = 20   # Direction GPIO Pin Motor X
STEPx = 21  # Step GPIO Pin Motor X

DIRy = 7    # Direction GPIO Pin Motor Y
STEPy = 1   # Step GPIO Pin Motor Y


GPIO.setmode(GPIO.BCM)

GPIO.setup(DIRx, GPIO.OUT)
GPIO.setup(STEPx, GPIO.OUT)
GPIO.output(DIRx, CW)

GPIO.setup(DIRy, GPIO.OUT)
GPIO.setup(STEPy, GPIO.OUT)
GPIO.output(DIRy, CW)

def autofocus():
    return(print("Autofocus"))
    
def photo():
    return(print("Ka-chick"))
    
def home():
    return()
    
def step_x_fov():
    for x in range(no_pulse_x_fov):
        GPIO.output(STEPx, GPIO.HIGH)
        sleep(pulse)
        GPIO.output(STEPx, GPIO.LOW)
        sleep(pulse)
    return()

def step_y_fov():
    for y in range(no_pulse_y_fov):
        GPIO.output(STEPy, GPIO.HIGH)
        sleep(pulse)
        GPIO.output(STEPy, GPIO.LOW)
        sleep(pulse)
    return()

for fov in range(y_length):

    for x in range(x_length):
        autofocus()
        photo()
        step_x_fov()
    
    step_y_fov()
    
    if DIRx == CW:
        GPIO.output(DIRx, CCW)
    elif DIRx == CCW:
        GPIO.output(DIRx, CW)
        
home()

GPIO.cleanup()
