import RPi.GPIO as GPIO
from time import sleep
from pynput import keyboard
from picamera import PiCamera
import time
import os
import sys
from numpy import array, floor
import pygame
import copy


#GLOBAL VARS
pulse = 1/500
path = '/home/pi/Documents/Database/'
ms = [1, 1, 1]
xyz = array([0, 0, 0])
xy = array([186, 74])

screen = None
xyz_ini = None


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
camera.start_preview(fullscreen=False, window=(420,100,1014,760))

GPIO.setup(led, GPIO.OUT)

GPIO.setup(step_gpio, GPIO.OUT)
GPIO.setup(dir_gpio, GPIO.OUT)

GPIO.setup(enable_motX, GPIO.OUT)
GPIO.setup(enable_motY, GPIO.OUT)
GPIO.setup(enable_motZ, GPIO.OUT)

GPIO.setup(ms1, GPIO.OUT)
GPIO.setup(ms2, GPIO.OUT)
GPIO.setup(ms3, GPIO.OUT)

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS']='%i,%i' % (15,150)


#FUNCTIONS

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
    
    global xyz
    xyz -= [1, 0, 0]
    
    GPIO.output(enable_motX, 0)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 1)
    step()
    return()


def motor_right():
    
    global xyz
    xyz += [1, 0, 0]
    
    GPIO.output(enable_motX, 0)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 0)
    step()
    return()


def motor_front():
    
    global xyz
    xyz += [0, 1, 0]
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 0)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 0)
    step()
    return()


def motor_back():
    
    global xyz
    xyz -= [0, 1, 0]
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 0)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 1)
    step()
    return()


def motor_up():
    
    global xyz
    xyz += [0, 0, 1]
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 0)
    GPIO.output(dir_gpio, 0)
    micro_steps_on()
    step()
    
    return()


def motor_down():
    
    global xyz
    xyz -= [0, 0, 1]
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 0)
    GPIO.output(dir_gpio, 1)
    micro_steps_on()
    step()
    return()


def high_speed_ms():
    global ms
    ms = [1,0,0]
    return()


def low_speed_ms():
    global ms
    ms = [1,1,1]
    return()


def photos_numbering(path_):
    for filename in os.listdir(path_):
        name, _ = os.path.splitext(filename)
        yield int(name[3:])


def capture():
    if len(os.listdir(path)) > 0:
        count = max(photos_numbering())
        count += 1
        camera.capture(path + 'img' + str(count) +'.jpg')
    else:
        camera.capture(path + 'img1.jpg')
    return()


def tracker():
    
    global xy, xyz, xyz_ini, screen
    
    xyz_ini = copy.copy(xyz)[[0,1]]
    
    screen = pygame.display.set_mode((375, 150))
    pygame.draw.rect(screen, (255, 0, 0), (xy[0], xy[1], 3, 2))
    pygame.display.update()
    return()


def tracker_update():
    
    global xy, xyz, xyz_ini
   
    try:
        xy_update = xy + floor((xyz[[0,1]] - xyz_ini)/5.3333)
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (xy_update[0], xy_update[1], 3, 2))
        pygame.display.update()
    except:
        pass
    return()


def on_press(key):
    global xy, screen
    if key == keyboard.Key.left:
        motor_left()
        tracker_update()
    elif key == keyboard.Key.right:
        motor_right()
        tracker_update()
    elif key == keyboard.Key.up:
        motor_front()
        tracker_update()
    elif key == keyboard.Key.down:
        motor_back()
        tracker_update()
    elif key == keyboard.KeyCode.from_char('x'):
        motor_up()
    elif key == keyboard.KeyCode.from_char('z'):
        motor_down()
    elif key == keyboard.KeyCode.from_char('c'):
        capture()
    elif key == keyboard.KeyCode.from_char('1'):
        low_speed_ms()
    elif key == keyboard.KeyCode.from_char('2'):
        high_speed_ms()
    elif key == keyboard.Key.esc:
        camera.stop_preview()
        pygame.quit()
        sys.exit()
    elif key == keyboard.KeyCode.from_char('9'):
        GPIO.output(dir_gpio, 1)
        micro_step()
    elif key == keyboard.KeyCode.from_char('0'):
        GPIO.output(dir_gpio, 0)
        micro_step()
    elif key == keyboard.KeyCode.from_char('l'):
        lights_on_off()
    elif key == keyboard.KeyCode.from_char('t'):
        tracker()


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