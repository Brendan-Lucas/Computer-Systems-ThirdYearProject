#============================================================================================
# widget_keypad.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
#--------------------------------------------------------------------------------------------
#
# Handles input from Keypad and Camera, and output to LCD
#
#============================================================================================
# Imports
import time
import threading
from tkinter import *
from winsound import *
from tkinter.filedialog import askopenfilename
from Door import Door

#============================================================================================
# Class Declaration
#--------------------------------------------------------------------------------------------
class KeypadPanel(Frame):     
#============================================================================================
    # Initializing Code
    #---------------------------------------------------------------
    def __init__(self, master, door):
        Frame.__init__(self, master)
        self["relief"]="raised"
        self["borderwidth"]="1"

        self.DOOR = door # Pointer to Door 
        self.grid()
        # Initialize Buttons
        buttonTags = ['1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D',]
        self.buttons = []
        i=0
        while(i<16):
            self.buttons.append(Button(self))
            self.buttons[i]["text"] = str(buttonTags[i])
            self.buttons[i]["fg"]  = "black"
            self.buttons[i]["width"] = "4"
            self.buttons[i]["height"] = "2"
            self.buttons[i]["relief"] = "flat"
            self.buttons[i]["borderwidth"] = "0"
            if(buttonTags[i].isnumeric()):
                self.buttons[i]["bg"] = "#b5e627"
            else:
                self.buttons[i]["bg"] = "white"
            self.buttons[i].grid(row=(i)//4+1,column=(i)%4,sticky=W+E+N+S)
            i+=1 
		# Initialize LCD
        self.LCD = Label(self)
        self.LCD["text"] = self.DOOR.DOOR_IO.LCD_BUFFER
        self.LCD["height"] = "2"
        self.LCD["fg"] = "black"
        self.LCD["bg"] = "white"
        self.LCD["relief"] = "sunken"
        self.LCD["borderwidth"] = "1"
        self.LCD.grid(row=0, column=0, columnspan = 4, sticky=W+E+N+S)

        # Button Commands
        self.buttons[ 0]["command"] = lambda: self.buttonPressed('1')
        self.buttons[ 1]["command"] = lambda: self.buttonPressed('2')
        self.buttons[ 2]["command"] = lambda: self.buttonPressed('3')
        self.buttons[ 3]["command"] = lambda: self.buttonPressed('A')
        self.buttons[ 4]["command"] = lambda: self.buttonPressed('4')
        self.buttons[ 5]["command"] = lambda: self.buttonPressed('5')
        self.buttons[ 6]["command"] = lambda: self.buttonPressed('6')
        self.buttons[ 7]["command"] = lambda: self.buttonPressed('B')
        self.buttons[ 8]["command"] = lambda: self.buttonPressed('7')
        self.buttons[ 9]["command"] = lambda: self.buttonPressed('8')
        self.buttons[10]["command"] = lambda: self.buttonPressed('9')
        self.buttons[11]["command"] = lambda: self.buttonPressed('C')
        self.buttons[12]["command"] = lambda: self.buttonPressed('*')
        self.buttons[13]["command"] = lambda: self.buttonPressed('0')
        self.buttons[14]["command"] = lambda: self.buttonPressed('#')
        self.buttons[15]["command"] = lambda: self.buttonPressed('D')
        
        # Launch Update Thread
        update_thread = threading.Thread(target=self.update,args=())
        update_thread.daemon = True
        update_thread.start()
        return

    #===============================================================
    # buttonPressed()
    #---------------------------------------------------------------
    # Modify KEYPAD_BUFFER with key that was pressed
    #---------------------------------------------------------------
    def buttonPressed(self, button):
        threading.Thread(target=PlaySound,args=('sounds/sound_keypad.wav', SND_FILENAME)).start()
        self.DOOR.DOOR_IO.KEYPAD_BUFFER = button
        return

    #===============================================================
    # update()
    #---------------------------------------------------------------
    # Update GUI with results from LCD_BUFFER
    #---------------------------------------------------------------
    def update(self):
        text = self.DOOR.DOOR_IO.LCD_BUFFER
        while True:
            # Check for Request to Take Picture
            if self.DOOR.DOOR_IO.CAMERA_BUFFER is not False:
                # Take picture with file dialog
                filename = askopenfilename(
                    initialdir="C:/Users/Dell/Pictures",
                    filetypes =(("JPEG File", "*.jpg;*.JPEG"),("All Files","*.*")),
                    title = "Choose an image to send."
                )         
                # Set Buffer
                if filename:
                    self.DOOR.DOOR_IO.CAMERA_BUFFER = filename
                else:
                    self.DOOR.DOOR_IO.CAMERA_BUFFER = False
            # Check for changes to LCD  
            if text is not self.DOOR.DOOR_IO.LCD_BUFFER: 
                text = self.DOOR.DOOR_IO.LCD_BUFFER
                self.LCD["text"] = text
            time.sleep(0.25) # Sleep for a 1/4 second

#============================================================================================
