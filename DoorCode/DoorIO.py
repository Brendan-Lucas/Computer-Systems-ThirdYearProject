#===============================================================
# DoorIO.py
#---------------------------------------------------------------
# Collection of IO functions for a door using the 
# GertBoard, PiFace, or Virtual Interface
#===============================================================
#imports
import time
#===============================================================
class VirtualDoorIO():
#===============================================================
    #===============================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self):
        # Buffers for interacting with GUI Interface
        self.LOCK_BUFFER   = False
        self.DOOR_BUFFER   = False
        self.KEYPAD_BUFFER = False
        self.CAMERA_BUFFER = False
        self.SOUND_BUFFER    = False
        self.LCD_BUFFER    = ""
        
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
    # setUnocked()
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
    # getKeyPressed()
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
            time.sleep(0.05) #wait fro response from camera.
        picture = self.CAMERA_BUFFER
        with open(picture, "rb") as imageFile:
            f = imageFile.read()
            picture = bytearray(f)
        self.CAMERA_BUFFER = False
        return picture

#===============================================================
class HardwareDoorIO():
#===============================================================
    #===============================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self):
        # Buffers for interacting with GUI Interface
        self.LOCK_BUFFER   = False
        self.DOOR_BUFFER   = False
        self.KEYPAD_BUFFER = False
        self.CAMERA_BUFFER = False
        self.SOUND_BUFFER    = False
        self.LCD_BUFFER    = ""
        
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
    # setUnocked()
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
    # getKeyPressed()
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
            time.sleep(0.05) #wait fro response from camera.
        picture = self.CAMERA_BUFFER
        with open(picture, "rb") as imageFile:
            f = imageFile.read()
            picture = bytearray(f)
        self.CAMERA_BUFFER = False
        return picture

