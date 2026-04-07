from tkinter import Tk
from os import path
from mcaddon.contrib import tkchooser
import mcpath

root = Tk()
root.withdraw()

p = path.join(
    mcpath.bedrockGDK.get_development_resource_packs_dir() or "", "assets_plus_RP"
)
pack = tkchooser.askpack(title="Choose Pack", resources_path="all-rp", initial=p)
if pack:
    print(pack.name, pack.path)
else:
    print(pack)

root.destroy()
