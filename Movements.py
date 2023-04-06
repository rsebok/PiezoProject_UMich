import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util

def move_posX(voltage,t):
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')

    if voltage >=6:
        print('That voltage is too high!')
        return
    
    print('posX',voltage,'Vpp',t,'s')
        
    #C1 0 #neg B
    #print(vi.query("*idn?"))
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
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    time.sleep(0.6)
    
    print('Move done.')

def move_posY(voltage,t):
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('posY',voltage,'Vpp',t,'s')
    

    #C2 0 #neg Y
    #print(vi.query("*idn?"))
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
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")
    time.sleep(0.6)
    
    print('Move done.')

def move_negX(voltage,t):
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('negX',voltage,'Vpp',t,'s')
 
    #C1 100 #pos B
    #print(vi.query("*idn?"))
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
    time.sleep(1)
    vi.write("c1:output on")
    time.sleep(t)
    vi.write("c1:output off")
    time.sleep(0.6)
    
    print('Move done.')
    
def move_negY(voltage,t):
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    if voltage >=6:
        print('That voltage is too high!')
        return
        
    print('negY',voltage,'Vpp',t,'s')
 
    #C2 100 #neg A
    #print(vi.query("*idn?"))
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
    time.sleep(1)
    vi.write("c2:output on")
    time.sleep(t)
    vi.write("c2:output off")
    time.sleep(0.6)

    print('Move done.')
