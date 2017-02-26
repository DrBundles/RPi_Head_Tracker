import time
from easy_driver_v4p4 import *

dirPin = 23
stepPin = 24
enablePin = 25
ms1Pin = 19
ms2Pin = 26

motor = easy_driver_v4p4(stepPin, dirPin, enablePin, ms1Pin, ms2Pin)

while True:
  #Go forward 
  motor.goforward()              # Set the direction
  motor.take_steps(4000, MIN_DELAY)    # Iterate for 4000 microsteps

  #Go backwared
  motor.gobackard()              # Set the direction
  take_steps(4000, MIN_DELAY)    # Iterate for 4000 microsteps

  time.sleep(1)
