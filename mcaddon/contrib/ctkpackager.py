"""
Packager GUI for Minecraft Add-ons using customtkinter.
"""

__all__ = ["CTkPackager"]

from typing import Optional
from tkinter import Menu
from customtkinter import CTk, CTkTabview, CTkLabel
from mclang import tl

from mcaddon import __version__
from mcaddon.toolchain import PackagerConfig, Packager


class CTkPackager(CTk):
    def __init__(self, config: Optional[PackagerConfig] = None):
        CTk.__init__(self)
        self.pconfig = config or PackagerConfig()
        self.api = Packager()

        self.title(tl("menu.mcaddon:packager", __version__))

        self.package_tool()

        self.menu = Menu(self)
        self.menu_config = Menu(self.menu, tearoff=False)
        self.menu_config.add_command(label="Import")
        self.menu_config.add_command(label="Export")
        self.menu.add_cascade(label="Config", menu=self.menu_config)
        self.configure(menu=self.menu)

    def package_tool(self) -> None:
        tabs = CTkTabview(self)

        # Variables

        # RESOURCE_PACKS = []
        # BEHAVIOR_PACKS = []
        # SKIN_PACKS = []

        # OUTPUT = StringVar()
        # WORLD = StringVar(value=self.pconfig.world)
        # FORMAT = StringVar(value=self.pconfig.format or "unset")
        # BUMP = StringVar(value=self.pconfig.bump or "unset")
        # MINIFY = BooleanVar(value=self.pconfig.minify)
        # FLATTEN = BooleanVar(value=self.pconfig.flatten)
        # VERIFY = BooleanVar(value=self.pconfig.verify)

        # Functions

        # Widgets

        options_tab = tabs.add(tl("menu.mcaddon:packager.options"))
        CTkLabel(options_tab, text="Options").grid(row=0, column=0)

        content_tab = tabs.add(tl("menu.mcaddon:packager.content"))
        CTkLabel(content_tab, text="Content").grid(row=0, column=0)

        marketing_tab = tabs.add(tl("menu.mcaddon:packager.marketing"))
        CTkLabel(marketing_tab, text="Marketing").grid(row=0, column=0)

        tabs.grid_columnconfigure(0, weight=1)
        tabs.grid(row=0, column=0, sticky="nesw")
