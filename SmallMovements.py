import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util
import config_constants as cc

negX_speed = cc.speeds['negX']
negY_speed = cc.speeds['negY']
posY_speed = cc.speeds['posY']
posX_speed = cc.speeds['posX']

def smallmove_posX(x):
    #Use this section to move in pos x
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    newt = 0.5
    freq = 0.1
    voltage = 1.6

    print('posX',voltage,'Vpp',newt,'s')

    #print(vi.query("*idn?"))
    print("Configuring C1")
    vi.write("c1:bswv frq, %s" %freq) #set the frequency of channel 1
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
    time.sleep(newt)
    vi.write("c1:output off")
    time.sleep(1)

    print('Small move done.')
    
def smallmove_negX(x):
    #Use this section to move in neg x
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    
    
    newt = 0.5
    freq = 0.1
    voltage = 2.25

    print('negX',voltage,'Vpp',newt,'s')

    #print(vi.query("*idn?"))
    print("Configuring C1")
    vi.write("c1:bswv frq, %s" %freq) #set the frequency of channel 1
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
    time.sleep(newt)
    vi.write("c1:output off")
    time.sleep(1)

    print('Small move done.')

def smallmove_negY(y):
    #Use this section to move in neg y
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    newt = 0.5
    freq = 0.1
    voltage = 2.8

    print('negY',voltage,'Vpp',newt,'s')

    #print(vi.query("*idn?"))
    print("Configuring C2")
    vi.write("c2:bswv frq, %s" %freq) #set the frequency of channel 1
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
    time.sleep(newt)
    vi.write("c2:output off")
    time.sleep(1)

    print('Small move done.')

def smallmove_posY(y):
    #Use this section to move in pos y
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    
    newt = 0.5
    freq = 0.1
    voltage = 1.7

    print('posY',voltage,'Vpp',newt,'s')

    #print(vi.query("*idn?"))
    print("Configuring C2")
    vi.write("c2:bswv frq, %s" %freq) #set the frequency of channel 1
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
    time.sleep(newt)
    vi.write("c2:output off")
    time.sleep(1)

    print('Small move done.')

        