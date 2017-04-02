import time
from easy_driver_v4p4 import *

class HeadStepper:
  
  def __init__(self, dirPin, stepPin, enablePin, ms1Pin, ms2Pin):
    delay_time = 20
    self.motor = easy_driver_v4p4(stepPin, dirPin, enablePin, ms1Pin, ms2Pin, delay_time)

  def test_movement(self):
    #Go forward 
    self.motor.goforward()              # Set the direction
    self.motor.take_steps(4000, MIN_DELAY)    # Iterate for 4000 microsteps

    #Go backwared
    self.motor.gobackard()              # Set the direction
    self.take_steps(4000, MIN_DELAY)    # Iterate for 4000 microsteps

#  def center_on_moving(self):
#    # Center the camera x position onto the centroid of the moving body
