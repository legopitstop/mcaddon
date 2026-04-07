from tkinter import Tk

from mcaddon.contrib import tkchooser


root = Tk()
root.withdraw()

world = tkchooser.askworld(title="Choose World", verbose=True)
if world:
    print(world.name, world.path)
else:
    print(world)

root.destroy()
