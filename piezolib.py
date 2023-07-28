#Library for piezo functions

import time
from random import shuffle
from timer import Timer
import math
import array
import pandas as pd
import numpy as np
import pyvisa as visa
import os
import config_constants as cc
import matplotlib.pyplot as plt
import itertools
import sys
import cv2 as cv
import usb.core
import usb.util
from vpython import * 
from pypylon import pylon
import smtplib
from email.mime.text import MIMEText

def send_email():
    """

    This function sends an email to RAS.

    Args:

    None.

    Returns:

    None.

    """
    subject = "AutoTest complete!"
    body = "This is a notification that your test sequence has concluded :)"
    sender = "3214lab@gmail.com"
    password = "ebdzhrzhhpysfpjb"
    recipients = ["rsebok@umich.edu"]
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()
    
    return

def grab_location(name):
    """

    This function measures the location of the positioner.

    Args:

    name (str): Name of the csv file to save the coordinates to.

    Returns:

    a,b (float) : The coordinate pair of the spine location (mm).

    """
    conversion = cc.conversion

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

def auto_test(channel, symm, voltage, freq, duration, trials):
    """

    This function tests the distance moved based on an input wave configuration.

    Args:

    channel (int): 1 or 2, representing x or y channels.

    symm (int): Symmetry of the wave, usually 0 or 100, dictates negative or positive movement.
    
    voltage (float): Amplitude of the waveform (V), should not exceed 5V.
    
    freq (float): Frequency of the wave (Hz).
    
    duration (float): Time for waveform generator to be active, length of wave (s).
    
    trials (int): Number of times to repeat this signal.

    Returns:

    xcoords, ycoords, x0coords, y0coords: Final and initial locations of positioner (mm).

    """
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

    print('## AutoTest complete.') 
    
    return xcoords, ycoords, x0coords, y0coords

def move_circle():
    """

    This function moves the positioner along its maximum range.

    Args:

    None.

    Returns:

    None.

    """    
    rm = visa.ResourceManager()
    li = rm.list_resources()
    print(li)
    vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    t = 5 #sec
    
    print("Configuring C1")
    vi.write("c1:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c1:bswv amp, 4") #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 0") #set the symmetry
    time.sleep(0.6)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(0.6)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    
    print("Configuring C2")
    vi.write("c2:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c2:bswv amp, 4") #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 0") #set the symmetry
    time.sleep(0.6)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(0.6)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")

    print("Configuring C1")
    vi.write("c1:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c1:bswv amp, 4") #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 100") #set the symmetry
    time.sleep(0.6)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(0.6)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")

    print("Configuring C2")
    vi.write("c2:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c2:bswv amp, 4") #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 100") #set the symmetry
    time.sleep(0.6)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(0.6)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")

    print('Circle complete')
    
    return

def read_circle():
    """

    This function reads a motion of the spine and returns a circle fit. Used for running alongside move_circle().

    Args:

    None.

    Returns:

    xc, yc, r, sigma: Center, radius, and error of fitted circle (mm).

    """    
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
        blurFrame = cv.GaussianBlur(GrayFrame, (17,17),0)
        # Set up the detector with default parameters.

        # Threshold image to binary
        thresh = cv.threshold(blurFrame, 150, 255, cv.THRESH_BINARY)[1]
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
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Draw a circle at the center of the largest contour
        #cv.circle(img_with_contour, (cx, cy), 5, (255, 0, 0), 1)

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

def move_posX(x):
    """

    This function moves the positioner a given distance in the positive x direction by running a 4V, 10Hz wave for a calculated time
    based on the calibration. Designed for moves more than 250 um.

    Args:

    x (float): Distance to move in positive x direction (mm).

    Returns:

    None.

    """    
    posX_speed = cc.speeds['posX']
    voltage = cc.voltage
        
    t = abs(x/posX_speed)
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    
    print('posX,',voltage,'Vpp,',"10 Hz,",t,'s')
        
    print("Configuring C1")
    vi.write("c1:bswv frq, 10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 0") #set the symmetry
    time.sleep(0.3)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    
    print('Move done.')

def move_posY(y):
    """

    This function moves the positioner a given distance in the positive y direction by running a 4V, 10Hz wave for a calculated time
    based on the calibration. Designed for moves more than 250 um.

    Args:

    y (float): Distance to move in positive y direction (mm).

    Returns:

    None.

    """     
    posY_speed = cc.speeds['posY']
    voltage = cc.voltage

    t = abs(y/posY_speed)    
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
        
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('posY,',voltage,'Vpp,',"10 Hz,",t,'s')
    
    print("Configuring C2")
    vi.write("c2:bswv frq, 10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 100") #set the symmetry
    time.sleep(0.3)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")
    
    print('Move done.')

def move_negX(x):
    """

    This function moves the positioner a given distance in the negative x direction by running a 4V, 10Hz wave for a calculated time
    based on the calibration. Designed for moves more than 250 um.

    Args:

    x (float): Distance to move in negative x direction (mm).

    Returns:

    None.

    """     
    negX_speed = cc.speeds['negX']
    voltage = cc.voltage

    t = abs(x/negX_speed)
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
        
    
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('negX,',voltage,'Vpp,',"10 Hz,",t,'s')
 
    print("Configuring C1")
    vi.write("c1:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 100") #set the symmetry
    time.sleep(0.3)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    
    print('Move done.')
    
def move_negY(y):
    """

    This function moves the positioner a given distance in the negative y direction by running a 4V, 10Hz wave for a calculated time
    based on the calibration. Designed for moves more than 250 um.

    Args:

    y (float): Distance to move in negative y direction (mm).

    Returns:

    None.

    """     
    negY_speed = cc.speeds['negY']
    voltage = cc.voltage

    t = abs(y/negY_speed)
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
     
    
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('negY,',voltage,'Vpp,',"10 Hz,",t,'s')
 
    print("Configuring C2")
    vi.write("c2:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 0") #set the symmetry
    time.sleep(0.3)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")

    print('Move done.')
    
def movesteps_posY(voltage,steps):
    """

    This function moves the positioner a given number of steps in the positive y direction by running 10Hz wave for a 
    calculated time (s) [= steps/ 10Hz]. Designed for moves more than 250 um.

    Args:

    voltage (float): Amplitude of waveform (V), must not be greater than 5V.
    
    steps (int): Steps to take in positive y direction.

    Returns:

    None.

    """ 
    if voltage >=5:
        print('That voltage is too high!')
        return
    
    t = steps/10
    
    print('posY',voltage,'Vpp',steps,'steps')
    rm = visa.ResourceManager()
    li = rm.list_resources()
    print(li)
    vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    vi.timeout = 5000
        
    print("Configuring C1")
    vi.write("c1:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 0") #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(0.6)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    time.sleep(2)
    
    print('Done.')

def movesteps_posX(voltage,steps):
    """

    This function moves the positioner a given number of steps in the positive x direction by running 10Hz wave for a 
    calculated time (s) [= steps/ 10Hz]. Designed for moves more than 250 um.

    Args:

    voltage (float): Amplitude of waveform (V), must not be greater than 5V.
    
    steps (int): Steps to take in positive x direction.

    Returns:

    None.

    """
    if voltage >=5:
        print('That voltage is too high!')
        return
       
    t = steps/10
        
    print('posX',voltage,'Vpp',steps,'steps')
    rm = visa.ResourceManager()
    li = rm.list_resources()
    print(li)
    vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')

    print("Configuring C2")
    vi.write("c2:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 0") #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(0.6)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")
    time.sleep(2)
    
    print('Done.')

def movesteps_negY(voltage,steps):
    """

    This function moves the positioner a given number of steps in the negative y direction by running 10Hz wave for a 
    calculated time (s) [= steps/ 10Hz]. Designed for moves more than 250 um.

    Args:

    voltage (float): Amplitude of waveform (V), must not be greater than 5V.
    
    steps (int): Steps to take in negative y direction.

    Returns:

    None.

    """
    if voltage >=5:
        print('That voltage is too high!')
        return
    
    t = steps/10
    
    print('negY',voltage,'Vpp',steps,'steps')
    rm = visa.ResourceManager()
    li = rm.list_resources()
    print(li)
    vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
 
    print("Configuring C1")
    vi.write("c1:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 100") #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(0.6)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    time.sleep(2)
    
    print('Done.')
    
def movesteps_negX(voltage,steps):
    """

    This function moves the positioner a given number of steps in the negative x direction by running 10Hz wave for a 
    calculated time (s) [= steps/ 10Hz]. Designed for moves more than 250 um.

    Args:

    voltage (float): Amplitude of waveform (V), must not be greater than 5V.
    
    steps (int): Steps to take in negative x direction.

    Returns:

    None.

    """
    if voltage >=5:
        print('That voltage is too high!')
        return
    
    t = steps/10
    
    print('negX',voltage,'Vpp',steps,'steps')
    rm = visa.ResourceManager()
    li = rm.list_resources()
    print(li)
    vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')

    print("Configuring C2")
    vi.write("c2:bswv frq,10") #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.6)
    vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 100") #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.6)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(0.6)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")
    time.sleep(2)

    print('Done.')
    
def tinymove_posX(x):
    """

    This function moves the positioner a given distance in the positive x direction by running a 5Hz wave for 0.5s
    at a voltage calibrated by the config file. Designed for moves less than 250 um and greater than 50 um.

    Args:

    x (float): Distance to move in positive x (mm).

    Returns:

    None.

    """
    #Use this section to move in pos x
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    voltage = abs((abs(x) + cc.tiny_intercept_posX)/cc.tiny_slope_posX)
    newt = cc.tiny_time
    freq = cc.tiny_freq

    if voltage > 4:
        print("Dangerous voltage! CANCELED.")
        return

    print('posX,',voltage,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C1")
    vi.write("c1:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 0") #set the symmetry
    time.sleep(0.3)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(newt)
    vi.write("c1:output off")

    print('Tiny move done.')
    
def tinymove_negX(x):
    """

    This function moves the positioner a given distance in the negative x direction by running a 5Hz wave for 0.5s
    at a voltage calibrated by the config file. Designed for moves less than 250 um and greater than 50 um.

    Args:

    x (float): Distance to move in negative x (mm).

    Returns:

    None.

    """    
    #Use this section to move in neg x
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    voltage = abs((abs(x) + cc.tiny_intercept_negX)/cc.tiny_slope_negX)
    newt = cc.tiny_time
    freq = cc.tiny_freq

    if voltage > 4:
        print("Dangerous voltage! CANCELED.")
        return

    print('negX,',voltage,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C1")
    vi.write("c1:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 100") #set the symmetry
    time.sleep(0.3)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(newt)
    vi.write("c1:output off")

    print('Tiny move done.')

def tinymove_negY(y):
    """

    This function moves the positioner a given distance in the negative y direction by running a 5Hz wave for 0.5s
    at a voltage calibrated by the config file. Designed for moves less than 250 um and greater than 50 um.

    Args:

    y (float): Distance to move in negative y (mm).

    Returns:

    None.

    """
    #Use this section to move in pos y
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    voltage = abs((abs(y) + cc.tiny_intercept_negY)/cc.tiny_slope_negY)
    newt = cc.tiny_time
    freq = cc.tiny_freq

    if voltage > 4:
        print("Dangerous voltage! CANCELED.")
        return

    print('negY,',voltage,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C2")
    vi.write("c2:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 0") #set the symmetry
    time.sleep(0.3)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(newt)
    vi.write("c2:output off")

    print('Tiny move done.')

def tinymove_posY(y):
    """

    This function moves the positioner a given distance in the positive y direction by running a 5Hz wave for 0.5s
    at a voltage calibrated by the config file. Designed for moves less than 250 um and greater than 50 um.

    Args:

    y (float): Distance to move in positive y (mm).

    Returns:

    None.

    """
    #Use this section to move in neg y
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    voltage = abs((abs(y) + cc.tiny_intercept_posY)/cc.tiny_slope_posY)
    newt = cc.tiny_time
    freq = cc.tiny_freq

    if voltage > 4:
        print("Dangerous voltage! CANCELED.")
        return

    print('posY,',voltage,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C2")
    vi.write("c2:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 100") #set the symmetry
    time.sleep(0.3)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(newt)
    vi.write("c2:output off")

    print('Tiny move done.')

def micromove_posX(x):
    """

    This function moves the positioner a given distance in the positive x direction by running a 5Hz wave for 0.25s
    at a voltage calibrated by the config file. Designed for moves less than 50 um.

    Args:

    x (float): Distance to move in positive x (mm).

    Returns:

    None.

    """
    newt = cc.micro_time
    freq = cc.micro_freq

    #Use this section to move in pos x
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    voltage_posX = abs((abs(x) + cc.micro_intercept_posX)/cc.micro_slope_posX)
    
    if voltage_posX >4:
        print("Dangerous voltage! CANCELED.")
        return

    print('posX,',voltage_posX,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C1")
    vi.write("c1:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c1:bswv amp, %s" %voltage_posX) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 0") #set the symmetry
    time.sleep(0.3)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(newt)
    vi.write("c1:output off")

    print('Micro move done.')
    
def micromove_negX(x):
    """

    This function moves the positioner a given distance in the negative x direction by running a 5Hz wave for 0.25s
    at a voltage calibrated by the config file. Designed for moves less than 50 um.

    Args:

    x (float): Distance to move in negative x (mm).

    Returns:

    None.

    """
    newt = cc.micro_time
    freq = cc.micro_freq
    
    #Use this section to move in neg x
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')

    voltage_negX = abs((abs(x) + cc.micro_intercept_negX)/cc.micro_slope_negX)
    
    if voltage_negX >4:
        print("Dangerous voltage! CANCELED.")
        return
    
    print('negX,',voltage_negX,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C1")
    vi.write("c1:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c1:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c1:bswv amp, %s" %voltage_negX) #set the amplitude
    time.sleep(0.6)
    vi.write("c1:bswv sym, 100") #set the symmetry
    time.sleep(0.3)
    vi.write("c1:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c1:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(newt)
    vi.write("c1:output off")

    print('Micro move done.')

def micromove_negY(y):
    """

    This function moves the positioner a given distance in the negative y direction by running a 5Hz wave for 0.25s
    at a voltage calibrated by the config file. Designed for moves less than 50 um.

    Args:

    y (float): Distance to move in negative y (mm).

    Returns:

    None.

    """
    newt = cc.micro_time
    freq = cc.micro_freq
    
    #Use this section to move in neg y
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
        
    voltage_negY = abs((abs(y) + cc.micro_intercept_negY)/cc.micro_slope_negY)
    
    if voltage_negY >4:
        print("Dangerous voltage! CANCELED.")
        return

    print('negY,',voltage_negY,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C2")
    vi.write("c2:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c2:bswv amp, %s" %voltage_negY) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 0") #set the symmetry
    time.sleep(0.3)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(newt)
    vi.write("c2:output off")

    print('Micro move done.')

def micromove_posY(y):
    """

    This function moves the positioner a given distance in the positive y direction by running a 5Hz wave for 0.25s
    at a voltage calibrated by the config file. Designed for moves less than 50 um.

    Args:

    y (float): Distance to move in positive y (mm).

    Returns:

    None.

    """
    newt = cc.micro_time
    freq = cc.micro_freq
    
    #Use this section to move in pos y
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
        
    voltage_posY = abs((abs(y) + cc.micro_intercept_posY)/cc.micro_slope_posY)
    
    if voltage_posY >4:
        print("Dangerous voltage! CANCELED.")
        return

    print('posY,',voltage_posY,'Vpp,',freq,"Hz,",newt,'s')

    print("Configuring C2")
    vi.write("c2:bswv frq, %s" %freq) #set the frequency of channel 1
    time.sleep(0.6)
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    time.sleep(0.3)
    vi.write("c2:bswv amp, %s" %voltage_posY) #set the amplitude
    time.sleep(0.6)
    vi.write("c2:bswv sym, 100") #set the symmetry
    time.sleep(0.3)
    vi.write("c2:bswv duty,75") #duty cycle
    time.sleep(0.3)
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(newt)
    vi.write("c2:output off")

    print('Micro move done.')
        
def moveXY(x,y):
    """

    This function moves the positioner a given distance in x and y (mm). It will choose the correct move style based on
    the distance to be moved. These distance limits are defined in the config file.

    Args:

    x,y (float,float): Distance to move in x (mm) and y (mm).

    Returns:

    None.

    """    
    print("## Attempting to move by:",x,y)
     
            
    #Use this section to move in pos x
    if x > 0:
        if abs(x) <= cc.min_move:
            print("## Requested move is too small.")
            return
        elif abs(x) <= cc.micro_max:
            micromove_posX(x)
        elif abs(x) <= cc.tiny_max:
            tinymove_posX(x)
        else:
            move_posX(x)

    #Use this section to move in neg x
    if x < 0:
        if abs(x) <= cc.min_move:
            print("## Requested move is too small.")
            return
        elif abs(x) <= cc.micro_max:
            micromove_negX(x)
        elif abs(x) <= cc.tiny_max:
            tinymove_negX(x)
        else:
            move_negX(x)
       
    
    if y > 0:
        if abs(y) <= cc.min_move:
            print("## Requested move is too small.")
            return
        elif abs(y) <= cc.micro_max:
            micromove_posY(y)
        elif abs(y) <= cc.tiny_max:
            tinymove_posY(y)
        else:
            move_posY(y)

    #Use this section to move in neg y
    if y < 0:
        if abs(y) <= cc.min_move:
            print("## Requested move is too small.")
            return
        elif abs(y) <= cc.micro_max:
            micromove_negY(y)
        elif abs(y) <= cc.tiny_max:
            tinymove_negY(y)
        else:
            move_negY(y)
            
def micro_calib(trials):
    """

    This function returns the calibration for the micro (and tiny) moves.

    Args:

    trials (int): Number of times to repeat the calibration movements.

    Returns:

    None.

    """    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    circle_x = cc.circle['circle_x'] 
    circle_y = cc.circle['circle_y']    
    circle_r = cc.circle['circle_r']

    #enter a name for this test, the timestamp will be added and it will become the CSV name
    name = 'LongTermTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time #name of the CSV file will be the name that you chose plus the date and time
    print(name)

    x,y = grab_location('junk')
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center

    x,y = grab_location(name)

    #loop through the test for n trials
    n = 1
    while n <= trials: #number of trials
        print('trial #',n)

        if n >1:
            x,y = grab_location(name)
        #negx
        print("Configuring C1")
        vi.write("c1:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c1:bswv amp, %s" %1) #set the amplitude
        time.sleep(0.6)
        vi.write("c1:bswv sym, 100") #set the symmetry
        time.sleep(0.3)
        vi.write("c1:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c1:output on")
        time.sleep(0.25)
        vi.write("c1:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #posx
        print("Configuring C1")
        vi.write("c1:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c1:bswv amp, %s" %1) #set the amplitude
        time.sleep(0.6)
        vi.write("c1:bswv sym, 0") #set the symmetry
        time.sleep(0.3)
        vi.write("c1:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c1:output on")
        time.sleep(0.25)
        vi.write("c1:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #negy
        print("Configuring C2")
        vi.write("c2:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c2:bswv amp, %s" %1) #set the amplitude
        time.sleep(0.6)
        vi.write("c2:bswv sym, 0") #set the symmetry
        time.sleep(0.3)
        vi.write("c2:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c2:output on")
        time.sleep(0.25)
        vi.write("c2:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #posy
        print("Configuring C2")
        vi.write("c2:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c2:bswv amp, %s" %1) #set the amplitude
        time.sleep(0.6)
        vi.write("c2:bswv sym, 100") #set the symmetry
        time.sleep(0.3)
        vi.write("c2:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c2:output on")
        time.sleep(0.25)
        vi.write("c2:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        time.sleep(300)

        #negx
        print("Configuring C1")
        vi.write("c1:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c1:bswv amp, %s" %1.5) #set the amplitude
        time.sleep(0.6)
        vi.write("c1:bswv sym, 100") #set the symmetry
        time.sleep(0.3)
        vi.write("c1:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c1:output on")
        time.sleep(0.25)
        vi.write("c1:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #posx
        print("Configuring C1")
        vi.write("c1:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c1:bswv amp, %s" %1.5) #set the amplitude
        time.sleep(0.6)
        vi.write("c1:bswv sym, 0") #set the symmetry
        time.sleep(0.3)
        vi.write("c1:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c1:output on")
        time.sleep(0.25)
        vi.write("c1:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #negy
        print("Configuring C2")
        vi.write("c2:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c2:bswv amp, %s" %1.5) #set the amplitude
        time.sleep(0.6)
        vi.write("c2:bswv sym, 0") #set the symmetry
        time.sleep(0.3)
        vi.write("c2:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c2:output on")
        time.sleep(0.25)
        vi.write("c2:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #posy
        print("Configuring C2")
        vi.write("c2:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c2:bswv amp, %s" %1.5) #set the amplitude
        time.sleep(0.6)
        vi.write("c2:bswv sym, 100") #set the symmetry
        time.sleep(0.3)
        vi.write("c2:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c2:output on")
        time.sleep(0.25)
        vi.write("c2:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        time.sleep(300)

        #negx
        print("Configuring C1")
        vi.write("c1:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c1:bswv amp, %s" %2) #set the amplitude
        time.sleep(0.6)
        vi.write("c1:bswv sym, 100") #set the symmetry
        time.sleep(0.3)
        vi.write("c1:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c1:output on")
        time.sleep(0.25)
        vi.write("c1:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #posx
        print("Configuring C1")
        vi.write("c1:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c1:bswv amp, %s" %2) #set the amplitude
        time.sleep(0.6)
        vi.write("c1:bswv sym, 0") #set the symmetry
        time.sleep(0.3)
        vi.write("c1:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c1:output on")
        time.sleep(0.25)
        vi.write("c1:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #negy
        print("Configuring C2")
        vi.write("c2:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c2:bswv amp, %s" %2) #set the amplitude
        time.sleep(0.6)
        vi.write("c2:bswv sym, 0") #set the symmetry
        time.sleep(0.3)
        vi.write("c2:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c2:output on")
        time.sleep(0.25)
        vi.write("c2:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)
        time.sleep(0.3)
        x,y = grab_location(name)

        #posy
        print("Configuring C2")
        vi.write("c2:bswv frq, 5" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.3)
        vi.write("c2:bswv amp, %s" %2) #set the amplitude
        time.sleep(0.6)
        vi.write("c2:bswv sym, 100") #set the symmetry
        time.sleep(0.3)
        vi.write("c2:bswv duty,75") #duty cycle
        time.sleep(0.3)
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c2:output on")
        time.sleep(0.25)
        vi.write("c2:output off")
        time.sleep(0.3)

        print('Move done.') 

        x,y = grab_location(name)

        moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
        
        time.sleep(300)

        n += 1 

    x,y = grab_location('junk')
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center

    print('AutoTest complete.')

    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file

    start = data.iloc[0::2, :]
    end = data.iloc[1::2, :]

    endx = end['X (mm)'].tolist()
    endy = end['Y (mm)'].tolist()
    startx = start['X (mm)'].tolist()
    starty = start['Y (mm)'].tolist()

    xdiffs = np.subtract(endx, startx)
    xdiffs = list(xdiffs)

    ydiffs = np.subtract(endy, starty)
    ydiffs = list(ydiffs)

    negxdiffs1 = xdiffs[0::12]
    posxdiffs1 = xdiffs[1::12]
    negydiffs1 = ydiffs[2::12]
    posydiffs1 = ydiffs[3::12]
    negxdiffs15 = xdiffs[4::12]
    posxdiffs15 = xdiffs[5::12]
    negydiffs15 = ydiffs[6::12]
    posydiffs15 = ydiffs[7::12]
    negxdiffs2 = xdiffs[8::12]
    posxdiffs2 = xdiffs[9::12]
    negydiffs2 = ydiffs[10::12]
    posydiffs2 = ydiffs[11::12]

    print("Your micro moves should be defined by:")

    x = [1,1.5,2]
    y = [np.average(posxdiffs1),np.average(posxdiffs15),np.average(posxdiffs2)]

    m,b = np.polyfit(x, y, 1)
    print('Pos X slope:',m)
    print('Pos X intercept:',b)

    y = [np.average(negxdiffs1),np.average(negxdiffs15),np.average(negxdiffs2)]

    m,b = np.polyfit(x, y, 1)
    print('Neg X slope:',m)
    print('Neg X intercept:',b)

    y = [np.average(posydiffs1),np.average(posydiffs15),np.average(posydiffs2)]

    m,b = np.polyfit(x, y, 1)
    print('Pos Y slope:',m)
    print('Pos Y intercept:',b)

    y = [np.average(negydiffs1),np.average(negydiffs15),np.average(negydiffs2)]

    m,b = np.polyfit(x, y, 1)
    print('Neg Y slope:',m)
    print('Neg Y intercept:',b)

    print('Your results are saved as:',name)
    
def vel_negX(voltage,runtime,trials):
    """

    This function calculates the distance moved (mm) per second of an applied wave in the negative x direction. Used to 
    calibrate large moves in config file.

    Args:

    voltage (float): Amplitude of waveform (V). Shall not exceed 5V.
    
    runtime (float): Time to apply wave (s). Shall not exceed 5s.
    
    trials (int): Number of times to apply waveform. Shall not exceed 200.

    Returns:

    None.

    """
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    circle_x = cc.circle['circle_x'] 
    circle_y = cc.circle['circle_y']    
    circle_r = cc.circle['circle_r']
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    if runtime >=5:
        print('That time is too high!')
        return
    if trials >200:
        print('That is too many trials!')
        return

    #enter a name for this test, the timestamp will be added and it will become the CSV name
    name = 'AutoVelocityTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time #name of the CSV file will be the name that you chose plus the date and time
    print(name)

    x,y = grab_location('junk')
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
    
    x,y = grab_location(name)
    
    #loop through the test for n trials
    n = 1 
    while n <= trials: #number of trials
        print('trial #',n)
        
        if n >1:
            x,y = grab_location(name)

        print('negX,',voltage,'Vpp,',"10 Hz,",runtime,'s')

        print("Configuring C1")
        vi.write("c1:bswv frq, 10" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.6)
        vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
        time.sleep(0.6)
        vi.write("c1:bswv sym, 100") #set the symmetry
        time.sleep(0.6)
        vi.write("c1:bswv duty,75") #duty cycle
        time.sleep(0.6)
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c1:output on")
        time.sleep(runtime)
        vi.write("c1:output off")
        time.sleep(0.6)

        print('Move done.') 

        x,y = grab_location(name)
        moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
        
        n += 1 
    else:
        print('AutoTest complete.')
        
    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file
    start = data.iloc[0::2, :]
    end = data.iloc[1::2, :]
    
    endx = end['X (mm)'].tolist()
    endy = end['Y (mm)'].tolist()
    startx = start['X (mm)'].tolist()
    starty = start['Y (mm)'].tolist()

    xdiffs = np.subtract(endx, startx)
    xdiffs = list(xdiffs)
    xdiffs = [ele for ele in xdiffs if abs(ele) < 2]

    ydiffs = np.subtract(endy, starty)
    ydiffs = list(ydiffs)
    ydiffs = [ele for ele in ydiffs if abs(ele) < 2]

    print(xdiffs,ydiffs)

    def Average(lst):
        return sum(lst) / len(lst)

    print('Average x velocity:',Average(xdiffs)/runtime)
    print('Average y velocity:',Average(ydiffs)/runtime)
    
    print('Your results are saved as:',name)

def vel_negY(voltage,runtime,trials):
    """

    This function calculates the distance moved (mm) per second of an applied wave in the negative y direction. Used to 
    calibrate large moves in config file.

    Args:

    voltage (float): Amplitude of waveform (V). Shall not exceed 5V.
    
    runtime (float): Time to apply wave (s). Shall not exceed 5s.
    
    trials (int): Number of times to apply waveform. Shall not exceed 200.

    Returns:

    None.

    """
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    circle_x = cc.circle['circle_x'] 
    circle_y = cc.circle['circle_y']    
    circle_r = cc.circle['circle_r']
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    if runtime >=5:
        print('That time is too high!')
        return
    if trials >200:
        print('That is too many trials!')
        return

    #enter a name for this test, the timestamp will be added and it will become the CSV name
    name = 'AutoVelocityTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time #name of the CSV file will be the name that you chose plus the date and time
    print(name)
    
    x,y = grab_location('junk')
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
    
    x,y = grab_location(name)
    
    #loop through the test for n trials
    n = 1 
    while n <= trials: #number of trials
        print('trial #',n)
        
        if n >1:
            x,y = grab_location(name)
            
        print('negY,',voltage,'Vpp,',"10 Hz,",runtime,'s')

        print("Configuring C2")
        vi.write("c2:bswv frq, 10") #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.6)
        vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
        time.sleep(0.6)
        vi.write("c2:bswv sym, 0") #set the symmetry
        time.sleep(0.6)
        vi.write("c2:bswv duty,75") #duty cycle
        time.sleep(0.6)
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c2:output on")
        time.sleep(runtime)
        vi.write("c2:output off")
        time.sleep(0.6) #select the movement direction to test
        #time.sleep(2)
        
        x,y = grab_location(name)
        moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
        
        n += 1 
    else:
        print('AutoTest complete.')
        
    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file
    start = data.iloc[0::2, :]
    end = data.iloc[1::2, :]
    
    endx = end['X (mm)'].tolist()
    endy = end['Y (mm)'].tolist()
    startx = start['X (mm)'].tolist()
    starty = start['Y (mm)'].tolist()

    xdiffs = np.subtract(endx, startx)
    xdiffs = list(xdiffs)
    xdiffs = [ele for ele in xdiffs if abs(ele) < 2]

    ydiffs = np.subtract(endy, starty)
    ydiffs = list(ydiffs)
    ydiffs = [ele for ele in ydiffs if abs(ele) < 2]

    print(xdiffs,ydiffs)

    def Average(lst):
        return sum(lst) / len(lst)

    print('Average x velocity:',Average(xdiffs)/runtime)
    print('Average y velocity:',Average(ydiffs)/runtime)
    
    print('Your results are saved as:',name)

def vel_posY(voltage,runtime,trials):
    """

    This function calculates the distance moved (mm) per second of an applied wave in the positive y direction. Used to 
    calibrate large moves in config file.

    Args:

    voltage (float): Amplitude of waveform (V). Shall not exceed 5V.
    
    runtime (float): Time to apply wave (s). Shall not exceed 5s.
    
    trials (int): Number of times to apply waveform. Shall not exceed 200.

    Returns:

    None.

    """
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    circle_x = cc.circle['circle_x'] 
    circle_y = cc.circle['circle_y']    
    circle_r = cc.circle['circle_r']
   
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    if runtime >=5:
        print('That time is too high!')
        return
    if trials >200:
        print('That is too many trials!')
        return

    #enter a name for this test, the timestamp will be added and it will become the CSV name
    name = 'AutoVelocityTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time #name of the CSV file will be the name that you chose plus the date and time
    print(name)
    
    x,y = grab_location('junk')
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
    
    x,y = grab_location(name)
    
    #loop through the test for n trials
    n = 1 
    while n <= trials: #number of trials
        print('trial #',n)
        
        if n >1:
            x,y = grab_location(name)

        print('posY,',voltage,'Vpp,',"10 Hz,",runtime,'s')

        print("Configuring C2")
        vi.write("c2:bswv frq, 10") #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.6)
        vi.write("c2:bswv amp, %s" %voltage) #set the amplitude
        time.sleep(0.6)
        vi.write("c2:bswv sym, 100") #set the symmetry
        time.sleep(0.6)
        vi.write("c2:bswv duty,75") #duty cycle
        time.sleep(0.6)
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c2:output on")
        time.sleep(runtime)
        vi.write("c2:output off")
        time.sleep(0.6) #select the movement direction to test

        x,y = grab_location(name)
        moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
        
        n += 1 
    else:
        print('AutoTest complete.')
        
    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file
    start = data.iloc[0::2, :]
    end = data.iloc[1::2, :]
    
    endx = end['X (mm)'].tolist()
    endy = end['Y (mm)'].tolist()
    startx = start['X (mm)'].tolist()
    starty = start['Y (mm)'].tolist()

    xdiffs = np.subtract(endx, startx)
    xdiffs = list(xdiffs)
    xdiffs = [ele for ele in xdiffs if abs(ele) < 2]

    ydiffs = np.subtract(endy, starty)
    ydiffs = list(ydiffs)
    ydiffs = [ele for ele in ydiffs if abs(ele) < 2]

    print(xdiffs,ydiffs)

    def Average(lst):
        return sum(lst) / len(lst)

    print('Average x velocity:',Average(xdiffs)/runtime)
    print('Average y velocity:',Average(ydiffs)/runtime)
    
    print('Your results are saved as:',name)
    
def vel_posX(voltage,runtime,trials):
    """

    This function calculates the distance moved (mm) per second of an applied wave in the positive x direction. Used to 
    calibrate large moves in config file.

    Args:

    voltage (float): Amplitude of waveform (V). Shall not exceed 5V.
    
    runtime (float): Time to apply wave (s). Shall not exceed 5s.
    
    trials (int): Number of times to apply waveform. Shall not exceed 200.

    Returns:

    None.

    """
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    circle_x = cc.circle['circle_x'] 
    circle_y = cc.circle['circle_y']    
    circle_r = cc.circle['circle_r']
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    if runtime >=5:
        print('That time is too high!')
        return
    if trials >200:
        print('That is too many trials!')
        return

    #enter a name for this test, the timestamp will be added and it will become the CSV name
    name = 'AutoVelocityTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time #name of the CSV file will be the name that you chose plus the date and time
    print(name)
    
    x,y = grab_location('junk')
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
    
    x,y = grab_location(name)
    
    #loop through the test for n trials
    n = 1 
    while n <= trials: #number of trials
        print('trial #',n)
        
        if n >1:
            x,y = grab_location(name)

        print('posX,',voltage,'Vpp,',"10 Hz,",runtime,'s')

        print("Configuring C1")
        vi.write("c1:bswv frq, 10" ) #set the frequency of channel 1
        time.sleep(0.6)
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        time.sleep(0.6)
        vi.write("c1:bswv amp, %s" %voltage) #set the amplitude
        time.sleep(0.6)
        vi.write("c1:bswv sym, 0") #set the symmetry
        time.sleep(0.6)
        vi.write("c1:bswv duty,75") #duty cycle
        time.sleep(0.6)
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        time.sleep(1)
        vi.write("c1:output on")
        time.sleep(runtime)
        vi.write("c1:output off")
        time.sleep(0.6)

        print('Move done.') 
        
        x,y = grab_location(name)
        moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
        
        n += 1 
    else:
        print('AutoTest complete.')
        
    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file
    start = data.iloc[0::2, :]
    end = data.iloc[1::2, :]
    
    endx = end['X (mm)'].tolist()
    endy = end['Y (mm)'].tolist()
    startx = start['X (mm)'].tolist()
    starty = start['Y (mm)'].tolist()

    xdiffs = np.subtract(endx, startx)
    xdiffs = list(xdiffs)
    xdiffs = [ele for ele in xdiffs if abs(ele) < 2]

    ydiffs = np.subtract(endy, starty)
    ydiffs = list(ydiffs)
    ydiffs = [ele for ele in ydiffs if abs(ele) < 2]

    print(xdiffs,ydiffs)

    def Average(lst):
        return sum(lst) / len(lst)

    print('Average x velocity:',Average(xdiffs)/runtime)
    print('Average y velocity:',Average(ydiffs)/runtime)
    
    print('Your results are saved as:',name)
    
def AutoXYTest(points):
    """

    This function tests the positioning of the spine for an input number of random points.

    Args:

    points (int): Number of random points to attempt.

    Returns:

    None.

    """
    name = 'AutoXYTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time
    print(name)
    x = 0
    y = 0

    #generate random movetable
    i = 1
    randxs = []
    randys = []

    while i <= int(points):
        circle_x = cc.circle['circle_x'] 
        circle_y = cc.circle['circle_y']    
        circle_r = cc.circle['circle_r']
        alpha = 2 * math.pi * random.random() #random angle
        r = circle_r * math.sqrt(random.random()) #random radius
        randx = r * math.cos(alpha) + circle_x #calculating coordinates
        randy = r * math.sin(alpha) + circle_y
        #print("Random point", (randx, randy))
        randxs.append(randx)
        #print('Random x:',randxs)
        randys.append(randy)
        #print('Random y:',randys)

        i += 1
    else:
        print('Random x:',randxs)
        print('Random y:',randys)

    #or create your movetable
    goalx = [6.5,5.5,4.5,5.5]
    goaly = [6.5,7.5,6.5,5.5]

    x,y = grab_location('junk')
    moveXY(0,circle_y-y) #send the piezo back to the center
    x,y = grab_location('junk')
    moveXY(circle_x-x,0) #send the piezo back to the center

    #loop through the test for n trials
    n = 1 
    while n <= int(points):
        print('point #',n)
        
        x,y = grab_location(name) #add new location to CSV
        #time.sleep(1)

        desx = float(randxs[n-1]) #use for random moves
        desy = float(randys[n-1])

        #desx = str(goalx[n-1]) #use for your choice moves
        #desy = str(goaly[n-1])
        
        dict = {'X (mm)': [desx], 'Y (mm)': [desy]}
        df = pd.DataFrame(dict)
        df.to_csv('.\Results\%s.csv' % name, mode='a', index=False, header=False)

        dy = float(desy) - y
        moveXY(0,dy)
        x,y = grab_location('junk')
        dx = float(desx) - x
        moveXY(dx,0)
        #time.sleep(1)
        x,y = grab_location(name)
        n += 1
    else:
        print('AutoTest complete.')
        print('Your results are saved as:',name)

def AutoXYTestWinCond(points,attempts,error):
    """

    This function tests the positioning of the spine for an input number of random points. This version allows for multiple
    attempts of the same point up until the attempt limit is reached or the desired accuracy (mm) is satisfied.

    Args:

    points (int): Number of random points to attempt.
    
    attempts (int): Number of allowed iterations of movement code.
    
    error (float): Acceptable error aka win condition (mm).
    
    Returns:

    name (str): Name of folder with saved results.

    """    
    print('## Starting an XY test for',points,'points with a win condition of',error,'mm and a max attempt limit of',attempts)
    timer = Timer()
    timer.start()
    
    name = '\AutoXYTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time
    print(name)
    folder = '.\Results'
    os.mkdir(folder+name)
    destlist = name+'\DestList'
    moveslist = name+'\MovesList'
    winlist = name+'\WinList'
    losslist = name+'\LossList'
    finalslist = name+'\FinalsList'
    errorlist = name+'\ErrorList'
    attemptlist = name+'\AttemptList'
    x = 0
    y = 0

    #generate random movetable
    i = 1
    randxs = []
    randys = []

    while i <= int(points):
        circle_x = cc.circle['circle_x'] 
        circle_y = cc.circle['circle_y']    
        circle_r = cc.circle['circle_r']
        alpha = 2 * math.pi * random.random() #random angle
        r = circle_r * math.sqrt(random.random()) #random radius
        randx = r * math.cos(alpha) + circle_x #calculating coordinates
        randy = r * math.sin(alpha) + circle_y
        #print("Random point", (randx, randy))
        randxs.append(randx)
        #print('Random x:',randxs)
        randys.append(randy)
        #print('Random y:',randys)

        i += 1
    else:
        print('Random x:',randxs)
        print('Random y:',randys)
        
    for i in range(0,len(randxs)):    
        dict = {'X (mm)': [randxs[i]], 'Y (mm)': [randys[i]]} #add the destination points to the CSV
        df = pd.DataFrame(dict)
        df.to_csv('.\Results\%s.csv' % destlist, mode='a', index=False, header=False)

    n = 1 #start at trial 1
    i = 1 #start at point 1
    w = 0 #start at zero wins
    tries = []
    x,y = grab_location('junk')
    #center_piezo()
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
    x,y = grab_location(moveslist)

    while i <= int(points):
        print('##',name,'Point',i,'Attempt',n)
        
        dy = randys[i-1] - y
        moveXY(0,dy)
        x,y = grab_location(moveslist) #grab 'final' locaion
        print('## Error:', np.sqrt((float(randxs[i-1])-float(x))**2 + (float(randys[i-1])-float(y))**2),'mm')
        
        if np.sqrt((float(randxs[i-1])-float(x))**2 + (float(randys[i-1])-float(y))**2) > error: #check if destination reached
            
            dx = randxs[i-1] - x
            moveXY(dx,0)
         
            x,y = grab_location(moveslist) #grab 'final' locaion
        
        
        if np.sqrt((float(randxs[i-1])-float(x))**2 + (float(randys[i-1])-float(y))**2) <= error: #check if destination reached
            tries.append(n)
            print('## The error after this trial was:', np.sqrt((float(randxs[i-1])-float(x))**2 + (float(randys[i-1])-float(y))**2),'mm')

            dict = {'X (mm)': [x], 'Y (mm)': [y]} #add win point
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % winlist, mode='a', index=False, header=False)
            df.to_csv('.\Results\%s.csv' % finalslist, mode='a', index=False, header=False)
            
            dict = {'Error (mm)': [np.sqrt((float(randxs[i-1])-float(x))**2 + (float(randys[i-1])-float(y))**2)]} #add final error
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % errorlist, mode='a', index=False, header=False)
            
            i += 1 #go to next point
            n = 1 #reset trial counter
            w += 1
            
            print("## Win condition met. That makes",w,"wins.")
            
        else:   
            print('## The error after this trial was:', np.sqrt((float(randxs[i-1])-float(x))**2 + (float(randys[i-1])-float(y))**2),'mm')
            print('## Trying this point again...') #else attempt point again
            n += 1 #increase trial count

        if n > int(attempts):
            print('## Attempt limit reached. Moving on to the next point...') #unless trial limit reached

            dict = {'X (mm)': [x], 'Y (mm)': [y]} #add loss point
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % losslist, mode='a', index=False, header=False)
            df.to_csv('.\Results\%s.csv' % finalslist, mode='a', index=False, header=False)
            
            dict = {'Error (mm)': [np.sqrt((float(randxs[i-1])-float(x))**2 + (float(randys[i-1])-float(y))**2)]} #add final error
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % errorlist, mode='a', index=False, header=False)
            
            n = 1 #reset trial count
            i += 1 #go to next point

    else:
        print('## AutoTest complete.') #end after all points attempted
        
        for i in range(0,len(tries)):
            dict = {'Attempts': [tries[i]]} #add the try counts to the CSV
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % attemptlist, mode='a', index=False, header=False)
        
        timer.stop()

    def Average(lst):
        return sum(lst) / len(lst)

    print('## Final win count:',w,'/',len(randxs),"with an error of:",error,"mm.")
    try:
        print('## The maximum tries for a single win was',max(tries),'and the minimum was',min(tries),'.')
        print('## The average number of tries per win was',Average(tries),'.')
    except:
        pass
    print('## Your results are saved as:',name)

    return name

def AutoXYTestGRID(attempts,error):
    """

    This function tests the positioning of the spine for an input number of grid points. This version allows for multiple
    attempts of the same point up until the attempt limit is reached or the desired accuracy (mm) is satisfied.

    Args:
    
    attempts (int): Number of allowed iterations of movement code.
    
    error (float): Acceptable error aka win condition (mm).
    
    Returns:

    name (str): Name of folder with saved results.

    """     
    grid_size = 16
    
    print('## Starting an XY test for a',grid_size,'point grid with a win condition of',error,'mm and a max attempt limit of',attempts)
            
    timer = Timer()
    timer.start()
    
    name = '\AutoXYTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time
    print(name)
    folder = '.\Results'
    os.mkdir(folder+name)
    destlist = name+'\DestList'
    moveslist = name+'\MovesList'
    winlist = name+'\WinList'
    losslist = name+'\LossList'
    finalslist = name+'\FinalsList'
    errorlist = name+'\ErrorList'
    attemptlist = name+'\AttemptList'
    driftlist = name+'\DriftList'
    x = 0
    y = 0
    
    
    circle_x = cc.circle['circle_x'] 
    circle_y = cc.circle['circle_y']    
    circle_r = cc.circle['circle_r']

    #inserted the grid points code by FAO
    i = 1
    
    def create_target(grid, filename=None, plot=False, overwrite=False, verbose=False):
        """
        Usage: create_target(np.linspace(-6.0, 6.0, 8), 
                            filename='../movetables/<NAME>', *)

        grid (list, np array): 
            e.g. np.linspace(-5.5, 5.5, 6) creates a 32 points xy
        """
        xtgt = []
        ytgt = []
        for i,j in list(itertools.product(grid, grid)):
            _dist = np.hypot(i,j)
            if _dist > 2.5:
                if verbose: print(f"out of reach: {i:+.2f}, {j:+.2f}, {_dist:.2f}")
            else:
                xtgt.append(i+circle_x)
                ytgt.append(j+circle_y)

        print(f"Produced {len(xtgt)} targets")

        if plot:
            plt.figure(dpi=100)
            plt.plot(xtgt, ytgt, '+', ms=8)
            plt.plot(0,0, 'ro', zorder=0, alpha=0.4)
            plt.gca().set_aspect('equal')

        if filename is None:
            print("filename is None")
        elif os.path.isfile(filename) and (not overwrite):    
            print(f"\nERROR: File {filename} exists")
        else: 
            np.savetxt(filename, np.c_[xtgt, ytgt])

        return xtgt, ytgt
       
    goalxs, goalys = create_target(np.linspace(-2.5,2.5,6)) #14 does 124, 10 does 60, 19 does 253, 6 does 16
    #end FAO code
    
    print('Goal x:',goalxs)
    print('Goal y:',goalys) 
        
    list_array = []
    for i in range(grid_size):
        list_array.append(i)
        
    def my_shuffle(array):
        shuffle(array)
        return array
     
    shuff_array = my_shuffle(list_array)

    n = 1 #start at trial 1
    i = 0 #start at point 1
    w = 0 #start at zero wins
    tries = []
    drifts = []
    x,y = grab_location('junk')
    #center_piezo()
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
    x,y = grab_location(moveslist)

    while i < int(len(goalxs)):
        j = shuff_array[i]
        print('##',name,'Point',i+1,'Attempt',n)
        
        if n==1:
            dict = {'X (mm)': [goalxs[j]], 'Y (mm)': [goalys[j]]} #add the destination points to the CSV
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % destlist, mode='a', index=False, header=False)
        
        dy = goalys[j] - y
        moveXY(0,dy)
        x,y = grab_location(moveslist) #grab 'final' locaion
        print('## Error:', np.sqrt((float(goalxs[j])-float(x))**2 + (float(goalys[j])-float(y))**2),'mm')
        
        if np.sqrt((float(goalxs[j])-float(x))**2 + (float(goalys[j])-float(y))**2) > error: #check if destination reached
            dx = goalxs[j] - x
            moveXY(dx,0)
            

        x,y = grab_location(moveslist) #grab 'final' locaion
        
        
        if np.sqrt((float(goalxs[j])-float(x))**2 + (float(goalys[j])-float(y))**2) <= error: #check if destination reached
            tries.append(n)
            print('## The error after this trial was:', np.sqrt((float(goalxs[j])-float(x))**2 + (float(goalys[j])-float(y))**2),'mm')

            dict = {'X (mm)': [x], 'Y (mm)': [y]} #add win point
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % winlist, mode='a', index=False, header=False)
            df.to_csv('.\Results\%s.csv' % finalslist, mode='a', index=False, header=False)
            
            dict = {'Error (mm)': [np.sqrt((float(goalxs[j])-float(x))**2 + (float(goalys[j])-float(y))**2)]} #add final error
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % errorlist, mode='a', index=False, header=False)
            
            i += 1 #go to next point
            n = 1 #reset trial counter
            w += 1
            
            print("## Win condition met. That makes",w,"wins.")
            print("## Sleeping for 5 mins...")
            time.sleep(300)
            
            x2,y2 = grab_location(moveslist) #grab 'final' locaion
            drift = np.sqrt((float(x2)-float(x))**2 + (float(y2)-float(y))**2)
            print("## Sleep drift:", drift)
            drifts.append(drift)
            
        else:   
            print('## The error after this trial was:', np.sqrt((float(goalxs[j])-float(x))**2 + (float(goalys[j])-float(y))**2),'mm')
            print('## Trying this point again...') #else attempt point again
            n += 1 #increase trial count

        if n > int(attempts):
            print('## Attempt limit reached. Moving on to the next point...') #unless trial limit reached

            dict = {'X (mm)': [x], 'Y (mm)': [y]} #add loss point
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % losslist, mode='a', index=False, header=False)
            df.to_csv('.\Results\%s.csv' % finalslist, mode='a', index=False, header=False)
            
            dict = {'Error (mm)': [np.sqrt((float(goalxs[j])-float(x))**2 + (float(goalys[j])-float(y))**2)]} #add final error
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % errorlist, mode='a', index=False, header=False)
            
            n = 1 #reset trial count
            i += 1 #go to next point
            print("## Sleeping for 5 mins...")
            time.sleep(300)
            
            x2,y2 = grab_location(moveslist) #grab 'final' locaion
            drift = np.sqrt((float(x2)-float(x))**2 + (float(y2)-float(y))**2)
            print("## Sleep drift:", drift)
            drifts.append(drift)

    else:
        print('## AutoTest complete.') #end after all points attempted
        
        for i in range(0,len(tries)):
            dict = {'Attempts': [tries[i]]} #add the try counts to the CSV
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % attemptlist, mode='a', index=False, header=False)
            
        for i in range(0,len(drifts)):
            dict = {'Drift': [drifts[i]]} #add the try counts to the CSV
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % driftlist, mode='a', index=False, header=False)
            
        timer.stop()

    def Average(lst):
        return sum(lst) / len(lst)

    print('## Final win count:',w,'/',len(goalxs),"with an error of:",error,"mm.")
    try:
        print('## The maximum tries for a single win was',max(tries),'and the minimum was',min(tries),'.')
        print('## The average number of tries per win was',Average(tries),'.')
        print('## The average sleep drift was',Average(drifts),'mm.')
    except:
        pass
    print('## Your results are saved as:',name)


    return name