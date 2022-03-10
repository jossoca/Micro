#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 12:06:59 2022

@author: jose
"""
import cv2
import pandas as pd

path = "/home/jose/Desktop/train/cropped/"

img = cv2.imread(path + "images/" + 'img5_jpg.rf.9e053ded822f0956cb61278c34516561_1.jpg', cv2.IMREAD_UNCHANGED)
height, width, channels = img.shape
scale_percent = 50 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
 
# print('Resized Dimensions : ',resized.shape)


txt = pd.read_csv(path + "labels/" + "img5_jpg.rf.9e053ded822f0956cb61278c34516561_1.txt", sep=" ", header=None)


for i in range(len(txt)):
    
    ej1 = txt.loc[i][1:]
    
    x1 = [width*ej1[1]-width*ej1[3]/2, height*ej1[2]+height*ej1[4]/2]
    x1 = tuple([int(x) for x in x1])
    x2 = [width*ej1[1]+width*ej1[3]/2, height*ej1[2]-height*ej1[4]/2]
    x2 = tuple([int(x) for x in x2])
    
    color = (255, 0, 0)
    thickness = 2
    
    image = cv2.rectangle(resized, x1, x2, color, thickness)

cv2.imshow("img", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()