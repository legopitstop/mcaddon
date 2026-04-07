from tkinter import Tk

from mcaddon.contrib import ctkchooser


root = Tk()
root.withdraw()

world = ctkchooser.ctkaskworld()
if world:
    print(world.name, world.path)
else:
    print(world)

root.destroy()
