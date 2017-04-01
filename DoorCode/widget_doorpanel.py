#============================================================================================
# widget_doorpanel.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
#--------------------------------------------------------------------------------------------
#
# Widget for controlling and displating the state of a door
#
#============================================================================================
# Imports
from tkinter import *
from Door import Door
from winsound import *
import threading

#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class DoorPanel(Frame):
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self, master, door):
        Frame.__init__(self, master)
        self.DOOR = door

        self["relief"]="raised"
        self["borderwidth"]="1"

        self.closed_image = PhotoImage(file="images/closed.png")
        self.open_image   = PhotoImage(file="images/open.png")
        
        self.panel = Button(self.master, image=self.closed_image)
        self.panel.image = self.closed_image
        self.panel["relief"] = "flat"
        self.panel["borderwidth"] = "0"
        self.panel["bg"] = "white"
        self.panel["activebackground"] = "white"
        self.panel["command"] = lambda: self.toggle()
        self.panel.grid(row=1,column=0,sticky=W+E+N+S)
	
    #===============================================================
    # toggle()
    #---------------------------------------------------------------
    # Modify the state of the door if door is unlocked
    #---------------------------------------------------------------
    def toggle(self):
        #Toggle only if door is not locked
        if self.DOOR.DOOR_IO.LOCK_BUFFER is False:
          if self.DOOR.DOOR_IO.DOOR_BUFFER is True:
            self.DOOR.DOOR_IO.DOOR_BUFFER = False
            self.panel.configure(image = self.closed_image)
            self.panel.image = self.closed_image
            threading.Thread(target=PlaySound,args=('sounds/sound_closed.wav', SND_FILENAME)).start()
          else:
            self.DOOR.DOOR_IO.DOOR_BUFFER = True
            self.panel.configure(image = self.open_image)
            self.panel.image = self.open_image
            threading.Thread(target=PlaySound,args=('sounds/sound_open.wav', SND_FILENAME)).start()
        else:
            threading.Thread(target=PlaySound,args=('sounds/sound_blocked.wav', SND_FILENAME)).start()

#============================================================================================
   
		
		
