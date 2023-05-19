#The GUI for the piezo positioner setup
#Run this program from the Jupyter terminal

#Last updated 05/03/2023 by RAS

import pyvisa as visa
import PySimpleGUI as sg
from multiprocessing import Process
import sys
import os
import LiveVid as lv
from Movements import move_negX,move_posX,move_negY,move_posY
from MovementsSteps import movesteps_negX,movesteps_posX,movesteps_negY,movesteps_posY
import AutoCircleCopyRS as autocircle
import AutoXYTest as xy
import AutoXYTestWinCond as xywc
import AutoXYTestGRID as xygrid
from AutoVelocityTest import vel_posX,vel_negX,vel_posY,vel_negY
import GrabLocation as gb
import AutoFitCircle as afc
import move_by_XY as move
import config_constants as cc
import emailRAS as em


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
        [sg.Checkbox('Email RAS ?', default=False, key='email')]
        ]

col2 = [[sg.Text(' ')],
        [sg.Text('Quick info (no inputs required):')],
        [sg.Button('Grab Location'),sg.Button('Start Video')],
        [sg.Button('Center Piezo'),sg.Button('Run Circle'),sg.Button('Max Range Fit')],
        [sg.Text(' ')],
        [sg.Text('Direct movement control:')],
        [sg.Button('Move by XY'),sg.Button('Move to XY')],
        [sg.Button('posX'),sg.Button('posY'),sg.Button('negX'),sg.Button('negY')],
        [sg.Button('posXsteps'),sg.Button('posYsteps'),sg.Button('negXsteps'),sg.Button('negYsteps')],
        [sg.Text(' ')],
        [sg.Text('Run some analysis:')],
        [sg.Button('AutoXYTest'),sg.Button('AutoXYTestWinCond'),sg.Button('AutoXYTestGRID')],
        [sg.Button('AutoVelposX'),sg.Button('AutoVelposY'),sg.Button('AutoVelnegX'),sg.Button('AutoVelnegY')],
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
window = sg.Window('Piezo GUI',layout,size=(650,650),element_justification='center')
#Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    if event == 'Power On':
        os.system("cd C:\Program Files (x86)\PowerUSB && pwrusbcmd 1 1 1")
        print("All outlets set to: ON")
    if event == 'Power Off':
        os.system("cd C:\Program Files (x86)\PowerUSB && pwrusbcmd 0 0 0")
        print("All outlets set to: OFF")
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
        p1 = Process(target = afc.read_circle)
        p1.start()
        p1.join()
    if event == 'Grab Location':
        x,y = gb.grab_location('junk')
        print('Current coordinates (mm):',x,y)
    if event == 'Run Circle':
        autocircle.move_circle()
    if event == 'Max Range Fit':
        p1 = Process(target = afc.read_circle)
        p2 = Process(target = autocircle.move_circle)
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    if event == 'Center Piezo':
        x,y = gb.grab_location('junk')
        dy = cc.circle['circle_y'] - y
        move.moveXY(0,dy)
        x,y = gb.grab_location('junk')
        dx = cc.circle['circle_x'] - x
        move.moveXY(dx,0)
    
    #functions
    if event == 'Move to XY':
        try:
            x,y = gb.grab_location('junk')
            dy = float(values['y']) - y
            move.moveXY(0,dy)
            x,y = gb.grab_location('junk')
            dx = float(values['x']) - x
            move.moveXY(dx,0)
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: X, Y.")
    if event == 'Move by XY':
        try:
            move.moveXY(float(values['x']),float(values['y']))
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
            xy.AutoXYTest(int(values['points']))
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: # of Points.")
    if event == 'AutoXYTestWinCond':
        try:
            xywc.AutoXYTestWinCond(int(values['points']),int(values['attempts']),float(values['error']))
            if values['email'] == True:
                em.send_email()
        except:
            print("## FAILED. Double check that power is on and camera is closed. Inputs required: # of Points, Max Attempts, Acceptable Error.")
    if event == 'AutoXYTestGRID':
        try:
            xygrid.AutoXYTestGRID(int(values['attempts']),float(values['error']))
            if values['email'] == True:
                em.send_email()
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
