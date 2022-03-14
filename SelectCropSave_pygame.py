#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:55:18 2022

@author: jose
"""
import os
import pygame
from PIL import Image
import sys
from numpy import array
from pandas import read_csv, DataFrame

path = "/home/jose/Desktop/train/"


#LISTS OF IMAGES AND LABELS FILENAMES TO CROP
images = sorted([f for f in os.listdir(path + "images") if os.path.isfile(path + "images/" +f)])
labels = sorted(os.listdir(path + "labels"))

#CROP SIZE WINDOW
crop_size = 1000

#GETTING ORIGINAL IMAGES SIZE
im = Image.open(path + "images/" + images[0])
width, height = im.size

#DUMMY VARIABLE FOR SELECTING IMAGES
i = 0
#DUMMY VARIABLE FOR NAMING CROPPED IMAGES
j = 0


#DEFINING POSITION OF PYGAME WINDOW (TOP-LEFT CORNER)
os.environ['SDL_VIDEO_WINDOW_POS']='%i,%i' % (0,0)

#VARIABLES FOR DEFINING PYGAME WINDOW SIZE
X = int(width*0.45)
Y = int(height*0.45)

#SIZE FOR CROPPING RECTANGLE INSIDE RESIZED IMAGE
crop_xy = 1000*0.45

#COLORS FOR RECTANGLES
color_blue = (0,0,255)
color_green = (31,100,32)

#LIST FOR STORING THE CENTERS OF CROPPED IMAGES
crops_list = []


#-----------------------------------------------------
def crop_labels(crops_list_temp):
    
    global i
    
    cols_names = ["Class", "X_center", "Y_center", "Width", "Height"]
    original_labels = read_csv(path + "labels/" + labels[i], sep=" ", names=cols_names)
    
    
    original_labels[["X_center", "Width"]] = width*original_labels[["X_center", "Width"]]
    original_labels[["Y_center", "Height"]] = height*original_labels[["Y_center", "Height"]]
    
    original_labels = original_labels.astype(int)
    
    l = 0
    
    for center in crops_list_temp:
        
        temp_labels = []
        center = (array(center)/0.45).astype(int)
        
        for k in range(len(original_labels)):
            
            l_r_cond = (center[0]-500) - (original_labels.loc[k]["X_center"]+original_labels.loc[k]["Width"]/2) < 0
            r_l_cond = (center[0]+500) - (original_labels.loc[k]["X_center"]-original_labels.loc[k]["Width"]/2) > 0
            
            u_d_cond = (center[1]+500) - (original_labels.loc[k]["Y_center"]-original_labels.loc[k]["Height"]/2) > 0
            d_u_cond = (center[1]-500) - (original_labels.loc[k]["Y_center"]+original_labels.loc[k]["Height"]/2) < 0
            

            
            if (l_r_cond and r_l_cond) and (u_d_cond and d_u_cond):
                temp_labels.append(original_labels.loc[k])
            else:
                pass
            
        temp_labels = DataFrame(temp_labels)
      
        try:
            temp_labels["X_center"] = (temp_labels["X_center"]-(center[0]-500))/1000
            temp_labels["Y_center"] = (temp_labels["Y_center"]-(center[1]-500))/1000
            temp_labels["Width"] = temp_labels["Width"]/1000
            temp_labels["Height"] = temp_labels["Height"]/1000
                       
            index = temp_labels.loc[temp_labels.X_center + temp_labels.Width/2 > 1].index
            temp_labels.loc[index, "Width"] = 1 + temp_labels.Width/2 - temp_labels.X_center
            temp_labels.loc[index, "X_center"] = 1 - temp_labels.Width/2
            
            index = temp_labels.loc[temp_labels.X_center - temp_labels.Width/2 < 0].index
            temp_labels.loc[index, "Width"] = temp_labels.Width - (temp_labels.X_center - temp_labels.Width/2).abs()
            temp_labels.loc[index, "X_center"] = temp_labels.Width/2
            
            index = temp_labels.loc[temp_labels.Y_center - temp_labels.Height/2 < 0].index
            temp_labels.loc[index, "Height"] = temp_labels.Height - (temp_labels.Y_center - temp_labels.Height/2).abs()
            temp_labels.loc[index, "Y_center"] = temp_labels.Height/2
            
            index = temp_labels.loc[temp_labels.Y_center + temp_labels.Height/2 > 1].index
            temp_labels.loc[index, "Height"] = 1 + temp_labels.Height/2 - temp_labels.Y_center
            temp_labels.loc[index, "Y_center"] = 1 - temp_labels.Height/2
                        
            temp_labels.to_csv(path + "/cropped/labels/" + labels[i][:-4] + "_" + str(l) + ".txt", index=False, header=False, sep=' ')
            l += 1
        except:
            temp_labels.to_csv(path + "/cropped/labels/" + labels[i][:-4] + "_" + str(l) + ".txt", index=False, header=False, sep=' ')
            l += 1
    
    return()
#-----------------------------------------------------


def crop_fnc(pos):
    
    global i, j
    
    pos = tuple(array(pos)/0.45)
    img = Image.open(path + "images/" + images[i])
    box = (int(pos[0]-500), int(pos[1]-500), int(pos[0]+500), int(pos[1]+500))
    
    
    img.crop(box).save(path + "/cropped/images/" + images[i][:-4] + "_" + str(j) + ".jpg")
    
    return()
    

def mouse_LC(pos):
    
    image = pygame.image.load(path + "images/" + images[i])
    image = pygame.transform.scale(image, (X,Y))
    display_surface.blit(image, (0, 0))
    pygame.draw.rect(display_surface, color_blue, pygame.Rect(pos[0] - crop_xy/2, pos[1] - crop_xy/2, crop_xy, crop_xy),  3)
    pygame.display.update()
    
    return()
    

def mouse_RC(pos):
    
    global j, crops_list
    
    crop_fnc(pos)
    j += 1
    crops_list.append(pos)
    
    image = pygame.image.load(path + "images/" + images[i])
    image = pygame.transform.scale(image, (X,Y))
    display_surface.blit(image, (0, 0))
    for center in crops_list:
        pygame.draw.rect(display_surface, color_green, pygame.Rect(center[0] - crop_xy/2, center[1] - crop_xy/2, crop_xy, crop_xy),  3)
    pygame.display.update()
    return()


def keyboard_RA():
    
    global X, Y, i, j, crops_list
    
    crop_labels(crops_list)
    
    i += 1
    j = 0
    crops_list = []
    
    if i <= len(images)-1:
        image = pygame.image.load(path + "images/" + images[i])
        image = pygame.transform.scale(image, (X,Y))
        display_surface.blit(image, (0, 0))
        pygame.display.update()
    else:
        print('\a')
        i -= 1
    return()


def keyboard_LA():
    
    global X, Y, i, j, crops_list
    
    i-= 1
    j = 0
    crops_list = []
    
    if i >= 0:
        image = pygame.image.load(path + "images/" + images[i])
        image = pygame.transform.scale(image, (X,Y))
        display_surface.blit(image, (0, 0))
        pygame.display.update()
    else:
       print('\a')
       i += 1
    return()


def events_handler():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_RIGHT:
                keyboard_RA()
            elif event.key == pygame.K_LEFT:
                keyboard_LA()
       
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_LC(event.pos)
            elif event.button == 3:
                mouse_RC(event.pos)
    return()


pygame.init()
display_surface = pygame.display.set_mode((X,Y))
pygame.display.set_caption("Image")
image = pygame.image.load(path + "images/" + images[0])
image = pygame.transform.scale(image, (X,Y))
display_surface.blit(image, (0, 0))
pygame.display.update()

while True:
    events_handler()