import numpy as np
from PIL import Image, ImageOps
import time
import os

path = "/home/jose/Documents/Ecosur/Doctorado/Microscopio/Codigo/Fotos/"
filenames = os.listdir(path)

# ------------------------------------------------------------
def laplacian(img):
    
    ker = np.stack([-1*np.ones(rows), 2*np.ones(rows), -1*np.ones(rows)]).T
    
    af = 0
    for y in range(1, cols-1):
        af += np.sum(np.sum(img[:, y-1:y+2]*ker, axis=1)**2)
 
    return(af)
# -------------------------------------------------------------

# ------------------------------------------------------------
def brenner(img):
    
    ker = np.stack([np.ones(rows), np.zeros(rows), -1*np.ones(rows)]).T
    
    af = 0
    for y in range(1, cols-1):
        af += np.sum(np.sum(img[:, y-1:y+2]*ker, axis=1)**2)
 
    return(af)
# -------------------------------------------------------------

# ------------------------------------------------------------
def sq_grad(img):
    
    ker = np.stack([np.ones(rows), -1*np.ones(rows)]).T
    
    af = 0
    for y in range(1, cols):
        af += np.sum(np.sum(img[:, y-1:y+1]*ker, axis=1)**2)
 
    return(af)
# -------------------------------------------------------------

# ------------------------------------------------------------
def var(img):
    
    average = np.mean(img)
    
    af = np.sum((imgArray-average).**2)/average
    
    return(af)
# -------------------------------------------------------------

l = {}
for file in filenames:

    img = Image.open(path + file)
    img = ImageOps.grayscale(img)
    imgArray = np.array(img)
    
    rows, cols = imgArray.shape
    
    
    start = time.time()
    
    af = var(imgArray)
    
    l[file] = af
   
    end = time.time()
    print("Tiempo de cómputo: ", end - start)
