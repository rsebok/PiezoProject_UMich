#Piezo constants across system
#Piezo 0: Before the time of this folder
#Piezo 1: From FNAL, eventually failed at crack
#Piezo 2: Working well, may be affected by bad glue job (soldered)
#Piezo 3: Decent glue, used in the socket
#Piezo 4: Good glue, initial issues with movement
#Piezo 5: Solder and glue are the best to-date

#Last updated 06/23/2023 by RAS - added all of the micro defs

#speed of each channel (piezo 2)
speeds = dict(
    posX = 1.393, #mm/s
    negX = 1.579,
    posY = 1.735,
    negY = 1.852,
)

#move defs
voltage = 4 #Vpp

micro_slope_posX = 0.084 #mm/V
micro_intercept_posX = 0.065
micro_slope_negX = 0.088
micro_intercept_negX = 0.071
micro_slope_posY = 0.081
micro_intercept_posY = 0.060
micro_slope_negY = 0.074
micro_intercept_negY = 0.053
micro_time = 0.25 #s
micro_freq = 5 #Hz

tiny_slope_posX = micro_slope_posX*2
tiny_intercept_posX = micro_intercept_posX*2
tiny_slope_negX = micro_slope_negX*2
tiny_intercept_negX = micro_intercept_negX*2
tiny_slope_posY = micro_slope_posY*2
tiny_intercept_posY = micro_intercept_posY*2
tiny_slope_negY = micro_slope_negY*2
tiny_intercept_negY = micro_intercept_negY*2
tiny_time = 0.5 #s
tiny_freq = 5 #Hz

min_move = 0.0035 #mm (= acceptable error/root 2)
micro_max = 0.05 #mm
tiny_max = 0.25 #mm

#max range of piezo
circle = dict(
    circle_x = 13.95, #mm
    circle_y = 12.17,   
    circle_r = 2.5,
)

#pixel conversions etc
#wired
#conversion = 0.009615 #mm/pix
#solder
conversion = 0.009036 #mm/pix

