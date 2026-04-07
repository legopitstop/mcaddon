from tkinter import Tk, StringVar, Button

from mcaddon.contrib import tkchooser


root = Tk()
root.geometry("500x500")

PACK = StringVar()

pack = tkchooser.PackButton(root, variable=PACK)
pack.grid(row=0)

Button(root, text="Print path", command=lambda: print(PACK.get())).grid(row=1)

root.mainloop()
