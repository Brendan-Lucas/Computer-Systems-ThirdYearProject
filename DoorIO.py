import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep

class HardwareDoorIO():
    def __init__(self, type):
        # Variable to indicate hardware type
        if type == "Front": self.HW = "GertBoard"
        else: self.HW = "PiFace"

    #===============================================================
    # setLocked()
    #---------------------------------------------------------------
    # Set door to locked state.
    # return: True(successful), False(unsuccessful)
    #---------------------------------------------------------------
    def setLocked(self):
        # Only run if actual state is different than passed state
        if self.isLocked() is False:
            if(self.HW == "GertBoard"):
                pin_number=7
                time_Complete = 10 # to be changed
                
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(pin_number, GPIO.OUT)

                GPIO.output(pin_number, 1)
                time.sleep(time_Complete)
                GPIO.output(pin_number, 0)
                GPIO.cleanup()

        # Check if operation was successful
        if self.isLocked() is True:
            return True
        return False

    #===============================================================
    # setUnocked()
    #---------------------------------------------------------------
    # Set door to unlocked state.
    # return: True(successful), False(unsuccessful)
    #---------------------------------------------------------------
    def setUnlocked(self):
        # Only run if actual state is different than passed state
        if self.isLocked() is True:
             if(self.HW == "GertBoard"):
                pin_number=7
                time_Complete = 10 # to be changed
                
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(pin_number, GPIO.OUT)

                GPIO.output(pin_number, 1)
                time.sleep(time_Complete)
                GPIO.output(pin_number, 0)
                GPIO.cleanup()
                
        # Check if operation was successful
        if self.isLocked() is False: return True
        return False

    #===============================================================
    # isLocked()
    #---------------------------------------------------------------
    # Get the current state of the lock
    # return: True(Locked), False(Unlocked)
    #---------------------------------------------------------------
    def isLocked(self):     
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.IN, GPIO.PUD_UP)
        if not GPIO.input(12):
            return True  # Door Locked
        else:
            return False # Door Unlocked
    

    #===============================================================
    # isOpen()
    #---------------------------------------------------------------
    # Get the current state of the door
    # return: True(Open), False(Closed)
    #---------------------------------------------------------------
    def isOpen(self): 
        return False
    


    #===============================================================
    # displayLCD()
    #---------------------------------------------------------------
    # Display message on LCD
    #---------------------------------------------------------------
    def displayLCD(self, message):
        return

    #===============================================================
    # playSound()
    #---------------------------------------------------------------
    # Play sound on keypad panel speaker
    #---------------------------------------------------------------
    def playSound(self, sound):
        return

    #===============================================================
    # takePicture()
    #---------------------------------------------------------------
    # Take picture with camera
    # return: byte[](Picture taken), False(Error Occurred)
    #---------------------------------------------------------------
    def takePicture(self): 
        try:
            camera = PiCamera()
            camera.start_preview()
            sleep(5)

            camera.capture('/home/pi/Desktop/image.jpg')
            camera.stop_preview()
        except IOError:
            pass

#===============================================================
