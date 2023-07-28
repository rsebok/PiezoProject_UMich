#The GUI for the piezo positioner setup
#Run this program from the Jupyter terminal

#Last updated 06/22/2023 by RAS

import pyvisa as visa
import PySimpleGUI as sg
from multiprocessing import Process
import sys
import os
import LiveVid as lv
import config_constants as cc
import time
import pandas as pd
from piezolib import *
import smtplib
from email.mime.text import MIMEText
from vpython import * 
from pypylon import pylon

sg.theme('DarkPurple')   # Add a touch of color
# All the stuff inside your window.

col1 = [[sg.Text('X :'), sg.Input(key='x',size=(10))],
        [sg.Text('Y:'), sg.Input(key='y',size=(10))],
        [sg.Text('Voltage:'), sg.Input(key='voltage',size=(10))],
        [sg.Text('Time:'), sg.Input(key='time',size=(10))],
        [sg.Text('Steps:'), sg.Input(key='steps',size=(10))],
        [sg.Text('Trials:'), sg.Input(key='trials',size=(10))],
        [sg.Text('# of Points:'), sg.Input(key='points',size=(10))],
        [sg.Text('Acceptable Error:'), sg.Input(key='error',size=(10))],
        [sg.Text('Max Attempts:'), sg.Input(key='attempts',size=(10))],
        [sg.Checkbox('Email RAS ?', default=True, key='email')]
        ]

col2 = [[sg.Text(' ')],
        [sg.Text('Calibration:')],
        [sg.Button('Center Piezo'),sg.Button('Max Range Fit'),sg.Button('Micro Moves Calib')],
        [sg.Button('AutoVelposX'),sg.Button('AutoVelposY'),sg.Button('AutoVelnegX'),sg.Button('AutoVelnegY')],
        [sg.Text(' ')],
        [sg.Text('Quick options (no inputs required):')],
        [sg.Button('Grab Location'),sg.Button('Start Video')],
        [sg.Button('Run Circle')],
        [sg.Text(' ')],
        [sg.Text('Direct movement control:')],
        [sg.Button('Move by XY'),sg.Button('Move to XY')],
        [sg.Button('posX'),sg.Button('posY'),sg.Button('negX'),sg.Button('negY')],
        [sg.Button('posXsteps'),sg.Button('posYsteps'),sg.Button('negXsteps'),sg.Button('negYsteps')],
        [sg.Text(' ')],
        [sg.Text('Run some analysis:')],
        [sg.Button('AutoXYTest'),sg.Button('AutoXYTestWinCond'),sg.Button('AutoXYTestGRID')],
        [sg.Text(' ')],
        [sg.Text('Power options:')],
        [sg.Button('Power Status'),sg.Button('Power On'),sg.Button('Power Off')],
        [sg.Text(' ')]
        ]

layout=[[sg.Text('~~~ Welcome to the U of Michigan piezo positioner. ~~~')],
        [sg.Text('May the odds be ever in your favor.')],
        [sg.Column(col2), sg.Column(col1,element_justification='right')], 
        [sg.Button('Exit')]]

#Create the Window
window = sg.Window('Piezo GUI',layout,size=(650,750),element_justification='center')
#Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    if event == 'Power On':
        os.system("cd C:\Program Files (x86)\PowerUSB && pwrusbcmd 1 1 1")
        print("All outlets set to: ON")
        
        t = time.localtime()
        current_time = time.strftime(' %Y%m%d_%H%M%S', t)

        dict = {'Power On:'+current_time} #add test to the log
        df = pd.DataFrame(dict)
        df.to_csv('.\log.csv', mode='a', index=False, header=False)
        
    if event == 'Power Off':
        os.system("cd C:\Program Files (x86)\PowerUSB && pwrusbcmd 0 0 0")
        print("All outlets set to: OFF")
        
        t = time.localtime()
        current_time = time.strftime(' %Y%m%d_%H%M%S', t)

        dict = {'Power Off:'+current_time} #add test to the log
        df = pd.DataFrame(dict)
        df.to_csv('.\log.csv', mode='a', index=False, header=False)
        
    if event == 'Power Status':
        try:
            rm = visa.ResourceManager()
            li = rm.list_resources()
            vi = rm.open_resource('USB0::0xF4ED::0xEE3A::388C14124::0::INSTR')
            print("Waveform generator response detected. Power is on.")
        except visa.errors.VisaIOError:
            print("No response from waveform generator. Power is most likely off.")
    
    #quick analysis        
    if event == 'Start Video':
        p1 = Process(target = read_circle)
        p1.start()
        p1.join()
    if event == 'Grab Location':
        x,y = grab_location('junk')
        print('Current coordinates (mm):',x,y)
    if event == 'Run Circle':
        move_circle()
        
        t = time.localtime()
        current_time = time.strftime(' %Y%m%d_%H%M%S', t)

        dict = {'Run Circle:'+current_time} #add test to the log
        df = pd.DataFrame(dict)
        df.to_csv('.\log.csv', mode='a', index=False, header=False)
            
    if event == 'Max Range Fit':
        p1 = Process(target = read_circle)
        p2 = Process(target = move_circle)
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        
        t = time.localtime()
        current_time = time.strftime(' %Y%m%d_%H%M%S', t)

        dict = {'Max Range Fit:'+current_time} #add test to the log
        df = pd.DataFrame(dict)
        df.to_csv('.\log.csv', mode='a', index=False, header=False)
            
    if event == 'Micro Moves Calib':
        micro_calib(int(values['trials']))
        if values['email'] == True:
                send_email()
                
        t = time.localtime()
        current_time = time.strftime(' %Y%m%d_%H%M%S', t)

        dict = {'Micro Moves Calib:'+current_time} #add test to the log
        df = pd.DataFrame(dict)
        df.to_csv('.\log.csv', mode='a', index=False, header=False)
        
    if event == 'Center Piezo':
        x,y = grab_location('junk')
        dy = cc.circle['circle_y'] - y
        moveXY(0,dy)
        x,y = grab_location('junk')
        dx = cc.circle['circle_x'] - x
        moveXY(dx,0)
        
        t = time.localtime()
        current_time = time.strftime(' %Y%m%d_%H%M%S', t)

        dict = {'Center Piezo:'+current_time} #add test to the log
        df = pd.DataFrame(dict)
        df.to_csv('.\log.csv', mode='a', index=False, header=False)
    
    #functions
    if event == 'Move to XY':
        try:
            x,y = grab_location('junk')
            dy = float(values['y']) - y
            moveXY(0,dy)
            x,y = grab_location('junk')
            dx = float(values['x']) - x
            moveXY(dx,0)
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: X, Y.")
    if event == 'Move by XY':
        try:
            moveXY(float(values['x']),float(values['y']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: X, Y.")
    if event == 'posX':
        try:
            move_posX(float(values['x']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: X.")
    if event == 'posY':
        try:
            move_posY(float(values['y']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Y.")
    if event == 'negX':
        try:
            move_negX(float(values['x']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: X.")
    if event == 'negY':
        try:
            move_negY(float(values['y']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Y.")
    if event == 'posXsteps':
        try:
            movesteps_posX(float(values['voltage']),float(values['steps']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Voltage, Steps.")
    if event == 'posYsteps':
        try:
            movesteps_posY(float(values['voltage']),float(values['steps']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Voltage, Steps.")
    if event == 'negXsteps':
        try:
            movesteps_negX(float(values['voltage']),float(values['steps']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Voltage, Steps.")
    if event == 'negYsteps':
        try:
            movesteps_negY(float(values['voltage']),float(values['steps']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Voltage, Steps.")
    
    #testing
    if event == 'AutoXYTest':
        try:
            AutoXYTest(int(values['points']))
            
            t = time.localtime()
            current_time = time.strftime(' %Y%m%d_%H%M%S', t)
    
            dict = {'AutoXYTest:'+current_time} #add test to the log
            df = pd.DataFrame(dict)
            df.to_csv('.\log.csv', mode='a', index=False, header=False)
            
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: # of Points.")
    if event == 'AutoXYTestWinCond':
        try:
            name = AutoXYTestWinCond(int(values['points']),int(values['attempts']),float(values['error']))
            if values['email'] == True:
                send_email()
    
            dict = {'AutoXYTestWinCond:'+name} #add test to the log
            df = pd.DataFrame(dict)
            df.to_csv('.\log.csv', mode='a', index=False, header=False)
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: # of Points, Max Attempts, Acceptable Error.")
        
    if event == 'AutoXYTestGRID':
        try:
            name = AutoXYTestGRID(int(values['attempts']),float(values['error']))
            if values['email'] == True:
                send_email()
    
            dict = {'AutoXYTestGRID:'+name} #add test to the log
            df = pd.DataFrame(dict)
            df.to_csv('.\log.csv', mode='a', index=False, header=False)
            
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Max Attempts, Acceptable Error.")
    if event == 'AutoVelposX':
        try:
            vel_posX(float(values['voltage']),float(values['time']),int(values['trials']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Voltage, Time, Trials.")
    if event == 'AutoVelposY':
        try:
            vel_posY(float(values['voltage']),float(values['time']),int(values['trials']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Voltage, Time, Trials.")
    if event == 'AutoVelnegX':
        try:
            vel_negX(float(values['voltage']),float(values['time']),int(values['trials']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Voltage, Time, Trials.")
    if event == 'AutoVelnegY':
        try:
            vel_negY(float(values['voltage']),float(values['time']),int(values['trials']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: Voltage, Time, Trials.")
window.close()
