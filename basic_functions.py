import RPi.GPIO as GPIO
from time import sleep
from pynput import keyboard
from picamera import PiCamera
import time
import os
import sys
import numpy as np

#GLOBAL VARS
path = '/home/pi/Documents/'
pulse = 1/500
ms = [1, 1, 1]
xy = np.array([0, 0])
xy_records = np.array([0, 0])

#PINS DEFINITION
led = 13

step_gpio = 17
dir_gpio = 27

enable_motX = 4
enable_motY = 5
enable_motZ = 6

ms1 = 9
ms2 = 10
ms3 = 11


#SETUP RASP, GPIOS AND CAMERA
GPIO.setmode(GPIO.BCM)

camera = PiCamera()
time.sleep(1)
camera.resolution = (4056, 3040)
camera.iso = 100
camera.exposure_mode = 'off'
camera.shutter_speed = 10
print(camera.shutter_speed)

GPIO.setup(led, GPIO.OUT)

GPIO.setup(step_gpio, GPIO.OUT)
GPIO.setup(dir_gpio, GPIO.OUT)

GPIO.setup(enable_motX, GPIO.OUT)
GPIO.setup(enable_motY, GPIO.OUT)
GPIO.setup(enable_motZ, GPIO.OUT)

GPIO.setup(ms1, GPIO.OUT)
GPIO.setup(ms2, GPIO.OUT)
GPIO.setup(ms3, GPIO.OUT)


#BASIC FUNCTIONS
 
def lights_on_off():
    light = GPIO.input(led)
    if light == 0:
        GPIO.output(led, True)
    if light == 1:
        GPIO.output(led, False)
    return()


def step():
    for _ in range(5):
        sleep(pulse)
        GPIO.output(step_gpio, 1)
        sleep(pulse)
        GPIO.output(step_gpio, 0)
    return()


def micro_steps_on():
    GPIO.output(ms1, ms[0])
    GPIO.output(ms2, ms[1])
    GPIO.output(ms3, ms[2])
    return()


def micro_steps_off():
    GPIO.output(ms1, 0)
    GPIO.output(ms2, 0)
    GPIO.output(ms3, 0)
    return()
          

def micro_step():
    micro_steps_on()
    sleep(pulse)
    GPIO.output(step_gpio, 1)
    sleep(pulse)
    GPIO.output(step_gpio, 0)
    return()


def motor_left():
    
    global xy
    xy -= [1, 0]
    
    GPIO.output(enable_motX, 0)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 1)
    step()
    return()


def motor_right():
    
    global xy
    xy += [1, 0]
    
    GPIO.output(enable_motX, 0)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 0)
    step()
    return()


def motor_front():
    
    global xy
    xy += [0, 1]
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 0)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 0)
    step()
    return()


def motor_back():
    
    global xy
    xy -= [0, 1]
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 0)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 1)
    step()
    return()


def motor_up():
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 0)
    GPIO.output(dir_gpio, 0)
    micro_steps_on()
    step()
    return()


def motor_down():
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 0)
    GPIO.output(dir_gpio, 1)
    micro_steps_on()
    step()
    return()


def photos_numbering():
    for filename in os.listdir(path + "Database/"):
        name, _ = os.path.splitext(filename)
        yield int(name[3:])
    return()


def capture():
    if len(os.listdir(path + "Database/")) > 0:
        count = max(photos_numbering())
        count += 1
        camera.capture(path + "Database/" + 'img' + str(count) +'.jpg')
    else:
        camera.capture(path + "Database/" + 'img1.jpg')
    return()


def on_press(key):
    if key == keyboard.Key.left:
        motor_left()
    elif key == keyboard.Key.right:
        motor_right()
    elif key == keyboard.Key.up:
        motor_front()
    elif key == keyboard.Key.down:
        motor_back()
    elif key == keyboard.KeyCode.from_char('x'):
        motor_up()
    elif key == keyboard.KeyCode.from_char('z'):
        motor_down()
    elif key == keyboard.KeyCode.from_char('c'):
        capture()
    elif key == keyboard.Key.esc:
        sys.exit()
    elif key == keyboard.KeyCode.from_char('9'):
        GPIO.output(dir_gpio, 1)
        micro_step()
    elif key == keyboard.KeyCode.from_char('0'):
        GPIO.output(dir_gpio, 0)
        micro_step()
    elif key == keyboard.Key.enter:
        global xy_records
        xy_records = np.vstack([xy_records, xy])
    elif key == keyboard.KeyCode.from_char('l'):
        lights_on_off()


def on_release(key):
    if key == keyboard.KeyCode.from_char('x'):
        micro_steps_off()
    elif key == keyboard.KeyCode.from_char('z'):
        micro_steps_off()
    elif key == keyboard.KeyCode.from_char('9'):
        micro_steps_off()
    elif key == keyboard.KeyCode.from_char('0'):
        micro_steps_off()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()