#========================================================================
# Door.py
#------------------------------------------------------------------------
# Main Operation of a Phantom Lock door
# Patrick Perron
# 20/02/17
#
#========================================================================
#imports
import time
import threading
from DoorIO   import *
from ServerIO import *

#========================================================================
# class definition
#------------------------------------------------------------------------
class Door:
    #===============================================================
    # Initializer
    #---------------------------------------------------------------
    def __init__(self, HomeID, DoorID, Type):
        # Check if HomeID is in valid range        
        if int(HomeID) < 0 or 255 < int(HomeID):       
            print("Error: Invalid Home ID Range"); exit(1)
        # Check if DoorID is in valid range
        if int(DoorID) < 0 or 255 < int(DoorID):        
            print("Error: Invalid Door ID Range"); exit(1)
        # Check if DoorID is in valid range
        if Type != "Front" and Type != "Back":        
            print("Error: Invalid Door Type"); exit(1)

        # Instance Variables for Door
        self.HOME_ID   = int(HomeID)
        self.DOOR_ID   = int(DoorID)
        self.SERVER_IO = ServerIO(self.HOME_ID, self.DOOR_ID) # Module that communicates with server
        self.DOOR_IO   = None  # Module that connects hardware/virtual interacted
        self.SECURED   = False # Internal State of Door     
        self.LCD       = ""    # Text Currently on LCD 
        self.active    = 0 # Value to inidcate how active the keypad is
        self.DOOR_TYPE = Type
            
    #===============================================================
    # runVirtual()
    #---------------------------------------------------------------
    # Run a door on a virtual interface
    #---------------------------------------------------------------
    def runVirtual(self):
        self.DOOR_IO = VirtualDoorIO()
        self.run()
    
    #===============================================================
    # runVirtual()
    #---------------------------------------------------------------
    # Run a door on a hardware interface
    #---------------------------------------------------------------
    def runHardware(self):
        self.DOOR_IO = HardwareDoorIO()
        self.run()

    #===============================================================
    # run()
    #---------------------------------------------------------------
    # Run the main loop of a Phantom Lock door
    #---------------------------------------------------------------
    def run(self): 
        # It's Time to Run!!
        # Ensure DOOR_IO is initalized        
        if self.DOOR_IO is None:       
            print("Error: DOOR_IO module undefined"); exit(1)
        
        # Thread to receive message from server
        pollMessage_thread = threading.Thread(target=self.pollMessageThread,args=())
        pollMessage_thread.daemon = True # run in background
        pollMessage_thread.start()

        # Thread to check Door State
        pollDoor_thread = threading.Thread(target=self.pollDoorThread,args=())
        pollDoor_thread.daemon = True # run in background
        pollDoor_thread.start()

        # Check keypad if door is a front Door
        if self.DOOR_TYPE == "Front":
            pollKeypad_thread = threading.Thread(target=self.pollKeypadThread,args=())
            pollKeypad_thread.daemon = True # run in background
            pollKeypad_thread.start()
        
        #Run threads
        while True:
            time.sleep(10)
    #===============================================================
    # pollMessage())
    #---------------------------------------------------------------
    # Check if state of door has changed
    #---------------------------------------------------------------
    def pollMessageThread(self): 
        while True and not False:
            self.pollMessage()
            time.sleep(0.01)
    def pollMessage(self): 
        #Receive Message
        message = self.SERVER_IO.receive()
        #Retrieve  Opcode
        home = message[0]
        door = message[1]
        opcode = message[2]
        # Response From Passcode
        if opcode == 0x00: 
            if message[3] == 0x00:
                self.printLCD("PASSCODE ACCEPTED")
                # Unlock Door
                if self.DOOR_IO.isLocked() is True and self.DOOR_IO.isOpen() is False:
                    self.DOOR_IO.setUnlocked()
                    time.sleep(1)
                    self.printLCD("DOOR UNLOCKED")
                # Lock Door
                elif self.DOOR_IO.isLocked() is False and self.DOOR_IO.isOpen() is False:
                    self.DOOR_IO.setLocked()
                    time.sleep(1)
                    self.printLCD("DOOR LOCKED")
                # Door Left Open
                else:
                    time.sleep(1)
                    self.printLCD("ERROR - DOOR OPEN")
            else:
                self.printLCD("PASSCODE REJECTED")
        
        # Response from Picture
        elif opcode == 0x01: 
            if message[3] == 0x00:
                self.printLCD("REQUEST ACCEPTED")
                # Unlock Door
                if self.DOOR_IO.isLocked() is True and self.DOOR_IO.isOpen() is False:
                    self.DOOR_IO.setUnlocked()
                    time.sleep(1)
                    self.printLCD("DOOR UNLOCKED")
            else:
                self.printLCD("REQUEST REJECTED")

        # TODO: Lock or Unlock Request
        elif opcode == 0x03: 
            if message[3] == 0x00:
                self.printLCD("REQUEST ACCEPTED")
                # Unlock Door
                if self.DOOR_IO.isLocked() is True and self.DOOR_IO.isOpen() is False:
                    self.DOOR_IO.setUnlocked()
                    time.sleep(1)
                    self.printLCD("DOOR UNLOCKED")
            else:
                self.printLCD("REQUEST REJECTED")

    #===============================================================
    # pollDoor()
    #---------------------------------------------------------------
    # Check if state of door has changed
    #---------------------------------------------------------------
    def pollDoorThread(self):
        while True:
            self.pollDoor()
            time.sleep(0.25) #4 times per second
    def pollDoor(self): 
        # Door is secured. Only check the lock state
        if self.SECURED is True:
            lockReading = self.DOOR_IO.isLocked()
            if lockReading is False:
                self.SECURED = False
                self.SERVER_IO.sendState(self.SECURED) #Update Server with new state
        # Door is unsecured. Poll lock and door State
        else:           
            lockReading = self.DOOR_IO.isLocked()
            doorReading = self.DOOR_IO.isOpen()
            if lockReading is True and doorReading is False:
                self.SECURED = True
                self.SERVER_IO.sendState(self.SECURED) #Update Server with new state
        
    #===============================================================
    # pollKeypad()
    #---------------------------------------------------------------
    # Check if keypad has been pressed
    #---------------------------------------------------------------
    def pollKeypadThread(self):
        while True:
            self.pollKeypad()
            time.sleep(0.05) #4 times per second
    def pollKeypad(self):
        keyReading = self.DOOR_IO.isKeyPressed()
        if keyReading is not False:
            self.active = 100 # Set LCD active timer for 5 seconds 
            # Enter/Clear Button Pressed
            if keyReading == "#":
                self.requestPassword(self.LCD)
            # Picture Request Button Pressed
            elif keyReading == "*":
                self.requestPicture()
            # Backspace
            elif keyReading == "D": 
                self.backspaceLCD()
            # Keycode pressed
            else:
                if len(self.LCD) == 0 or len(self.LCD) > 4:
                    self.printLCD(keyReading)
                elif len(self.LCD) < 4:
                    self.appendLCD(keyReading)
            # Delay if a key has been pressed
            time.sleep(0.25)
        # Clear LCD if inactive
        if    self.active <= 0: self.clearLCD()
        else: self.active -= 1

    #===============================================================
    # requestPassword()
    #---------------------------------------------------------------
    # Request access to door via password
    #---------------------------------------------------------------
    def requestPassword(self, password):
        if len(password) is 4:
            self.SERVER_IO.sendPassword(password)
            time.sleep(3)     
    
    #===============================================================
    # requestPicture()
    #---------------------------------------------------------------
    # Request access to door via picture
    #---------------------------------------------------------------
    def requestPicture(self):
        self.printLCD("TAKING PICTURE")
        time.sleep(1)
        picture = self.DOOR_IO.takePicture()
        self.SERVER_IO.sendPicture(picture) # MAKE INTO THREAD
        self.printLCD("REQUEST SENT")
        time.sleep(3)

    #===============================================================
    # LCD Functions 
    #---------------------------------------------------------------
    def printLCD(self, message):
        self.LCD = message
        self.DOOR_IO.displayLCD(self.LCD)
    def appendLCD(self, message):
        self.LCD += message
        self.DOOR_IO.displayLCD(self.LCD)
    def backspaceLCD(self):
        self.LCD = self.LCD[:-1]
        self.DOOR_IO.displayLCD(self.LCD)
    def clearLCD(self):
        self.printLCD("")

#========================================================================
