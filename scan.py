import basic_functions as bf
import numpy as np
import math as mth

x_field, y_field = 11, 8

xy_records = bf.xy_records
xy = bf.xy

xy1 = np.array([min(xy_records[:,0]), max(xy_records[:,1])])
xy2 = np.array([max(xy_records[:,0]), max(xy_records[:,1])])
xy3 = np.array([max(xy_records[:,0]), min(xy_records[:,1])])
xy4 = np.array([min(xy_records[:,0]), min(xy_records[:,1])])


def start_position():
    
    global xy
    
    while xy[0] != xy1[0]:
        
        if xy[0] > xy1[0]:
            bf.motor_left()
            
        if xy[0] < xy1[0]:
            bf.motor_right()
        print(xy, "        -----       ", xy1)
            
    while xy[1] != xy1[1]:
    
        if xy[1] > xy1[1]:
            bf.motor_back()
        
        if xy[1] < xy1[1]:
            bf.motor_front()
        print(xy, "        -----       ", xy1)
    return()
   
   
   
def move_x_field(x_dir):
        
    if x_dir == 0:
        for _ in range(x_field):
            bf.motor_right()
    elif x_dir == 1:
        for _ in range(x_field):
            bf.motor_left()
            
    return()


def move_y_field():
    
    for _ in range(y_field):
        bf.motor_front()    
    return()


def scan():
    
    x_min, x_max = min(xy1[0], xy4[0]), max(xy2[0], xy3[0])
    y_min, y_max = min(xy3[1], xy4[1]), max(xy1[1], xy2[1])
    
    x_steps, y_steps = x_max - x_min, y_max - y_min
    
    start_position()
    
    x_dir = 0
    i = 25
    
    for _ in range(mth.ceil((y_steps/y_field))):
         
        for _ in range(mth.ceil((x_steps/x_field))):
            
            bf.camera.capture(bf.path + "Pr/" + 'img' +str(i) + ".jpg")
            move_x_field(x_dir)
            i += 1
            print(bf.xy)
            
        move_y_field()
        x_dir = 1 if x_dir == 0 else 0
        i += 1
        print(bf.xy)



scan()
print("Finish succesfully!")