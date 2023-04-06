#!/usr/bin/env python
# coding: utf-8

# In[1]:


from vpython import * 
from pypylon import pylon
import cv2 as cv
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.ticker import FormatStrFormatter
import time
from openpyxl import Workbook
import xlwt
from datetime import datetime
import random
from itertools import count
from IPython.display import display, clear_output
from matplotlib.animation import FuncAnimation
from drawnow import drawnow
from bokeh.plotting import curdoc, figure
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import numpy.ma as ma
import math
import time
import circle_fit as cf
import matplotlib.colors as mcolors
import config_constants as cc



# In[2]:


def read_circle():
    
    conversion = cc.conversion
    xcoords = []
    ycoords = []

    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    #camera.Width = 4112
    #camera.Height = 2172
    camera.CenterX.SetValue(True)
    camera.Width.SetValue(2956)
    camera.CenterY.SetValue(True)
    camera.Height.SetValue(1988)
    camera.Close()
    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()

    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


    #def for background change to black and white
    object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=70)

    #def for counter 
    t = 0
    tmax = 650
    dt = 1
    #display 
    scene1 = canvas()
    #display(fig)
    #measure the time
    st = time.time()
    #Camera grabbing while loop and set count time 
    while camera.IsGrabbing() and t < tmax:
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
        if not grabResult.GrabSucceeded: break

    #Frame color control 
        GrayFrame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        blurFrame = cv.GaussianBlur(GrayFrame, (25,25),0)
        # Set up the detector with default parameters.

        # Threshold image to binary
        thresh = cv.threshold(blurFrame, 35, 255, cv.THRESH_BINARY)[1]

        # Find contours
        contours, hierarchy = cv.findContours(blurFrame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # Iterate through contours and find largest contour
        largest_contour_area = 0
        largest_contour = None
        for contour in contours:
            area = cv.contourArea(contour)
            if area > largest_contour_area:
                largest_contour_area = area
                largest_contour = contour

        # Draw outline of largest contour on input image
        img_with_contour = cv.cvtColor(blurFrame, cv.COLOR_GRAY2BGR)
        cv.drawContours(img_with_contour, [largest_contour], 0, (0, 0, 255), 2)

        # Get coordinates of center of largest contour
        M = cv.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Draw a circle at the center of the largest contour
        cv.circle(img_with_contour, (cx, cy), 5, (255, 0, 0), -1)

        # Show the input image with contour and center
        imS = cv.resize(img_with_contour, (1478, 994)) # Resize image
        cv.imshow("Image with contour", imS)

        # Print coordinates of center of largest contour
        #print(f"({cx}, {cy})")
        xcoords.append(cx*conversion)
        ycoords.append(cy*conversion)

        key = cv.waitKey(30) 
        if key == 27 : break
        #count time 
        t = t + dt

    #camera control         
    camera.StopGrabbing()
    cv.destroyAllWindows()

    data = [[xcoords[i], ycoords[i]] for i in range(len(xcoords))]
    xc, yc, r, sigma = cf.least_squares_circle((data))
    print('Center coordinates:',xc,yc,'mm')
    print('Radius:',r,'mm')
    print('Residual error:',sigma,'mm')
    
    #cf.plot_data_circle(xd,yd,xc,yc,r)
    
    return xc, yc, r, sigma

