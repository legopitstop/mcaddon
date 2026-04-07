from tkinter import Tk
from os import path

from mcaddon.contrib import ctkchooser
import mcpath

root = Tk()
root.withdraw()

p = path.join(
    mcpath.bedrockGDK.get_development_resource_packs_dir() or "", "assets_plus_RP"
)
pack = ctkchooser.ctkaskpack(resources_path="all-rp", initial=p)
if pack:
    print(pack.name, pack.path)
else:
    print(pack)

root.destroy()
