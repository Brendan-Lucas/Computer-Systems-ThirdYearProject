#============================================================================================
# virtualDoorManager.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
#--------------------------------------------------------------------------------------------
#
# GUI Widget to ease initialization of Virtual Door Simulator. 
# NOTE: Code is deprecated. Not part of final version
#
#============================================================================================
# Imports
import threading
from tkinter import *
import socket

#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class VirtualDoorManager(Frame):  
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self, master=None):
        Frame.__init__(self, master, bg="white")
        self.master.wm_title("Phantom Lock - Virtual Door Manager")
        self.master.iconbitmap(r'images/icon.ico')
        self.master.resizable(False,False)
        self.grid()   
        # Set Labels
        self.HomeID = Label(self, text = "HomeID"  , bg="white", width=8).grid(row=0,column=0,sticky=W+E+N+S)
        self.DoorID = Label(self, text = "DoorID"  , bg="white", width=8).grid(row=0,column=1,sticky=W+E+N+S)
        self.Type   = Label(self, text = "Type"    , bg="white", width=8, relief="flat", borderwidth="1").grid(row=0,column=2,sticky=W+E+N+S)
        self.Owner  = Label(self, text = "Owners"  , bg="white", width=8, relief="flat", borderwidth="1").grid(row=0,column=3,sticky=W+E+N+S)
        self.Code   = Label(self, text = "Password", bg="white", width=8, relief="flat", borderwidth="1").grid(row=0,column=4,sticky=W+E+N+S)

        self.output = []

        self.HomeIDs = []
        self.DoorIDs = []
        self.Types   = []
        self.Owners  = []
        self.Codes   = []
        self.Buttons = []
        i = 0
        while i < 8:
            self.HomeIDs.append(Entry (self, width=3  , relief="groove", borderwidth="1"))
            self.DoorIDs.append(Entry (self, width=3  , relief="groove", borderwidth="1"))
            self.Types  .append(Label (self, width=5  , relief="sunken", borderwidth="1"))
            self.Owners .append(Label (self, width=20 , relief="sunken", borderwidth="1", anchor="w"))
            self.Codes  .append(Label (self, width=8  , relief="sunken", borderwidth="1")) 
            self.Buttons.append(Button(self, width=3  , relief="flat"  , borderwidth="1", text="C", bg="white",))
            self.HomeIDs[i].grid(row=i+1,column=0,sticky=W+E+N+S)
            self.DoorIDs[i].grid(row=i+1,column=1,sticky=W+E+N+S)
            self.Types  [i].grid(row=i+1,column=2,sticky=W+E+N+S)
            self.Owners [i].grid(row=i+1,column=3,sticky=W+E+N+S)
            self.Codes  [i].grid(row=i+1,column=4,sticky=W+E+N+S)
            self.Buttons[i].grid(row=i+1,column=5,sticky=W+E+N+S)
            i+=1
        
        self.Buttons[0]["command"] = lambda: self.check(0)
        self.Buttons[1]["command"] = lambda: self.check(1)
        self.Buttons[2]["command"] = lambda: self.check(2)
        self.Buttons[3]["command"] = lambda: self.check(3)
        self.Buttons[4]["command"] = lambda: self.check(4)
        self.Buttons[5]["command"] = lambda: self.check(5)
        self.Buttons[6]["command"] = lambda: self.check(6)
        self.Buttons[7]["command"] = lambda: self.check(7)

        self.Cancel = Button(self, command=master.quit, pady=3, bg="white", width=10, text="Cancel", borderwidth="1")
        self.Cancel.grid(row=9,column=3, sticky=E)
        self.Okay   = Button(self, command=self.commit, pady=3, bg="white", width=10, text="OK", borderwidth="1")
        self.Okay.grid(row=9,column=4, sticky=W)
        self.Okay.configure(state='disabled')

    # Exit program
    def commit(self):
        i=0
        while i<8:
            if self.Types[i]["bg"] == "#b5e627":
                entry = []
                entry.append(int(self.HomeIDs[i].get()))
                entry.append(int(self.DoorIDs[i].get()))
                entry.append(self.Types [i]["text"])
                entry.append(self.Owners[i]["text"])
                entry.append(self.Codes [i]["text"])
                self.output.append(entry) 
            i+=1
        self.master.quit()

    #Confirm existance of door with server
    def check(self, index):    
        try:
            HomeID = int(self.HomeIDs[index].get())
            DoorID = int(self.DoorIDs[index].get())
        except ValueError: return
        if HomeID<0 or DoorID<0 or HomeID>255 or DoorID>255:
            self.Owners[index]["text"] = "Invalid DoorID/HomeID"
            self.Types [index]["text"] = ""
            self.Codes [index]["text"] = ""
            self.Types [index]["bg"]   = "red"
            self.Owners[index]["bg"]   = "red"
            self.Codes [index]["bg"]   = "red"
            return
        # Where to Send and Receive
        SERVER_ADDRESS  = '127.0.0.1' ; SERVER_PORT  = 1400
        RECEIVE_ADDRESS = '127.0.0.1' ; RECEIVE_PORT = 1400+10*HomeID+DoorID
        # Socket Setup
        SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        RECEIVE = (RECEIVE_ADDRESS, RECEIVE_PORT)
        SOCKET.bind(RECEIVE)
        # Message to send
        toSend = bytes([HomeID&0xFF, DoorID&0xFF, 0x05 ])
        SOCKET.sendto(toSend, (SERVER_ADDRESS, SERVER_PORT))
        # Wait for reponse
        response, address = SOCKET.recvfrom(RECEIVE_PORT);
        opcode = response[2]-0x30
        answer = response[3]-0x30
        if opcode==0x05 and answer==0x00:
            response = response[4:].decode('utf-8').split(';')
            self.HomeIDs[index].configure(state='disabled')
            self.DoorIDs[index].configure(state='disabled')
            self.Types  [index]["text"] = response[0]
            self.Owners [index]["text"] = response[1]
            self.Codes  [index]["text"] = response[2]
            self.Types  [index]["bg"]   = "#b5e627"
            self.Owners [index]["bg"]   = "#b5e627"
            self.Codes  [index]["bg"]   = "#b5e627"
            self.Okay.configure(state='active')
        else:
            self.Owners[index]["text"] = "Not Found"
            self.Types [index]["text"] = ""
            self.Codes [index]["text"] = ""
            self.Types [index]["bg"]   = "red"
            self.Owners[index]["bg"]   = "red"
            self.Codes [index]["bg"]   = "red"
