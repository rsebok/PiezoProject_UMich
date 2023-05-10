#Piezo constants across system

#Last updated 05/09/2023 by RAS - experimented with new piezo tube

#speed of each channel (piezo 1)
speeds = dict(
    posX = 1.775, #mm/s
    negX = 1.742,
    posY = 2.225,
    negY = 1.772,
)

#speed of each channel (piezo 2)
#speeds = dict(
    #posX = 1.284, #mm/s
    #negX = 1.048,
    #posY = 1.238,
    #negY = 1.206,
#)

pix_move_dist = dict(
    posX = 0.005, #mm
    negX = 0.01,
    posY = 0.005,
    negY = 0.005,
)    
    

#max range of piezo
circle = dict(
    circle_x = 15.293, #mm
    circle_y = 10.880,   
    circle_r = 2.5,
)

#pixel conversions etc
voltage = 4 #Vpp
conversion = 0.009053 #mm/pix
