#Function to test the positioning
#Input: number of random points to attempt

#Last updated 05/03/2023 by RAS

import time
import random
import math
import array
import pandas as pd
from AutoCircleCopyRS import move_circle
from move_by_XY import moveXY
from GrabLocation import grab_location
from Movements import move_negX,move_posX,move_negY,move_posY
import config_constants as cc

def AutoXYTest(points):
    
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





