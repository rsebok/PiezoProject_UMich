#piezo constants across system

#speed of each channel
speeds = dict(
    posX = 1.8046, #mm/s
    negX = 1.7787,
    posY = 1.7555,
    negY = 1.5822,
)

#max range of piezo
circle = dict(
    circle_x = 14.760, #mm
    circle_y = 11.537,   
    circle_r = 2.5,
)

#pixel conversions etc
voltage = 4.0 #Vpp
conversion = 0.009375 #mm/pix
offset = 0.08 #mm
