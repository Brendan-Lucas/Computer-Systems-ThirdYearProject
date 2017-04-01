#============================================================================================
# widget_lockpanel.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
#--------------------------------------------------------------------------------------------
#
# Handles input from Lock state
#
#============================================================================================
# Imports
import time
import threading
from tkinter import *
from winsound import *
from Door import Door
	
#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class LockPanel(Frame):
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self, master, door):
        Frame.__init__(self, master)
        # Set State Label
        self.DOOR = door #Pointer to door
        self.stateLabel = Label(self)
        self.stateLabel["text"] = "UNSECURED"
        self.stateLabel["fg"] = "black"
        self.stateLabel["width"] = "12"
        self.stateLabel["bg"] = "white"
        self.stateLabel["relief"] = "flat"
        self.stateLabel["borderwidth"] = "0"
        self.stateLabel["anchor"] = "center"
		# get Images
        self.locked   = PhotoImage(file="images/locked.png")
        self.unlocked = PhotoImage(file="images/unlocked.png")
        # Set Lock Button
        self.lockButton = Button(self,image=self.unlocked)
        self.lockButton.image = self.unlocked
        self.lockButton["command"] = lambda: self.toggle()
        self.lockButton["relief"] = "flat"
        self.lockButton["bg"] = "white"
        self.lockButton["activebackground"] = "white"
        self.lockButton["borderwidth"] = "0"
        self.lockButton["anchor"] = "center"
		# Place Images
        self.grid()
        self.lockButton.grid(row=0,column=1,sticky=W+E+N+S, ipadx=8)
        self.stateLabel.grid(row=1,column=1,sticky=W+E+N+S, ipadx=8)
	    # Launch Update Thread
        update_thread = threading.Thread(target=self.update,args=())
        update_thread.daemon = True
        update_thread.start()
        return 

    #===============================================================
    # update()
    #---------------------------------------------------------------
    # Update GUI with values in Buffers
    #---------------------------------------------------------------
    def update(self):
        # Initialize
        state = self.DOOR.secured
        lock  = self.DOOR.DOOR_IO.LOCK_BUFFER
        while True:
            if lock is not self.DOOR.DOOR_IO.LOCK_BUFFER:
                lock = self.DOOR.DOOR_IO.LOCK_BUFFER
                if lock is True:
                    threading.Thread(target=PlaySound,args=('sounds/sound_locked.wav', SND_FILENAME)).start()
                    self.lockButton.configure(image = self.locked)
                    self.lockButton.image = self.locked
                else:
                    threading.Thread(target=PlaySound,args=('sounds/sound_unlocked.wav', SND_FILENAME)).start()
                    self.lockButton.configure(image = self.unlocked)
                    self.lockButton.image = self.unlocked    
            if state is not self.DOOR.secured:
                state = self.DOOR.secured    
                if state is True:
                    self.stateLabel["text"] = "SECURED"
                else:
                    self.stateLabel["text"] = "UNSECURED"
            time.sleep(0.25)

    #===============================================================
    # toggle()
    #---------------------------------------------------------------
    # Toggle the lock if the button is pressed
    #---------------------------------------------------------------
    def toggle(self):
        # Door Locked, unlock it
        if self.DOOR.DOOR_IO.LOCK_BUFFER is True:
            self.DOOR.DOOR_IO.LOCK_BUFFER = False
        # Door unlocked, lock it
        else:
            self.DOOR.DOOR_IO.LOCK_BUFFER = True  

#==========================================================================================
