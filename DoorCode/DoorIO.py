#============================================================================================
# DoorIO.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
# 20/02/17
#--------------------------------------------------------------------------------------------
#
# Collection of IO functions for a door using the GertBoard, PiFace, RPi or 
# Virtual Interface.
#
# Two classes: - VirtualDoorIO() : IO for a virtually simulated door
#              - HardwareDoorIO(): IO for a physically run door
#
#============================================================================================
# Imports
import time
import io

try:
    import RPi.GPIO as GPIO
    from picamera import PiCamera
except:
    print("Running Virtual")

import PIL
from PIL import Image

#============================================================================================
# Constants
PIC_SIZE = 128
PIC_NAME = "sample.jpg"

#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class VirtualDoorIO():
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self):
        # Create Buffers for interacting with GUI Interface
        self.LOCK_BUFFER   = False
        self.DOOR_BUFFER   = False
        self.KEYPAD_BUFFER = False
        self.CAMERA_BUFFER = False
        self.SOUND_BUFFER  = False
        self.LCD_BUFFER    = ""     #LCD initilaly blank
        
    #===============================================================
    # setLocked()
    #---------------------------------------------------------------
    # Set door to locked state.
    # return: True(successful), False(unsuccessful)
    #---------------------------------------------------------------
    def setLocked(self):
        # Only run if actual state is different than passed state
        if self.isLocked() is False:
            self.LOCK_BUFFER = True
        # Check if operation was successful
        if self.isLocked() is True: return True
        return False

    #===============================================================
    # setUnlocked()
    #---------------------------------------------------------------
    # Set door to unlocked state.
    # return: True(successful), False(unsuccessful)
    #---------------------------------------------------------------
    def setUnlocked(self):
        # Only run if actual state is different than passed state
        if self.isLocked() is True:
           self.LOCK_BUFFER = False
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
        return self.LOCK_BUFFER;

    #===============================================================
    # isOpen()
    #---------------------------------------------------------------
    # Get the current state of the door
    # return: True(Open), False(Closed)
    #---------------------------------------------------------------
    def isOpen(self):
        return self.DOOR_BUFFER;

    #===============================================================
    # isKeyPressed()
    #---------------------------------------------------------------
    # Check if key on keypad is pressed
    # return: char(key pressed), False(key not pressed)
    #---------------------------------------------------------------
    def isKeyPressed(self):
        message = self.KEYPAD_BUFFER
        self.KEYPAD_BUFFER = False
        return message

    #===============================================================
    # displayLCD()
    #---------------------------------------------------------------
    # Display message on LCD
    #---------------------------------------------------------------
    def displayLCD(self, message):
        self.LCD_BUFFER = message

    #===============================================================
    # playSound()
    #---------------------------------------------------------------
    # Play sound on keypad panel speaker
    #---------------------------------------------------------------
    def playSound(self, sound):
        self.SOUND_BUFFER = sound

    #===============================================================
    # takePicture()
    #---------------------------------------------------------------
    # Take picture with camera
    # return: byte[](Picture taken), False(Error Occurred)
    #---------------------------------------------------------------
    def takePicture(self):
        self.CAMERA_BUFFER = True
        while self.CAMERA_BUFFER is True:
            time.sleep(0.05) #wait for response from camera.
        picture = self.CAMERA_BUFFER # Get picture from buffer
        # Crop picture to 128x128
        picture = Image.open(picture)
        picture = picture.crop((420, 0, 1500, 1080)) # Cut to square image
        picture = picture.resize((PIC_SIZE, PIC_SIZE), PIL.Image.ANTIALIAS)
        picture.save(PIC_NAME)

        with open(PIC_NAME, "rb") as imageFile:
            f = imageFile.read()
            picByteArr = bytearray(f) 
        
        # Reset buffer and return byte array
        self.CAMERA_BUFFER = False
        return picByteArr

#============================================================================================
class HardwareDoorIO():
#============================================================================================
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
                GPIO.setmode(GPIO.BOARD)
                pin_number=7
                GPIO.setup(pin_number, GPIO.OUT)
                frequency_hertz= 50
                pwm= GPIO.PWM(pin_number, frequency_hertz)

                right_position=2.5
                middle_position = 5

                positionList= [middle_position, right_position, middle_position]
                ms_per_cycle= 700/frequency_hertz

                for position in positionList:
                    duty_cycle_percentage = position * 100 /ms_per_cycle
                    pwm.start(duty_cycle_percentage)
                    time.sleep(0.5)

                pwm.stop()
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
                GPIO.setmode(GPIO.BOARD)
                pin_number=7
                GPIO.setup(pin_number, GPIO.OUT)
                frequency_hertz= 50
                pwm= GPIO.PWM(pin_number, frequency_hertz)

                right_position=2.5
                middle_poristion = 7.5

                positionList= [middle_poristion, right_position]
                ms_per_cycle= 700/frequency_hertz

                for position in positionList:
                    duty_cycle_percentage = position * 100 /ms_per_cycle
                    pwm.start(duty_cycle_percentage)
                    time.sleep(0.5)

                pwm.stop()
                GPIO.cleanup()
            
                
        # Check if operation was successful
        if self.isLocked() is False: return True
        return False
    
    #===============================================================
    # isKeyPressed()
    #---------------------------------------------------------------
    # Check if key on keypad is pressed
    # return: char(key pressed), False(key not pressed)
    #---------------------------------------------------------------
    def isKeyPressed(self):
        return
    
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
