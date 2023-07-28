#Function to test the distance moved per second
#Input: voltage, time per move, trials

#Last updated 05/25/2023 by RAS - added centering to every trial

import time
import random
import array
import pandas as pd
import numpy as np
from AutoCircleCopyRS import move_circle
from move_by_XY import moveXY
from GrabLocation import grab_location
from Movements import move_posY,move_negY,move_posX,move_negX
import config_constants as cc
import pyvisa as visa

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

dict = {'LongTermTest:'+name} #add test to the log
df = pd.DataFrame(dict)
df.to_csv('.\log.csv', mode='a', index=False, header=False)

x,y = grab_location('junk')
moveXY(circle_x-x,circle_y-y) #send the piezo back to the center

x,y = grab_location(name)

#loop through the test for n trials
n = 1
while n <= 500: #number of trials
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
xdiffs = [ele for ele in xdiffs if abs(ele) < 2]

ydiffs = np.subtract(endy, starty)
ydiffs = list(ydiffs)
ydiffs = [ele for ele in ydiffs if abs(ele) < 2]

print(xdiffs,ydiffs)

print('Your results are saved as:',name)

