# RPi_Head_Tracker
Motion detection with stepper enabled tracking of a camera

# Setting up anaconda virtual env
Python version needs to be 3.5 to work with opencv3. Python 3.6 was not compatible. If you wanted to set up python 2.7 the command would be `conda install -c menpo opencv`. 
RPIO is a modified version of RPi library. Has functionality to handle interrupts and PWM.
```
conda create --name opencv python=3.5
conda install -c menpo opencv3
conda install ipython
pip install imutils
pip install RPIO
```

# Libraries Used
motion_detection
head_stepper

# Scripts
## test_mac.py
Runs object detection on a mac computer, this should also work on a linux setup. Not tested in windows env. Does not use GPIO libraries. Used for development and debugging.
