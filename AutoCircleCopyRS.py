#Function to move the positioner along the outer range

#Last updated 05/03/2023 by RAS

import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util


def move_circle():
    
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

# In[ ]:




