#Piezo constants across system

#Last updated 05/19/2023 by RAS - added all of the micro defs

#speed of each channel (piezo 2)
speeds = dict(
    posX = 1.690, #mm/s
    negX = 1.428,
    posY = 1.468,
    negY = 1.725,
)

#micro move defs
micro_voltage_posX = 2.5 #Vpp
micro_voltage_negX = 2.5 #Vpp
micro_voltage_posY = 2.25 #Vpp
micro_voltage_negY = 2.8 #Vpp
micro_time = 1 #s
micro_freq = 0.1 #Hz

min_move = 0.005 #mm
micro_max = 0.025 #mm
double_micro_max = 0.04 #mm
tiny_max = 0.25 #mm

#not using atm
pix_move_dist = dict(
    posX = 0.005, #mm
    negX = 0.01,
    posY = 0.005,
    negY = 0.005,
)    
    

#max range of piezo
circle = dict(
    circle_x = 15.552, #mm
    circle_y = 11.255,   
    circle_r = 2.5,
)

#pixel conversions etc
voltage = 4 #Vpp
conversion = 0.009386 #mm/pix

