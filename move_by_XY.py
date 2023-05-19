#The function that ties together all of the different movement styles to best position the spine
#Input: distance to move in x and y

#Last updated 05/15/2023 by RAS

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
from MicroMovements import micromove_negX,micromove_posX,micromove_negY,micromove_posY

def moveXY(x,y):
    
    print("## Attempting to move by:",x,y)
     
            
    #Use this section to move in pos x
    if x > 0:
        if abs(x) <= cc.min_move:
            print("## Requested move is too small.")
            return
        elif abs(x) <= cc.micro_max:
            micromove_posX(x)
        elif abs(x) <= cc.double_micro_max:
            micromove_posX(x)
            micromove_posX(x)
        elif abs(x) <= cc.tiny_max:
            tinymove_posX(x)
        else:
            move_posX(x)

    #Use this section to move in neg x
    if x < 0:
        if abs(x) <= cc.min_move:
            print("## Requested move is too small.")
            return
        elif abs(x) <= cc.micro_max:
            micromove_negX(x)
        elif abs(x) <= cc.double_micro_max:
            micromove_negX(x)
            micromove_negX(x)
        elif abs(x) <= cc.tiny_max:
            tinymove_negX(x)
        else:
            move_negX(x)
       
    
    if y > 0:
        if abs(y) <= cc.min_move:
            print("## Requested move is too small.")
            return
        elif abs(y) <= cc.micro_max:
            micromove_posY(y)
        elif abs(y) <= cc.double_micro_max:
            micromove_posY(y)
            micromove_posY(y)
        elif abs(y) <= cc.tiny_max:
            tinymove_posY(y)
        else:
            move_posY(y)

    #Use this section to move in neg y
    if y < 0:
        if abs(y) <= cc.min_move:
            print("## Requested move is too small.")
            return
        elif abs(y) <= cc.micro_max:
            micromove_negY(y)
        elif abs(y) <= cc.double_micro_max:
            micromove_negY(y)
            micromove_negY(y)
        elif abs(y) <= cc.tiny_max:
            tinymove_negY(y)
        else:
            move_negY(y)
     

