#Function to test the distance moved per second
#Input: voltage, time per move, trials

#Last updated 05/03/2023 by RAS

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

def vel_negX(voltage,runtime,trials):
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    if runtime >=5:
        print('That runtime is too high!')
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
    
    #starts by centering the piezo and saving an initial location
    #x,y = grab_location('junk')
    #center_piezo()
    #moveXY(cc.circle[circle_x]-x,cc.circle[circle_y-y]) #send the piezo back to the center of config range
    grab_location(name)
    
    #loop through the test for n trials
    n = 1 
    while n <= trials: #number of trials
        print('trial #',n)
        move_negX(voltage,runtime) #select the movement direction to test
        #time.sleep(2)
        grab_location(name) #add new location to CSV
        move_posX(voltage,runtime) #send the piezo back to the center
        #time.sleep(2)
        grab_location(name) #add new location to CSV
        n += 1 
    else:
        print('AutoTest complete.')
        
    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file
    start = data.iloc[2::2, :]
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
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    if runtime >=5:
        print('That runtime is too high!')
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
    
    #starts by centering the piezo and saving an initial location
    #x,y = grab_location('junk')
    #center_piezo()
    #moveXY(cc.circle[circle_x]-x,cc.circle[circle_y-y]) #send the piezo back to the center of config range
    grab_location(name)
    
    #loop through the test for n trials
    n = 1 
    while n <= trials: #number of trials
        print('trial #',n)
        move_negY(voltage,runtime) #select the movement direction to test
        #time.sleep(2)
        grab_location(name) #add new location to CSV
        move_posY(voltage,runtime) #send the piezo back to the center
        #time.sleep(2)
        grab_location(name) #add new location to CSV
        n += 1 
    else:
        print('AutoTest complete.')
        
    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file
    start = data.iloc[2::2, :]
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
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    if runtime >=5:
        print('That runtime is too high!')
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
    
    #starts by centering the piezo and saving an initial location
    #x,y = grab_location('junk')
    #center_piezo()
    #moveXY(cc.circle[circle_x]-x,cc.circle[circle_y-y]) #send the piezo back to the center of config range
    grab_location(name)
    
    #loop through the test for n trials
    n = 1 
    while n <= trials: #number of trials
        print('trial #',n)
        move_posY(voltage,runtime) #select the movement direction to test
        #time.sleep(2)
        grab_location(name) #add new location to CSV
        move_negY(voltage,runtime) #send the piezo back to the center
        #time.sleep(2)
        grab_location(name) #add new location to CSV
        n += 1 
    else:
        print('AutoTest complete.')
        
    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file
    start = data.iloc[2::2, :]
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
    
    if voltage >=6:
        print('That voltage is too high!')
        return
    if runtime >=5:
        print('That runtime is too high!')
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
    
    #starts by centering the piezo and saving an initial location
    #x,y = grab_location('junk')
    #center_piezo()
    #moveXY(cc.circle[circle_x]-x,cc.circle[circle_y-y]) #send the piezo back to the center of config range
    grab_location(name)
    
    #loop through the test for n trials
    n = 1 
    while n <= trials: #number of trials
        print('trial #',n)
        move_posX(voltage,runtime) #select the movement direction to test
        #time.sleep(2)
        grab_location(name) #add new location to CSV
        move_negX(voltage,runtime) #send the piezo back to the center
        #time.sleep(2)
        grab_location(name) #add new location to CSV
        n += 1 
    else:
        print('AutoTest complete.')
        
    headers = ['X (mm)', 'Y (mm)']
    data = pd.read_csv('.\Results\%s.csv' % name, names=headers) #select your file
    start = data.iloc[2::2, :]
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




