import pyvisa as visa
import time
import cv2
import sys
import usb.core
import usb.util
import numpy as np
import config_constants as cc
from Movements import move_negX,move_posX,move_negY,move_posY


def moveXY(x,y):
    
    rm = visa.ResourceManager()
    li = rm.list_resources()
    print(li)
    vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
    vi.read_termination = '\r'
    vi.write_termination = '\r'
    
    negX_speed = cc.speeds['negX']
    negY_speed = cc.speeds['negY']
    posY_speed = cc.speeds['posY']
    posX_speed = cc.speeds['posX']
    voltage = cc.voltage

    
    print(x,y)
    
    #Use this section to move in pos x
    if x > 0:
        t = abs(x/posX_speed)

        move_posX(voltage,t)

    #Use this section to move in neg x
    if x < 0:
        t = abs(x/negX_speed)

        move_negX(voltage,t)
        
    #Use this section to move in pos y
    if y > 0:
        t = abs(y/posY_speed)

        move_posY(voltage,t)

    #Use this section to move in neg y
    if y < 0:
        t = abs(y/negY_speed)

        move_negY(voltage,t)
        
