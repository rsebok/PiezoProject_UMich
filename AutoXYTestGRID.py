#Function to test the positioning with multiple attempts
#Input: attempts allowed, and acceptable error (win condition)

#Last updated 05/19/2023 by RAS - created test

import time
from timer import Timer
import math
import array
import pandas as pd
import numpy as np
import pyvisa as visa
import os
from AutoCircleCopyRS import move_circle
from move_by_XY import moveXY
from GrabLocation import grab_location
import config_constants as cc
import matplotlib.pyplot as plt
import itertools
import sys


def AutoXYTestGRID(attempts,error):
    
    print('## Starting an XY test for a 60 point grid with a win condition of',error,'mm and a max attempt limit of',attempts)
    timer = Timer()
    timer.start()
    
    name = '\AutoXYTest'
    t = time.localtime()
    current_time = time.strftime('_%Y%m%d_%H%M%S', t)
    name = name+current_time
    print(name)
    folder = '.\Results'
    os.mkdir(folder+name)
    fulllist = name+'\FullList'
    winlist = name+'\WinList'
    losslist = name+'\LossList'
    errorlist = name+'\ErrorList'
    print(fulllist)
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
       
    goalxs, goalys = create_target(np.linspace(-2.5,2.5,10))
    #end FAO code

    print('Goal x:',goalxs)
    print('Goal y:',goalys)

    n = 1 #start at trial 1
    i = 1 #start at point 1
    w = 0 #start at zero wins
    tries = []
    x,y = grab_location('junk')
    #center_piezo()
    moveXY(circle_x-x,circle_y-y) #send the piezo back to the center
    x,y = grab_location(fulllist)

    while i <= int(len(goalxs)):
        print('## Point',i,',Trial',n)
        #x,y = grab_location(name) #add new location to CSV
        #time.sleep(1)

        dict = {'X (mm)': [goalxs[i-1]], 'Y (mm)': [goalys[i-1]]} #add the destination point to the CSV every time
        df = pd.DataFrame(dict)
        df.to_csv('.\Results\%s.csv' % fulllist, mode='a', index=False, header=False)
        
        dx = goalxs[i-1] - x
        moveXY(dx,0)
        x,y = grab_location('junk')
        
        if np.sqrt((float(goalxs[i-1])-float(x))**2 + (float(goalys[i-1])-float(y))**2) > error: #check if destination reached
            
            dy = goalys[i-1] - y
            moveXY(0,dy)

        x,y = grab_location(fulllist) #grab 'final' locaion
        
        
        if np.sqrt((float(goalxs[i-1])-float(x))**2 + (float(goalys[i-1])-float(y))**2) <= error: #check if destination reached
            tries.append(n)
            print('## The error after this trial was:', np.sqrt((float(goalxs[i-1])-float(x))**2 + (float(goalys[i-1])-float(y))**2),'mm')

            dict = {'X (mm)': [x], 'Y (mm)': [y]} #add win point
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % winlist, mode='a', index=False, header=False)
            
            dict = {'Error (mm)': [np.sqrt((float(goalxs[i-1])-float(x))**2 + (float(goalys[i-1])-float(y))**2)]} #add final error
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % errorlist, mode='a', index=False, header=False)
            
            i += 1 #go to next point
            n = 1 #reset trial counter
            w += 1
            
            print("## Win condition met. That makes",w,"wins.")
            
        else:   
            print('## The error after this trial was:', np.sqrt((float(goalxs[i-1])-float(x))**2 + (float(goalys[i-1])-float(y))**2),'mm')
            print('## Trying this point again...') #else attempt point again
            n += 1 #increase trial count

        if n > int(attempts):
            print('## Attempt limit reached. Moving on to the next point...') #unless trial limit reached

            dict = {'X (mm)': [x], 'Y (mm)': [y]} #add loss point
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % losslist, mode='a', index=False, header=False)
            
            dict = {'Error (mm)': [np.sqrt((float(goalxs[i-1])-float(x))**2 + (float(goalys[i-1])-float(y))**2)]} #add final error
            df = pd.DataFrame(dict)
            df.to_csv('.\Results\%s.csv' % errorlist, mode='a', index=False, header=False)
            
            n = 1 #reset trial count
            i += 1 #go to next point

    else:
        print('## AutoTest complete.') #end after all points attempted
        timer.stop()

    def Average(lst):
        return sum(lst) / len(lst)

    print('## Final win count:',w,'/',len(goalxs),"with an error of:",error,"mm.")
    print('## The maximum tries for a single win was',max(tries),'and the minimum was',min(tries),'.')
    print('## The average number of tries per win was',Average(tries),'.')
    print('## Your results are saved as:',name)





