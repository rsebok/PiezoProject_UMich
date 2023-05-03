#The function to get the current location of the spine
#Input: file save location

#Last updated 05/03/2023 by RAS

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
#get_ipython().run_line_magic('matplotlib', 'inline')


conversion = cc.conversion

def grab_location(name):
    a=0
    b=0
    
    while True:
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

        #def for set time counter 
        t = 0
        tmax = 1
        dt = .5
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
            #blurFrame = cv.GaussianBlur(GrayFrame, (17,17),0)
            # Set up the detector with default parameters.

            # Threshold image to binary
            thresh = cv.threshold(GrayFrame, 254, 255, cv.THRESH_BINARY)[1]
            thresh2 = cv.resize(thresh, (1478, 994))
            cv.imshow("Thresh", thresh2)

            # Find contours
            contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            # Iterate through contours and find largest contour
            largest_contour_area = 0
            largest_contour = None
            for contour in contours:
                area = cv.contourArea(contour)
                if area > largest_contour_area:
                    largest_contour_area = area
                    largest_contour = contour

            # Draw outline of largest contour on input image
            img_with_contour = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
            cv.drawContours(img_with_contour, [largest_contour], 0, (0, 255, 0), 1)

            # Get coordinates of center of largest contour
            M = cv.moments(largest_contour)
            cx = (M['m10'] / M['m00'])
            cy = (M['m01'] / M['m00'])
            subpixel_contour = cv.cornerSubPix(GrayFrame, np.float32([(cx,cy)]), winSize=(1,1), zeroZone=(-1,-1), criteria=(cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.00001))
            subpixel_point = subpixel_contour[0]
            cv.circle(img_with_contour, (int(subpixel_point[0]), int(subpixel_point[1])), 2, (255,0,0), 1)
            pcx = subpixel_point[0]
            pcy = subpixel_point[1]

            # Draw a circle at the center of the largest contour
            #cv.circle(img_with_contour, (cx, cy), 5, (255, 0, 0), 1)

            # Show the input image with contour and center
            imS = cv.resize(img_with_contour, (1478, 994)) # Resize image
            cv.imshow("Image with contour", imS)

            # Print coordinates of center of largest contour
            #print(f"({cx}, {cy})")
            xcoords.append(pcx*conversion)
            ycoords.append(pcy*conversion)

            key = cv.waitKey(30) 
            if key == 27 : break
            #count time 
            t = t + dt

        #camera control         
        camera.StopGrabbing()
        cv.destroyAllWindows()

        
        a=xcoords[-1]
        b=ycoords[-1]
        
        if a and b > 1:
            break
        

    dict = {'X': [a], 'Y': [b]}
    df = pd.DataFrame(dict)
    df.to_csv('.\Results\%s.csv' % name, mode='a', index=False, header=False)

    return a,b


