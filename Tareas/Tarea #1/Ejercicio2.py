# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:04:20 2016

@author: Perry
"""

import matplotlib.pyplot as plt
import random

#Object Point to hold (x,y) numbers
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Functions for plot.
def f1(p): 
    return Point(p.x*0.85 + p.y*0.04 + 0.0, p.x*-0.04 + p.y*0.85 + 1.6)
def f2(p): 
    return Point(-0.15*p.x + 0.28*p.y + 0.0, p.x*0.26 + p.y*0.24 + 0.44)
def f3(p): 
    return Point(p.x*0.2 + p.y*-0.26 + 0.0, p.x*0.23 + p.y*0.22 + 1.6)
def f4(p):
    return Point(p.x*0.0 + p.y*0.0, p.x*0.0 + p.y*0.16)

# First point
p = Point(random.random(), random.random())
# Then we declare our list to hold the points
pointsList = []         # List declared
pointsList.append(p)    # First element in
# Main loop for in program
for i in range(1, 100000):
    # First we generate a random value to determine the function we're using.    
    randFuncValue = random.random()
    
    # Then we place our n-point in the array     
    if randFuncValue <= 0.85:                       # For randFuncValue = 0.85
        pointsList.append(f1(pointsList[i-1]))
    elif randFuncValue <= 0.92:                     # For randFuncValue = 0.07
        pointsList.append(f2(pointsList[i-1]))
    elif randFuncValue <= 0.99:                     # For randFuncValue = 0.07
        pointsList.append(f3(pointsList[i-1]))
    else:                                           # for randFuncValue = 0.01
        pointsList.append(f4(pointsList[i-1]))
    
# After the for loop, we get all the x's ans y's to plot
xValues = [points.x for points in pointsList]
yValues = [points.y for points in pointsList]

# Plot the image 
plt.plot(xValues, yValues, '.', ms=0.1)
# Save the image
plt.savefig('Barnsley.png', dpi = 1080)