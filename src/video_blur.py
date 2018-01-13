#! /usr/bin/env python3

__author__ = "Stefano Zaglio"
__license__ = "MIT"
__version__ = "0.9.0"

import os
import sys
import datetime
import glob
import cv2
import numpy as np


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name

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
        blurred = cv2.GaussianBlur( blurred, (11, 11), 10 )
        # RoundedRectangle(blurred);
        # merge this blurry rectangle to our final image
        frame[ y:y + blurred.shape[0], x:x + blurred.shape[1] ] = blurred
        
        
# =============================================================================

ifile = sys.argv[1]
print("video input file is:", ifile)

if len(sys.argv)>2:
    ofile = sys.argv[2]
else:
    ofile = ""

video = cv2.VideoCapture( ifile )

# Check if camera opened successfully
if (video.isOpened()== False):
  print("Error opening video stream or file")
  quit()
  
frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
fps = video.get(cv2.CAP_PROP_FPS)
size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
		int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

print("FPS: %.2f" % fps)
print("COUNT: %.2f" % frames)
print("WIDTH: %d" % size[0])
print("HEIGHT: %d" % size[1])

n = 0
pos = 0
cv2.setNumThreads(4)
            
# Define the codec and create VideoWriter object
if (ofile!=""):
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fourcc = cv2.VideoWriter_fourcc(*'H264') # loses quality
    # fourcc = cv2.VideoWriter_fourcc(*'HFYU') # really too big (and loses quality)
    if os.path.isfile( ofile ):
        print("video out file exists and is:", ofile)
        tfile = ofile + '.tmp'
        os.rename( ofile, tfile )
        
    else:
        print("video out file is:", ofile)
        tfile = ''

    out = cv2.VideoWriter( ofile, fourcc, fps, size )
    
    if tfile != '':
        # every resume re-compress the frames, losing in quality
        tvideo = cv2.VideoCapture( tfile )

        if (tvideo.isOpened()== False):
          print("Error opening video stream or file")
          os.rename( tfile, ofile )
          quit()
          
        n = pos = int( tvideo.get( cv2.CAP_PROP_FRAME_COUNT ))
        while(tvideo.isOpened()):
          ret, frame = tvideo.read()
          if ret == True:
            out.write(frame)
          else:
            break

        tvideo.release()
        os.remove(tfile)


templates = glob.glob('templates/*.png')
templates.sort()
for t in templates: print(t)

video.set( cv2.CAP_PROP_POS_FRAMES, pos )

while(video.isOpened()):
  ret, frame = video.read()
  if ret == True:
    n += 1
    
    for t in templates:
        template = cv2.imread( t, 0 )
        AutoBlur( frame, template)

    del(template)

    if (ofile != ""):
        out.write(frame)
    #else:
        small = cv2.resize( frame, (0,0), fx=0.7, fy=0.7 )
        cv2.imshow('Result', small )

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
    '''
    skip = 20
    while skip>0 and ret == True : 
        skip-=1
        ret, frame = video.read()
        n += 1
    '''        
    if (n % (10*fps)) == 0: 
        today = datetime.date.today()
        print( today, "frame", n, " of ", frames )

    # if n>100: break

    
  else:
    break

# When everything done, release the video capture object
video.release()
if (ofile!=""):
    out.release()
    
# Closes all the frames
cv2.destroyAllWindows()

# =========================================================================

