#============================================================================================
# Door.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
# 20/02/17
#--------------------------------------------------------------------------------------------
#
# Main operating logic for Phantom Lock
#
#============================================================================================
# Imports
import time
import threading
from DoorIO   import *
from ServerIO import *

#============================================================================================
# Opcodes
PASSWORD_OPCODE  =  0x00
PIC_OPCODE       =  0x01
STATUS_OPCODE    =  0x02
REQUEST_OPCODE   =  0x03
PIC_ACK_OPCODE   = [0x00,0x04,0x00,0x00] # Expected Acknowledgement opcode for pic transfers
PIC_TRANS_OPCODE = [0x00,0x02]           # Transfer opcode for pic transfers

#============================================================================================
# Constants
ACCEPTED     = 0x00
REJECTED     = 0xFF
PASSWORD_LEN = 4
MAX_ID       = 256

ENTER_KEY  = "#"
DELETE_KEY = "D"
PIC_KEY    = "*"

#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class Door:
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self, HomeID, DoorID, Type):
        # Check if HomeID is in valid range        
        if int(HomeID) < 0 or MAX_ID < int(HomeID):       
            print("Error: Invalid Home ID Range"); exit(1)
        # Check if DoorID is in valid range
        if int(DoorID) < 0 or MAX_ID < int(DoorID):        
            print("Error: Invalid Door ID Range"); exit(1)
        # Check if Door Type is valid
        if Type != "Front" and Type != "Back":        
            print("Error: Invalid Door Type"); exit(1)
        # Door Instance Info
        self.HOME_ID   = int(HomeID)
        self.DOOR_ID   = int(DoorID)
        self.DOOR_TYPE = Type
        # Door IO Modules
        self.SERVER_IO = ServerIO(self.HOME_ID, self.DOOR_ID)
        self.DOOR_IO   = None  # Will be initalized at runtime
        
        # Door State Variables
        self.secured      = False # Internal State of Door     
        self.lcdText      = ""    # Text Currently on LCD 
        self.keypadActive = 0     # Cycles before clearing keypad
        # Picture Transfer Variables        
        self.picToSend      = None
        self.picPacketCount = None
            
    #===============================================================
    # runVirtual()
    #---------------------------------------------------------------
    # Run a door on a virtual interface
    #---------------------------------------------------------------
    def runVirtual(self):
        self.DOOR_IO = VirtualDoorIO()
        self.run()
    
    #===============================================================
    # runHardware()
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
        # Ensure DOOR_IO is initalized        
        if self.DOOR_IO is None:       
            print("Error: DOOR_IO module undefined"); exit(1)
        # Thread to process messages from server
        self.pollMessage_thread = threading.Thread(target=self.pollMessageThread,args=())
        self.pollMessage_thread.daemon = True # run in background
        self.pollMessage_thread.start()
        # Thread to monitor door State
        pollDoor_thread = threading.Thread(target=self.pollDoorThread,args=())
        pollDoor_thread.daemon = True # run in background
        pollDoor_thread.start()
        # Check keypad if door is a front door
        if self.DOOR_TYPE == "Front":
            pollKeypad_thread = threading.Thread(target=self.pollKeypadThread,args=())
            pollKeypad_thread.daemon = True # run in background
            pollKeypad_thread.start()
        #Run threads and Loop Forever
        while True: time.sleep(1) 

    #===============================================================
    # pollMessageThread())
    #---------------------------------------------------------------
    # Thread to poll messages sent from server 
    #---------------------------------------------------------------
    def pollMessageThread(self):
        FREQUENCY = 100 
        delay = 1/FREQUENCY
        # Run Forever, running pollMessage() at the indicated frequency
        while True:
            self.pollMessage()
            time.sleep(delay)

    #===============================================================
    # pollMessage())
    #---------------------------------------------------------------
    # Respond to messages received from server
    #---------------------------------------------------------------
    def pollMessage(self): 
        # Wait to receive a message
        message, address = self.SERVER_IO.receive_address()
        # Parse Message Opode
        home   = message[0]
        door   = message[1]
        opcode = message[2]
        #-----------------------------------------------------     
        # Only answer message for correct door      
        if self.HOME_ID == home and self.DOOR_ID == door: 
            # Handle a response from a passcode request
            if opcode == PASSWORD_OPCODE: 
                status       = message[3]
                requestDelay = 1 
                if status == ACCEPTED:
                    self.printLCD("PASSCODE ACCEPTED")
                    # Handle Reponse according to state of door and lock
                    # Unlock Door Operation
                    if self.DOOR_IO.isLocked() is True and self.DOOR_IO.isOpen() is False:
                        self.DOOR_IO.setUnlocked()
                        time.sleep(requestDelay)
                        self.printLCD("DOOR UNLOCKED")
                    # Lock Door Operation
                    elif self.DOOR_IO.isLocked() is False and self.DOOR_IO.isOpen() is False:
                        self.DOOR_IO.setLocked()
                        time.sleep(requestDelay)
                        self.printLCD("DOOR LOCKED")
                    # Error Case - Door was left Open
                    else:
                        time.sleep(requestDelay)
                        self.printLCD("ERROR - DOOR OPEN")
                else:
                    self.printLCD("PASSCODE REJECTED")
            #-----------------------------------------------------
            # Handle a response from a picture request
            elif opcode == PIC_OPCODE: 
                status       = message[3]
                requestDelay = 1 
                if message[3] == ACCEPTED:
                    self.printLCD("REQUEST ACCEPTED")
                    # Unlock Door
                    if self.DOOR_IO.isLocked() is True and self.DOOR_IO.isOpen() is False:
                        self.DOOR_IO.setUnlocked()
                        time.sleep(1)
                        self.printLCD("DOOR UNLOCKED")
                else:
                    self.printLCD("REQUEST REJECTED")
            #-----------------------------------------------------
            # Handle a lock unlock/request from user via server
            elif opcode == REQUEST_OPCODE: 
                requestDelay = 1    
                if self.DOOR_IO.isLocked() is True:
                    self.DOOR_IO.setUnlocked()
                    time.sleep(requestDelay)
                    self.printLCD("DOOR UNLOCKED")
                else:
                    self.DOOR_IO.setLocked()
                    time.sleep(requestDelay)
                    self.printLCD("DOOR LOCKED")
            return
        #-----------------------------------------------------     
        # Handle Picture Transfer Operation    
        else:
            # Check Specialized OpCode Format for picture transfer
            if message[0]==PIC_ACK_OPCODE[0] and message[1]==PIC_ACK_OPCODE[1] and self.picToSend is not None:# and message[2]==PIC_ACK_OPCODE[2] and message[3]==PIC_ACK_OPCODE[3]:
                if self.picPacketCount is None: #reset picPacketCount for new request
                    self.picPacketCount = 1
                # Generate Transfer Opcode
                toSend = bytearray()
                toSend.append(PIC_TRANS_OPCODE[0])
                toSend.append(PIC_TRANS_OPCODE[1])
                toSend.append((self.picPacketCount//256)&0xFF) # Seperate packetCount into 2 Bytes
                toSend.append((self.picPacketCount %256)&0xFF)
                # Send next 1024 bytes
                if len(self.picToSend) > 1024:
                    for i in range(0,1024):
                        toSend.append(self.picToSend[i]&0xFF)
                    self.SERVER_IO.send_address(toSend, address[0], address[1])
                    
                    self.picToSend = self.picToSend[1024:] #cut sent bits from packet
                    self.picPacketCount+=1
                    return
                # Send rest of photo
                else:
                    # Fill with rest of photo
                    for i in range(0,len(self.picToSend)):
                        toSend.append(self.picToSend[i]&0xFF)
                    for i in range(0,5): toSend.append(0x00)
                    self.SERVER_IO.send_address(toSend, address[0], address[1])
                    # Reset
                    self.picPacketCount=None                        
                    self.picToSend = None
                    return
                return  

    #===============================================================
    # pollDoorThread()
    #---------------------------------------------------------------
    # Thread to poll activity from keypad
    #---------------------------------------------------------------
    def pollDoorThread(self):
        FREQUENCY = 20 
        delay = 1/FREQUENCY
        # Run Forever, running pollDoor() at the indicated frequency   
        while True:
            self.pollDoor()
            time.sleep(delay)

    #===============================================================
    # pollDoor()
    #---------------------------------------------------------------
    # Process input from the keypad
    #---------------------------------------------------------------
    def pollDoor(self): 
        # Door is secured. Only check the lock state
        if self.secured is True:
            lockReading = self.DOOR_IO.isLocked()
            if lockReading is False:
                self.secured = False
                self.SERVER_IO.sendState(self.secured) # Update Server Database with new state
        # Door is unsecured. Poll lock and door State
        else:           
            lockReading = self.DOOR_IO.isLocked()
            doorReading = self.DOOR_IO.isOpen()
            if lockReading is True and doorReading is False:
                self.secured = True
                self.SERVER_IO.sendState(self.secured) # Update Server Database with new state
        
    #===============================================================
    # pollKeypadThread()
    #---------------------------------------------------------------
    # Thread to poll activity from keypad
    #---------------------------------------------------------------
    def pollKeypadThread(self):
        FREQUENCY = 20 
        delay = 1/FREQUENCY
        # Run Forever, running pollMessage() at the indicated frequency        
        while True:
            self.pollKeypad()
            time.sleep(delay)

    #===============================================================
    # pollKeypad()
    #---------------------------------------------------------------
    # Check if keypad has been pressed
    #---------------------------------------------------------------
    def pollKeypad(self):
        keyReading = self.DOOR_IO.isKeyPressed()
        requestDelay = 0.25
        if keyReading is not False:
            self.keypadActive = 100 # Set LCD active timer for 5 seconds 
            # Enter/Clear Button Pressed
            if keyReading == ENTER_KEY:
                self.requestPassword(self.LCD)
            # Picture Request Button Pressed
            elif keyReading == PIC_KEY:
                self.requestPicture()
            # Backspace
            elif keyReading == DELETE_KEY: 
                self.backspaceLCD()
            # Keycode pressed
            else:
                # If LCD is full or empty, overwrite
                if len(self.LCD) == 0 or len(self.LCD) > PASSWORD_LEN:
                    self.printLCD(keyReading)
                # Otherwise append to existing values
                elif len(self.LCD) < PASSWORD_LEN:
                    self.appendLCD(keyReading)
            # Delay if a key has been pressed
            time.sleep(requestDelay)
        # Clear LCD if inactive
        if    self.keypadActive <= 0: self.clearLCD()
        else: self.keypadActive -= 1

    #===============================================================
    # requestPassword()
    #---------------------------------------------------------------
    # Request access to door via password
    #---------------------------------------------------------------
    def requestPassword(self, password):
        requestDelay = 3
        # Only Send a Correct Length Password
        if len(password) is PASSWORD_LEN:
            self.SERVER_IO.sendPassword(password)
            time.sleep(requestDelay)     
        else:
            self.printLCD("INVALID FORMAT")
            time.sleep(requestDelay)     
            self.clearLCD()
    
    #===============================================================
    # requestPicture()
    #---------------------------------------------------------------
    # Request access to door via picture
    #---------------------------------------------------------------
    def requestPicture(self):
        #Initialize     
        requestDelay = 2        
        self.printLCD("TAKING PICTURE")
        time.sleep(requestDelay)
        #Get Picture
        self.picToSend = self.DOOR_IO.takePicture()
        #Initiate Request
        self.SERVER_IO.sendPicture()
        self.printLCD("REQUEST SENT")
        time.sleep(requestDelay)

    #===============================================================
    # LCD Utility Functions 
    #---------------------------------------------------------------
    # Clear LCD and display Message    
    def printLCD(self, message):
        self.LCD = message
        self.DOOR_IO.displayLCD(self.LCD)
    #---------------------------------------------------------------
    # Append Message to existing message
    def appendLCD(self, message):
        self.LCD += message
        self.DOOR_IO.displayLCD(self.LCD)
    #---------------------------------------------------------------
    # Remove last character from LCD
    def backspaceLCD(self):
        self.LCD = self.LCD[:-1]
        self.DOOR_IO.displayLCD(self.LCD)
    #---------------------------------------------------------------
    # Remove all characters from LCD
    def clearLCD(self):
        self.printLCD("")

#========================================================================
