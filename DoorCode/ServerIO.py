#============================================================================================
# ServerIO.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
# 20/02/17
#--------------------------------------------------------------------------------------------
#
# Collection of IO functions for communication with Phantom Lock Server
#
#============================================================================================
#Imports
import time
import socket

#============================================================================================
# Opcodes
PASSWORD_OPCODE = 0x00
PICTURE_OPCODE  = 0x01
STATE_OPCODE    = 0x03

#============================================================================================
# Constants
SECURED         = 0x00
UNSECURED       = 0xFF

#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class ServerIO():
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self, homeID, doorID):        # Initialize servers and ports
        # Set Door Info
        self.HOME_ID = int(homeID)
        self.DOOR_ID = int(doorID)
        # Set Server Location
        self.SERVER_ADDRESS = '127.0.0.1'#'10.0.0.31'
        self.SERVER_PORT    = 1400
        # Set Receiving location
        self.DOOR_ADDRESS   = '127.0.0.1'#'10.0.0.20'
        self.DOOR_PORT      = 1400+10*int(homeID)+int(doorID)
        # Initalize Socket
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.RECEIVE = (self.DOOR_ADDRESS, self.DOOR_PORT)
        self.SOCKET.bind(self.RECEIVE)

    #===============================================================
    # sendPassword()
    #---------------------------------------------------------------
    # Send a password to the server
    # return: None
    #---------------------------------------------------------------
    def sendPassword(self, password):
        # Initalize message as bytes
        toSend = bytes([
            self.HOME_ID&0xFF, 
            self.DOOR_ID&0xFF, 
            PASSWORD_OPCODE,
            (ord(password[0]))&0xFF, 
            (ord(password[1]))&0xFF, 
            (ord(password[2]))&0xFF,
            (ord(password[3]))&0xFF
        ])
        self.send(toSend)
        return 

    #===============================================================
    # sendPicture()
    #---------------------------------------------------------------
    # Initialize a picture transfer to server
    # return: None
    #---------------------------------------------------------------
    def sendPicture(self):
        # Initalize message as bytes
        toSend = bytes([
            self.HOME_ID&0xFF, 
            self.DOOR_ID&0xFF, 
            PICTURE_OPCODE 
        ])
        self.send(toSend)
        return 

    #===============================================================
    # sendState()
    #---------------------------------------------------------------
    # Send the current door state to server
    # return: None
    #---------------------------------------------------------------
    def sendState(self, state):
        # Door is Secured
        if state is True: 
            toSend = bytes([ 
                self.HOME_ID&0xFF, 
                self.DOOR_ID&0xFF,
                STATE_OPCODE, 
                SECURED 
            ])
        # Door is Unsecured
        else: 
            toSend = bytes([ 
                self.HOME_ID&0xFF, 
                self.DOOR_ID&0xFF,
                STATE_OPCODE, 
                UNSECURED 
            ])
        self.send(toSend)
        return          

    #===============================================================
    # send_address()
    #---------------------------------------------------------------
    # Sends a message to specified port and address
    # return: None
    #---------------------------------------------------------------
    def send_address(self, message, IP, PORT):
        self.SOCKET.sendto(message, (IP,PORT))

    #===============================================================
    # send()
    #---------------------------------------------------------------
    # Sends a message to the servers default port and address
    # return: None
    #---------------------------------------------------------------
    def send(self, message):
        self.SOCKET.sendto(message, (self.SERVER_ADDRESS, self.SERVER_PORT))
    
    #===============================================================
    # receive_address()
    #---------------------------------------------------------------
    # Receives a message from specified port and address
    # return: msg
    #---------------------------------------------------------------
    def receive_address(self):
        return self.SOCKET.recvfrom(self.DOOR_PORT);
    
    #===============================================================
    # send()
    #---------------------------------------------------------------
    # Receives a message from the servers default port and address
    # return: msg
    #---------------------------------------------------------------
    def receive(self):
        buff, address = self.SOCKET.recvfrom(self.DOOR_PORT);
        return buff

#============================================================================================
