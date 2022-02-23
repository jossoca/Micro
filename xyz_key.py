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
from subprocess import check_output


#-----GLOBAL VARS-----

pulse = 1/500
path = '/home/pi/Documents/Database/'
ms = [1, 1, 1]
xyz = array([0, 0, 0])
vid_start_stop = 0


display_res  = list(map(int, str(check_output("xrandr  | grep \* | cut -d' ' -f4", shell=True))[2:-3].split('x')))

res_full_sensor = [4056, 3040]
aspect_ratio_full_sensor = 4056/3040

res_video = [1920, 1080]
aspect_ratio_video = 1920/1080

y_res = display_res[1] - int(11*display_res[1]/50)
prev_window_size = [int(y_res*aspect_ratio_full_sensor), y_res]
video_window_size = [int(y_res*aspect_ratio_video), y_res]

prev_window_pos = [int((display_res[0]-prev_window_size[0])/2), int(11*display_res[1]/50)]
video_window_pos = [int((display_res[0]-video_window_size[0])/2), int(11*display_res[1]/50)]

red= (255, 0, 0)
yellow = (255, 255, 0)
sample_aspect_ratio = 5/2.2
ratio_steps_pad = 2000/375

screen = None
xyz_ini = None


#-----PINS DEFINITION-----

led = 13

step_gpio = 17
dir_gpio = 27

enable_motX = 4
enable_motY = 5
enable_motZ = 6

ms1 = 9
ms2 = 10
ms3 = 11


#-----SETUP RASP, GPIOS AND CAMERA-----

GPIO.setmode(GPIO.BCM)

camera = PiCamera()
time.sleep(0.5)
camera.resolution = (res_full_sensor[0], res_full_sensor[1])
camera.start_preview(fullscreen=False, window=(prev_window_pos[0], prev_window_pos[1],
                                               prev_window_size[0], prev_window_size[1]))

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
os.environ['SDL_VIDEO_WINDOW_POS']='%i,%i' % (int((display_res[0] - display_res[0]/3.84)/2),0)


#-----FUNCTIONS-----

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
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 1)
    GPIO.output(enable_motZ, 0)
    
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
    xyz -= [0, 1, 0]
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 0)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 1)
    step()
    return()


def motor_back():
    
    global xyz
    xyz += [0, 1, 0]
    
    GPIO.output(enable_motX, 1)
    GPIO.output(enable_motY, 0)
    GPIO.output(enable_motZ, 1)
    GPIO.output(dir_gpio, 0)
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
        count = max(photos_numbering(path))
        count += 1
        camera.capture(path + 'img' + str(count) +'.jpg')
    else:
        camera.capture(path + 'img1.jpg')
    return()


def vid_capture():
    
    global vid_start_stop, camera
    
    if vid_start_stop == 0:
        
        camera.stop_preview()
        camera.resolution = (res_video[0], res_video[1])
        sleep(0.5)
        camera.start_preview(fullscreen=False, window=(video_window_pos[0], video_window_pos[1],
                                               video_window_size[0], video_window_size[1]))
        
        vid_start_stop = 1
        
        if len(os.listdir(path + "../Videos/")) > 0:
            count = max(photos_numbering(path + "../Videos/"))
            count += 1
            camera.start_recording(path + "../Videos/" + 'vid' + str(count) +'.h264')
        else:
            camera.start_recording(path + "../Videos/" + 'vid1.h264')
   
    elif vid_start_stop == 1:
        
        camera.stop_recording()
        
        camera.stop_preview()
        camera.resolution = (res_full_sensor[0], res_full_sensor[1])
        camera.start_preview(fullscreen=False, window=(prev_window_pos[0], prev_window_pos[1],
                                               prev_window_size[0], prev_window_size[1]))

        vid_start_stop =0
        
    return()


def tracker():
    
    global xyz, xyz_ini, screen
    
    xy = [0, 0]
    xyz_ini = copy.copy(xyz)[[0,1]]
    
    screen = pygame.display.set_mode((int(display_res[0]/3.84), int(display_res[0]/(3.84*sample_aspect_ratio))))
    pygame.draw.rect(screen, red, (xy[0], xy[1], 3, 2))
    pygame.display.update()
    return()


def history_tracker():
    
    global xyz, xyz_ini
    
    try:
        xy_update = floor((xyz[[0,1]] - xyz_ini)/ratio_steps_pad)
        pygame.draw.rect(screen, yellow, (xy_update[0], xy_update[1], 3, 2))
        pygame.display.update()
    except:
        pass
    return()


def tracker_update():
    
    global xyz, xyz_ini
    
    try:
        xy_update = floor((xyz[[0,1]] - xyz_ini)/ratio_steps_pad)
#         screen.fill((0, 0, 0))
        pygame.draw.rect(screen, red, (xy_update[0], xy_update[1], 3, 2))
        pygame.display.update()
        print(xy)
    except:
        pass
    return()


def on_press(key):

    if key == keyboard.Key.left:
        history_tracker()
        motor_left()
        tracker_update()
    elif key == keyboard.Key.right:
        history_tracker()
        motor_right()
        tracker_update()
    elif key == keyboard.Key.up:
        history_tracker()
        motor_front()
        tracker_update()
    elif key == keyboard.Key.down:
        history_tracker()
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
    elif key == keyboard.KeyCode.from_char('v'):     
        vid_capture()


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