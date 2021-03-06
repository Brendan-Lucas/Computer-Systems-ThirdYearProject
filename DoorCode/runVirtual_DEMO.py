#============================================================================================
# runVirtual_DEMO.py
#--------------------------------------------------------------------------------------------
# Patrick Perron
#--------------------------------------------------------------------------------------------
#
# Runs virtual door with preset door and homes
#
#============================================================================================
# Imports
from tkinter import *
from VirtualDoorSimulator import VirtualDoorSimulator

#============================================================================================
def main():
    output = []
    output.append(['1','1','Front','JJohnson'   , '1326'])
    output.append(['1','2','Back' ,'JJohnson'   , 'None'])
    output.append(['3','1','Front','AAaronson'  , 'A55B'])
    output.append(['3','2','Front','AAaronson'  , 'A55B'])
    output.append(['3','3','Back' ,'AAaronson'  , 'None'])
    output.append(['5','1','Front','TThompson'  , 'CC34'])
    output.append(['6','2','Front','RRichardson', '6540'])
    output.append(['9','3','Front','PPeterson'  , '6565'])
    if len(output) > 0:
        root2 = Tk()
        door = VirtualDoorSimulator(master=root2, info=output)
        door.mainloop()
        root2.destroy()

main()

#============================================================================================
