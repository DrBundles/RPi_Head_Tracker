
# Import the necessary packages
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
 
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
  time.sleep(0.25)
  [grabbed, rawCapture] = camera.read()

