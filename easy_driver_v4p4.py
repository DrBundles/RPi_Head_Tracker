import RPi.GPIO as GPIO
import time

class easy_driver_v4p4:
 
  def __init__(self, step_pin, dir_pin, enable_pin, ms1_pin, ms2_pin, delay_time):
    # setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(step_pin, GPIO.OUT)
    GPIO.output(step_pin, False)
    GPIO.setup(dir_pin, GPIO.OUT)
    GPIO.output(dir_pin, False)
    GPIO.setup(enable_pin, GPIO.OUT)
    GPIO.output(enable_pin, False)
    GPIO.setup(ms1_pin, GPIO.OUT)
    GPIO.output(ms1_pin, False)
    GPIO.setup(ms2_pin, GPIO.OUT)
    GPIO.output(ms2_pin, False)
    self.delayTime = delay_time

  def goforward():
    GPIO.output(dir_pin, True)
    #time.sleep(0.01)
    
  def gobackward():
    GPIO.output(dir_pin, False)
    #time.sleep(0.01)
    
  def take_steps(howManySteps, delayTime):
    GPIO.output(step_pin,False)
    GPIO.output(step_pin,True)
    time.sleep(delayTime)



