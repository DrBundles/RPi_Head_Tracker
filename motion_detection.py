def motion_detection(frame, avg, text, conf, timestamp):

  import imutils
  import cv2
  import pdb

  # setup GPIO
  ledPin = 21
  #GPIO.setmode(GPIO.BCM)
  #GPIO.setup(21, GPIO.OUT)
  #GPIO.output(21, 0)

  # Convert the frame to grayscale, and blur it
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (21, 21), 0)

  # accumulate the weighted average between the current frame and
  # previous frames, then compute the difference between the current
  # frame and running average
  cv2.accumulateWeighted(gray, avg, 0.5)
  frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

  # threshold the delta image, dilate the thresholded image to fill
  # in holes, then find contours on thresholded image
  thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
    cv2.THRESH_BINARY)[1]
  thresh = cv2.dilate(thresh, None, iterations=2)
  (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
 
  maxArea = 0

  #pdb.set_trace()
  centroid_x = 0
  centroid_y = 0

  # loop over the contours
  for c in cnts:
    # if the contour is too small, ignore it
    if cv2.contourArea(c) < conf["min_area"]:
      centroid_x = 0
      centroid_y = 0
      continue

 
    # compute the bounding box for the contour, draw it on the frame,
    # and update the text
    (x, y, w, h) = cv2.boundingRect(c)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    text = "Occupied"
    #GPIO.output(ledPin, True)    

    # find the centroid of the largest 
    if maxArea < cv2.contourArea(c): 
      maxArea = cv2.contourArea(c)
      M = cv2.moments(c)
      centroid_x = int(M['m10']/M['m00'])
      centroid_y = int(M['m01']/M['m00'])
      # Draw a green box around largest moving object
      cv2.circle(frame, (centroid_x, centroid_y), 5, (0,0,255), -1)
 
  # draw the text and timestamp on the frame
  ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
  cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
  cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
    0.35, (0, 0, 255), 1)

  return [frame, text, avg, centroid_x, centroid_y]
