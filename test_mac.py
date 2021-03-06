
# Import the necessary packages
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
import pdb

from motion_detection import *

# Width of camera frame, i.e. width of displayed picture
frameWidth = 500
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
  help="path to the JSON configuration file")
args = vars(ap.parse_args())
 
# filter warnings, load the configuration
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

# Imports change if the system is being run on a pi or on mac
if conf["use_pi"]:
  from picamera.array import PiRGBArray
  from picamera import PiCamera
  # initialize the camera and grab a reference to the raw camera capture
  camera = PiCamera()
  camera.resolution = tuple(conf["resolution"])
  camera.framerate = conf["fps"]
  rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))
else:
  camera = cv2.VideoCapture(0)
  #CV_CAP_PROP_FRAME_WIDTH
  camera.set(3,conf["resolution"][0])
  #CV_CAP_PROP_FRAME_HEIGHT
  camera.set(4,conf["resolution"][1])
  #CV_CAP_PROP_FPS
  camera.set(5,conf["fps"])
  time.sleep(0.25)
  [grabbed, rawCapture] = camera.read()

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

# capture frames from the camera
while True:
  if conf["use_pi"]:
    #f = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    camera.capture(rawCapture, format="bgr", use_video_port=True)
    #frame = f.array
    frame = rawCapture.array
  else:
    (grabbed, frame) = camera.read()

  # Resize the frame
  frame = imutils.resize(frame, width=frameWidth)

  # if the average frame is None, initialize it
  if avg is None:
    print("[INFO] starting background model...")
    # Convert the frame to grayscale, and blur it
    # frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    avg = gray.copy().astype("float")
    if conf["use_pi"]:
      rawCapture.truncate(0) #re-set rawCapture PiRGBArray object for next image capture
    continue

  # grab the raw NumPy array representing the image and initialize
  # the timestamp and occupied/unoccupied text
  timestamp = datetime.datetime.now()
  text = "Unoccupied"
  #GPIO.output(ledPin, False)
 
  # >>------------ Motion Detection Algorithm -------------------------->>
  # Motion detection and max area centroid location is calculated
  [frame, text, avg, centroid_x, centroid_y] = motion_detection(frame, avg, text, conf, timestamp)
  # <<------------ Motion Detection Algorithm --------------------------<<


  # >>------------ Stepper Motion Controls ----------------------------->>

  # <<------------ Stepper Motion Controls -----------------------------<<




  #----------------------------------DROPBOX----------------------------- >>
  # code for uploading to Dropbox
  # check to see if the room is occupied
  if text == "Occupied":
    # check to see if enough time has passed between uploads
    if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
      # increment the motion counter
      motionCounter += 1
 
      # check to see if the number of frames with consistent motion is
      # high enough
      if motionCounter >= conf["min_motion_frames"]:
        # update the last uploaded timestamp and reset the motion
        # counter
        lastUploaded = timestamp
        motionCounter = 0
 
  # otherwise, the room is not occupied
  else:
    motionCounter = 0


  #-------------------------DISPLAY OR CLOSE----------------------------- >>
  # check to see if the frames should be displayed to screen
  if conf["show_video"]:
    # display the security feed
    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
      break
 
  # clear the stream in preparation for the next frame
  if conf["use_pi"]:
    rawCapture.truncate(0)#re-set rawCapture PiRGBArray object for next image capture
