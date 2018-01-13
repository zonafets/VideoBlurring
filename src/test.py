#!/usr/bin/env python

__author__ = "Stefano Zaglio"
__license__ = "MIT"
__version__ = "0.9.0"

import cv2
import numpy as np
# from matplotlib import pyplot as plt
import random
import glob

def AutoBlur( frame, template ):

	img = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY )
	w, h = template.shape[ ::-1 ]

	res = cv2.matchTemplate( img, template, cv2.TM_CCOEFF_NORMED )
	threshold = 0.77
	loc = np.where( res >= threshold )
	for f in zip( *loc[::-1] ):

	    x, y = f
	    
	    # cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,0), 5)
	    blurred = frame[ y:y+h, x:x+w ]
	    blurred = cv2.GaussianBlur( blurred, (11, 11), 5 )
	    # RoundedRectangle(blurred);
	    # merge this blurry rectangle to our final image
	    frame[ y:y + blurred.shape[0], x:x + blurred.shape[1] ] = blurred
	

iframe = cv2.imread('test.png')
oframe=iframe.copy()
templates = glob.glob('templates/*.png')
for t in templates:
	print(t)
	template = cv2.imread( t, 0 )
	AutoBlur( iframe, template)
	#del(template)

cv2.imshow( "Img Source", iframe )
cv2.imshow( "Img Blurred", oframe )
cv2.waitKey(0)
cv2.destroyAllWindows()
