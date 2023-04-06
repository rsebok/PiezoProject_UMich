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
        elif abs(x) <= 0.03:
            pixmove_posX()
        elif abs(x) <= 0.05:
            pixmove_posX()
            pixmove_posX()
        elif abs(x) <= 0.3:
            tinymove_posX(voltage,x)
        else:
            move_posX(voltage,t)

    #Use this section to move in neg x
    if x < 0:
        t = abs(x/negX_speed)
        if abs(x) <= 0.005:
            return
        elif abs(x) <= 0.03:
            pixmove_negX()
        elif abs(x) <= 0.05:
            pixmove_negX()
            pixmove_negX()
        elif abs(x) <= 0.3:
            tinymove_negX(voltage,x)
        else:
            move_negX(voltage,t)
        
    #Use this section to move in pos y
    if y > 0:
        t = abs(y/posY_speed)
        if abs(y) <= 0.005:
            return
        elif abs(y) <= 0.03:
            pixmove_posY()
        elif abs(y) <= 0.05:
            pixmove_posY()
            pixmove_posY()
        elif abs(y) <= 0.3:
            tinymove_posY(voltage,y)
        else:
            move_posY(voltage,t)

    #Use this section to move in neg y
    if y < 0:
        t = abs(y/negY_speed)
        if abs(y) <= 0.005:
            return
        elif abs(y) <= 0.03:
            pixmove_negY()
        elif abs(y) <= 0.05:
            pixmove_negY()
            pixmove_negY()
        elif abs(y) <= 0.3:
            tinymove_negY(voltage,y)
        else:
            move_negY(voltage,t)
        
