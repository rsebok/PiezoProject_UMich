#These functions are used to move the positioner a certain number of steps at 10 Hz
#Input: voltage and number of steps

#Last updated 05/03/2023 by RAS

import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util

def movesteps_posY(voltage,steps):
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
