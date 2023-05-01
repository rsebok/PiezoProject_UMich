#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
import random
import math
import array
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.axes
from matplotlib.offsetbox import AnchoredText
import numpy as np
import pyvisa as visa
import os
from AutoCircleCopyRS import move_circle
from move_by_XY import moveXY
from GrabLocation import grab_location
import config_constants as cc
import cv2
import sys
import usb.core
import usb.util

def auto_test(channel, symm, voltage, freq, duration, trials):
    xcoords = []
    ycoords = []
    x0coords = []
    y0coords = []
    x, y = grab_location('junk')

    for i in range(1, trials + 1):
        moveXY(cc.circle['circle_x'] - x, cc.circle['circle_y'] - y + 2)

        x0, y0 = grab_location('junk')
        x0coords.append(x0)
        y0coords.append(y0)

        rm = visa.ResourceManager()
        li = rm.list_resources()
        vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
        
        if channel == 1:
            print('X', voltage, 'Vpp', duration, 's')

            # C1 0 #neg B
            # print(vi.query("*idn?"))
            print("Configuring C1")
            vi.write("c1:bswv frq, %s" % freq)  # set the frequency of channel 1
            time.sleep(0.6)
            vi.write("c1:bswv wvtp,ramp")  # set the type of waveform
            time.sleep(0.6)
            vi.write("c1:bswv amp, %s" % voltage)  # set the amplitude
            time.sleep(0.6)
            vi.write("c1:bswv sym, %s" % symm)  # set the amplitude
            time.sleep(0.6)
            vi.write("c1:bswv duty,75")  # duty cycle
            time.sleep(0.6)
            vi.write("c1:bswv dlay, 1")  # brust delay for 1 second
            time.sleep(1)
            vi.write("c1:output on")
            time.sleep(duration)
            vi.write("c1:output off")
            time.sleep(0.6)

            print('Move done.')

            x, y = grab_location('junk')
            xcoords.append(x)
            ycoords.append(y)

            print(i)
            
        if channel == 2:
            print('Y', voltage, 'Vpp', duration, 's')

            # C1 0 #neg B
            # print(vi.query("*idn?"))
            print("Configuring C2")
            vi.write("c2:bswv frq, %s" % freq)  # set the frequency of channel 1
            time.sleep(0.6)
            vi.write("c2:bswv wvtp,ramp")  # set the type of waveform
            time.sleep(0.6)
            vi.write("c2:bswv amp, %s" % voltage)  # set the amplitude
            time.sleep(0.6)
            vi.write("c2:bswv sym, %s" % symm)  # set the amplitude
            time.sleep(0.6)
            vi.write("c2:bswv duty,75")  # duty cycle
            time.sleep(0.6)
            vi.write("c2:bswv dlay, 1")  # brust delay for 1 second
            time.sleep(1)
            vi.write("c2:output on")
            time.sleep(duration)
            vi.write("c2:output off")
            time.sleep(0.6)

            print('Move done.')

            x, y = grab_location('junk')
            xcoords.append(x)
            ycoords.append(y)

            print(i)

    print('## AutoTest complete.')  # end after all points attempted
    
    return xcoords, ycoords, x0coords, y0coords

#if __name__ == '__main__':
    #trials = int(input("Enter the number of trials: "))
    #duration = float(input("Enter the duration of each trial in seconds: "))
    #auto_test(trials, duration)


# In[ ]:




