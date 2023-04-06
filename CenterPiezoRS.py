#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util
import numpy as np


# In[2]:


# In[3]:


def center_piezo():
    posA_speed = 0.855
    posB_speed = 0.681
    negB_speed = 0.717
    negA_speed = 0.844
    
    t = 5 #sec
    
    rm = visa.ResourceManager()
    li = rm.list_resources()
    print(li)
    vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    i=1
    while i<= 2:
        #C1 0 #neg B
        #print(vi.query("*idn?"))
        print("Configuring C1")
        vi.write("c1:bswv frq,10") #set the frequency of channel 1
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        vi.write("c1:bswv amp, 4") #set the amplitude
        vi.write("c1:bswv sym, 0") #set the amplitude
        vi.write("c1:bswv duty,75") #duty cycle
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        vi.write("c1:output on")
        time.sleep(t)
        vi.write("c1:output off")

        #C2 0 #neg A
        #print(vi.query("*idn?"))
        print("Configuring C2")
        vi.write("c2:bswv frq,10") #set the frequency of channel 1
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        vi.write("c2:bswv amp, 4") #set the amplitude
        vi.write("c2:bswv sym, 0") #set the amplitude
        vi.write("c2:bswv duty,75") #duty cycle
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        vi.write("c2:output on")
        time.sleep(t)
        vi.write("c2:output off")

        #C1 100 #pos B
        #print(vi.query("*idn?"))
        print("Configuring C1")
        vi.write("c1:bswv frq,10") #set the frequency of channel 1
        vi.write("c1:bswv wvtp,ramp") #set the type of waveform
        vi.write("c1:bswv amp, 4") #set the amplitude
        vi.write("c1:bswv sym, 100") #set the amplitude
        vi.write("c1:bswv duty,75") #duty cycle
        vi.write("c1:bswv dlay, 1") #brust delay for 1 second
        vi.write("c1:output on")
        time.sleep(t)
        vi.write("c1:output off")

        #C2 100 #pos A
        #print(vi.query("*idn?"))
        print("Configuring C2")
        vi.write("c2:bswv frq,10") #set the frequency of channel 1
        vi.write("c2:bswv wvtp,ramp") #set the type of waveform
        vi.write("c2:bswv amp, 4") #set the amplitude
        vi.write("c2:bswv sym, 100") #set the amplitude
        vi.write("c2:bswv duty,75") #duty cycle
        vi.write("c2:bswv dlay, 1") #brust delay for 1 second
        vi.write("c2:output on")
        time.sleep(t)
        vi.write("c2:output off")
        
        i+=1
        
    x = -2
    #-alpha
    ta = abs(x/negA_speed)

    #C2 0
    #print(vi.query("*idn?"))
    print("Configuring C2")
    vi.write("c2:bswv frq,10") #set the frequency of channel 1
    vi.write("c2:bswv wvtp,ramp") #set the type of waveform
    vi.write("c2:bswv amp, 2") #set the amplitude
    vi.write("c2:bswv sym, 0") #set the amplitude
    vi.write("c2:bswv duty,75") #duty cycle
    vi.write("c2:bswv dlay, 1") #brust delay for 1 second
    vi.write("c2:output on")
    time.sleep(ta)
    vi.write("c2:output off")

# In[4]:

# In[ ]:




