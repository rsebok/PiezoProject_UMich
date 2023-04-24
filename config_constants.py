#piezo constants across system

#speed of each channel
speeds = dict(
    posX = 1.610, #mm/s
    negX = 1.709,
    posY = 1.497,
    negY = 2.000,
)

#max range of piezo
circle = dict(
    circle_x = 14.604, #mm
    circle_y = 11.049,   
    circle_r = 2.5,
)

#pixel conversions etc
voltage = 4.0 #Vpp
conversion = 0.009375 #mm/pix
offset = 0.08 #mm
