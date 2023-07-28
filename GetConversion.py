#Code to return conversion factor

#Last updated 06/23/2023 by RAS

import cv2
import numpy as np
import sys

image = sys.argv[1]

# Read image.
img = cv2.imread(image, cv2.IMREAD_COLOR)

# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))

# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
               param2 = 30, minRadius = 75, maxRadius = 100)

rads = []

# Draw circles that are detected.
if detected_circles is not None:

    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        rads.append(r)
        
    print("Conversion factor (mm/pix):",1.5/(2*np.average(r)))
    
else:
    print("Failed to find a circle.")
    
