#Piezo constants across system

#Last updated 05/03/2023 by RAS

#speed of each channel
speeds = dict(
    posX = 1.775, #mm/s
    negX = 1.742,
    posY = 2.225,
    negY = 1.772,
)

pix_move_dist = dict(
    posX = 0.005, #mm
    negX = 0.01,
    posY = 0.005,
    negY = 0.005,
)    
    

#max range of piezo
circle = dict(
    circle_x = 14.604, #mm
    circle_y = 11.049,   
    circle_r = 2.5,
)

#pixel conversions etc
voltage = 4 #Vpp
conversion = 0.009375 #mm/pix
