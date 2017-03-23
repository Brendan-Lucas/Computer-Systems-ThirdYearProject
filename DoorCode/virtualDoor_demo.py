#####################################################
#
#   runVirtual.py
#   Patrick Perron
#
#####################################################

#imports
from tkinter import *
from VirtualDoorManager import VirtualDoorManager
from VirtualDoorSimulator import VirtualDoorSimulator


def main():
    output = []
    output.append(['1','1','Front','JJohnson'   , '1326'])
    output.append(['1','2','Back' ,'JJohnson'   , 'None'])
    output.append(['3','1','Front','AAaronson'  , 'A55B'])
    output.append(['3','2','Front','AAaronson'  , 'A55B'])
    output.append(['3','3','Back' ,'AAaronson'  , 'None'])
    output.append(['5','1','Front','TThompson'  , 'A55B'])
    output.append(['6','2','Front','RRichardson', '6565'])
    output.append(['9','3','Front','PPeterson'  , '6565'])
    if len(output) > 0:
        root2 = Tk()
        door = VirtualDoorSimulator(master=root2, info=output)
        door.mainloop()
        root2.destroy()

main()

#####################################################
