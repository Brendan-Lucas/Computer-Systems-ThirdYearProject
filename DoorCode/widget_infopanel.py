#============================================================================================
# widget_infopanel.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
#--------------------------------------------------------------------------------------------
#
# Information panel for displaying information about door being simulated
#
#============================================================================================
# Imports
from tkinter import *
from Door import Door

#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class InfoPanel(Frame):
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self, master, door, info):
        Frame.__init__(self, master)
        self.grid()
		# Home ID
        self.HomeIDTag = Label(self, text="Home ID", anchor="e", width=7, bg="white", fg="black", relief="flat")
        self.HomeIDTag.config(font=("Helvetica", 7))
        self.HomeIDTag.grid(row=0,column=0,sticky=W+E+N+S)
        self.HomeIDLabel = Label(self, text=str(door.HOME_ID), anchor="w", width=12, bg="white", fg="black", relief="sunken")
        self.HomeIDLabel.grid(row=0,column=1,sticky=W+E+N+S)
		# Door ID
        self.DoorIDTag = Label(self, text="Door ID", anchor="e", width=7, bg="white", fg="black", relief="flat")
        self.DoorIDTag.config(font=("Helvetica", 7))
        self.DoorIDTag.grid(row=1,column=0,sticky=W+E+N+S)
        self.DoorIDLabel = Label(self, text=str(door.DOOR_ID), anchor="w", width=12, bg="white", fg="black", relief="sunken")
        self.DoorIDLabel.grid(row=1,column=1,sticky=W+E+N+S)
        # Door Type
        self.TypeTag = Label(self, text="Type", anchor="e", width=7, bg="white", fg="black", relief="flat")
        self.TypeTag.config(font=("Helvetica", 7))
        self.TypeTag.grid(row=2,column=0,sticky=W+E+N+S)
        self.TypeLabel = Label(self, text=info[0], anchor="w", width=12, bg="white", fg="black", relief="sunken")
        self.TypeLabel.grid(row=2,column=1,sticky=W+E+N+S)
        # Door Owner
        self.OwnerTag = Label(self, text="Owner", anchor="e", width=7, bg="white", fg="black", relief="flat")
        self.OwnerTag.config(font=("Helvetica", 7))
        self.OwnerTag.grid(row=3,column=0,sticky=W+E+N+S)
        self.OwnerLabel = Label(self, text=info[1], anchor="w", width=12, bg="white", fg="black", relief="sunken")
        self.OwnerLabel.grid(row=3,column=1,sticky=W+E+N+S)
		# Door Code
        self.CodeTag = Label(self, text="Password", anchor="e", width=7, bg="white", fg="black", relief="flat")
        self.CodeTag.config(font=("Helvetica", 7))
        self.CodeTag.grid(row=4,column=0,sticky=W+E+N+S)
        self.CodeLabel = Label(self, text=info[2], anchor="w", width=12, bg="white", fg="black", relief="sunken")
        self.CodeLabel.grid(row=4,column=1,sticky=W+E+N+S)
        
#============================================================================================
		
