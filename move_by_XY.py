import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util
import numpy as np
import config_constants as cc
from Movements import move_negX,move_posX,move_negY,move_posY
from TinyMovements import tinymove_negX,tinymove_posX,tinymove_negY,tinymove_posY
from PixMovements import pixmove_negX,pixmove_posX,pixmove_negY,pixmove_posY
from SmallMovements import smallmove_negX,smallmove_posX,smallmove_negY,smallmove_posY

def moveXY(x,y):
    
    rm=visa.ResourceManager()
    li=rm.list_resources()
    vi=rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')

    negX_speed = cc.speeds['negX']
    negY_speed = cc.speeds['negY']
    posY_speed = cc.speeds['posY']
    posX_speed = cc.speeds['posX']
    voltage = cc.voltage

    
    print(x,y)
    
    #Use this section to move in pos x
    if x > 0:
        t = abs(x/posX_speed)
        if abs(x) <= 0.005:
            return
        #elif abs(x) <= 0.08:
            #smallmove_posX(x)
            #i = 2
            #while i <= abs(x)/0.01:
                #smallmove_posX(x)
                #i+=1
        elif abs(x) <= 0.5:
            tinymove_posX(voltage,x)
        else:
            move_posX(voltage,t)

    #Use this section to move in neg x
    if x < 0:
        t = abs(x/negX_speed)
        if abs(x) <= 0.005:
            return
        #elif abs(x) <= 0.08:
            #smallmove_negX(x)
            #i = 2
            #while i <= abs(x)/0.01:
                #smallmove_negX(x)
                #i+=1
        elif abs(x) <= 0.5:
            tinymove_negX(voltage,x)
        else:
            move_negX(voltage,t)
        
    #Use this section to move in pos y
    if y > 0:
        t = abs(y/posY_speed)
        if abs(y) <= 0.005:
            return
        #elif abs(y) <= 0.08:
            #smallmove_posY(y)
            #i = 2
            #while i <= abs(y)/0.01:
                #smallmove_posY(y)
                #i+=1
        elif abs(y) <= 0.5:
            tinymove_posY(voltage,y)
        else:
            move_posY(voltage,t)

    #Use this section to move in neg y
    if y < 0:
        t = abs(y/negY_speed)
        if abs(y) <= 0.005:
            return
        #elif abs(y) <= 0.08:
            #smallmove_negY(y)
            #i = 2
            #while i <= abs(y)/0.01:
                #smallmove_negY(y)
                #i+=1
        elif abs(y) <= 0.5:
            tinymove_negY(voltage,y)
        else:
            move_negY(voltage,t)
        
