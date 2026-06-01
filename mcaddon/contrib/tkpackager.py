"""
Packager GUI for Minecraft Add-ons using tkinter.
"""

__all__ = ["TkPackager"]

from typing import Optional
from tkinter import (
    Tk,
    Frame,
    Menu,
    Label,
    Listbox,
    Button,
    OptionMenu,
    Entry,
    Checkbutton,
    StringVar,
    BooleanVar,
)
from tkinter.ttk import Notebook
from tkinter.messagebox import showinfo
from mclang import tl
import platform

from mcaddon import __version__, PackageFormat, VersionBump
from mcaddon.toolchain import PackagerConfig, Packager

from .tkchooser import askpack, askworld


class TkPackager(Tk):
    def __init__(self, config: Optional[PackagerConfig] = None):
        Tk.__init__(self)
        self.pconfig = config or PackagerConfig.from_file()
        self.api = Packager()

        self.title(tl("menu.mcaddon:packager"))
        # self.geometry('600x500')

        self.package_tool()

        self.menu = Menu(self)
        self.menu_config = Menu(self.menu, tearoff=False)
        self.menu_config.add_command(label="Import")
        self.menu_config.add_command(label="Export")
        self.menu_help = Menu(self.menu, tearoff=False)
        self.menu_help.add_command(label=tl("gui.about"), command=self.show_about)
        self.menu.add_cascade(label="Config", menu=self.menu_config)
        self.menu.add_cascade(label=tl("gui.help"), menu=self.menu_help)
        self.configure(menu=self.menu)

        self.rp_list: Optional[Listbox] = None
        self.bp_list: Optional[Listbox] = None
        self.sp_list: Optional[Listbox] = None

    def show_about(self) -> None:
        showinfo(
            tl("menu.mcaddon:packager"),
            f"MCADDON Packager\n\nVersion: {__version__}\nPython: {platform.python_version()}\nOS: {platform.system()} {platform.version()}",
            parent=self,
        )

    def package_tool(self) -> None:
        tabs = Notebook(self)

        # Variables

        RESOURCE_PACKS = []
        BEHAVIOR_PACKS = []
        SKIN_PACKS = []

        OUTPUT = StringVar()
        WORLD = StringVar(value=self.pconfig.world)
        FORMAT = StringVar(value=self.pconfig.format or "unset")
        BUMP = StringVar(value=self.pconfig.bump or "unset")
        MINIFY = BooleanVar(value=self.pconfig.minify)
        FLATTEN = BooleanVar(value=self.pconfig.flatten)
        VERIFY = BooleanVar(value=self.pconfig.verify)

        # Functions

        def build():
            format = (
                None if FORMAT.get() == "unset" else PackageFormat[FORMAT.get().upper()]
            )
            bump = None if BUMP.get() == "unset" else VersionBump[BUMP.get().upper()]
            config = PackagerConfig(
                world=WORLD.get(),
                format=format,
                bump=bump,
                minify=MINIFY.get(),
                flatten=FLATTEN.get(),
                verify=VERIFY.get(),
            )
            self.api.build(OUTPUT.get(), config)

        def choose_world():
            world = askworld(initial=WORLD.get())
            if not world or not world.path:
                return
            WORLD.set(world.path)

        def choose_pack(type: str):
            pack = askpack(resources_path="all-" + type)
            if not pack or not pack.path:
                return

            match type:
                case "rp":
                    # TODO: self.rp_list is always None?
                    if self.rp_list:
                        self.rp_list.insert("end", pack.name)
                    RESOURCE_PACKS.append(pack.path)
                case "bp":
                    if self.bp_list:
                        self.bp_list.insert("end", pack.name)
                    BEHAVIOR_PACKS.append(pack.path)
                case "sp":
                    if self.sp_list:
                        self.sp_list.insert("end", pack.name)
                    SKIN_PACKS.append(pack.path)

        # Widgets

        options_tab = Frame(tabs, padx=20)
        Label(
            options_tab,
            text=tl("options.mcaddon:output"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew")
        Label(options_tab, text=tl("options.mcaddon:output.desc"), anchor="w").grid(
            row=1, column=0, sticky="ew"
        )
        Entry(options_tab, textvariable=OUTPUT).grid(
            row=2, column=0, pady=(0, 20), sticky="ew"
        )
        Button(options_tab, text=tl("gui.choose")).grid(row=2, column=1, sticky="s")

        Label(
            options_tab,
            text=tl("options.mcaddon:format"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=3, column=0, sticky="ew")
        Label(options_tab, text=tl("options.mcaddon:format.desc"), anchor="w").grid(
            row=4, column=0, sticky="ew"
        )
        OptionMenu(options_tab, FORMAT, "unset", *[x for x in PackageFormat]).grid(
            row=5, column=0, pady=(0, 20), sticky="ew"
        )

        Label(
            options_tab, text=tl("options.mcaddon:bump"), font=("bold", 10), anchor="w"
        ).grid(row=6, column=0, sticky="ew")
        Label(options_tab, text=tl("options.mcaddon:bump.desc"), anchor="w").grid(
            row=7, column=0, sticky="ew"
        )
        OptionMenu(options_tab, BUMP, "unset", *[x for x in VersionBump]).grid(
            row=8, column=0, pady=(0, 20), sticky="ew"
        )

        Label(
            options_tab,
            text=tl("options.mcaddon:minify"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=9, column=0, sticky="ew")
        Checkbutton(options_tab, variable=MINIFY).grid(
            row=9, column=1, rowspan=2, pady=(0, 20), sticky="w"
        )
        Label(options_tab, text=tl("options.mcaddon:minify.desc"), anchor="w").grid(
            row=10, column=0, pady=(0, 20), sticky="ew"
        )

        Label(
            options_tab,
            text=tl("options.mcaddon:flatten"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=11, column=0, sticky="ew")
        Checkbutton(options_tab, variable=FLATTEN).grid(
            row=11, column=1, rowspan=2, pady=(0, 20), sticky="w"
        )
        Label(options_tab, text=tl("options.mcaddon:flatten.desc"), anchor="w").grid(
            row=12, column=0, pady=(0, 20), sticky="ew"
        )

        Label(
            options_tab,
            text=tl("options.mcaddon:verify"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=13, column=0, sticky="ew")
        Checkbutton(options_tab, variable=VERIFY).grid(
            row=13, column=1, rowspan=2, pady=(0, 20), sticky="w"
        )
        Label(options_tab, text=tl("options.mcaddon:verify.desc"), anchor="w").grid(
            row=14, column=0, pady=(0, 20), sticky="ew"
        )

        tabs.add(options_tab, text=tl("menu.mcaddon:packager.options"))

        content_tab = Frame(tabs)
        ct_left = Frame(content_tab, padx=20)
        Label(
            ct_left, text=tl("options.mcaddon:world"), font=("bold", 10), anchor="w"
        ).grid(row=0, column=0, sticky="ew")
        Label(ct_left, text=tl("options.mcaddon:world.desc"), anchor="w").grid(
            row=1, column=0, sticky="ew"
        )
        self.world_entry = Entry(ct_left, textvariable=WORLD, state="readonly").grid(
            row=2, column=0, pady=(0, 20), sticky="ew"
        )
        self.world_btn = Button(
            ct_left, text=tl("gui.choose"), command=choose_world
        ).grid(row=2, column=1, pady=(0, 20), sticky="s")

        Label(
            ct_left,
            text=tl("options.mcaddon:resourcePacks"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=3, column=0, sticky="ew")
        Label(ct_left, text=tl("options.mcaddon:resourcePacks.desc"), anchor="w").grid(
            row=4, column=0, sticky="ew"
        )
        self.rp_list = Listbox(ct_left).grid(row=5, column=0, pady=(0, 20), sticky="ew")
        self.rp_btn = Button(
            ct_left, text=tl("gui.choose"), command=lambda: choose_pack("rp")
        ).grid(row=5, column=1, pady=(0, 20), sticky="s")
        ct_left.grid(row=0, column=0, sticky="nw")

        ct_right = Frame(content_tab)
        Label(
            ct_right,
            text=tl("options.mcaddon:behaviorPacks"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew")
        Label(ct_right, text=tl("options.mcaddon:behaviorPacks.desc"), anchor="w").grid(
            row=1, column=0, sticky="ew"
        )
        self.bp_list = Listbox(ct_right).grid(
            row=2, column=0, pady=(0, 20), sticky="ew"
        )
        self.bp_btn = Button(
            ct_right, text=tl("gui.choose"), command=lambda: choose_pack("bp")
        ).grid(row=2, column=1, pady=(0, 20), sticky="s")

        Label(
            ct_right,
            text=tl("options.mcaddon:skinPacks"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=3, column=0, sticky="ew")
        Label(ct_right, text=tl("options.mcaddon:skinPacks.desc"), anchor="w").grid(
            row=4, column=0, sticky="ew"
        )
        self.sp_list = Listbox(ct_right).grid(
            row=5, column=0, pady=(0, 20), sticky="ew"
        )
        self.sp_btn = Button(
            ct_right, text=tl("gui.choose"), command=lambda: choose_pack("sp")
        ).grid(row=5, column=1, pady=(0, 20), sticky="s")
        ct_right.grid(row=0, column=1, sticky="nw")

        tabs.add(content_tab, text=tl("menu.mcaddon:packager.content"))

        # TODO: Render images in grid instead of listbox.
        marketing_tab = Frame(tabs, padx=20)
        Label(
            marketing_tab,
            text=tl("options.mcaddon:marketingArt"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=1, column=0, sticky="ew")
        Label(
            marketing_tab, text=tl("options.mcaddon:marketingArt.desc"), anchor="w"
        ).grid(row=2, column=0, sticky="ew")
        self.marketing_art_list = Listbox(marketing_tab).grid(
            row=3, column=0, pady=(0, 20), sticky="ew"
        )
        self.marketing_art_btn = Button(marketing_tab, text=tl("gui.choose")).grid(
            row=3, column=1, pady=(0, 20), sticky="s"
        )

        Label(
            marketing_tab,
            text=tl("options.mcaddon:storeArt"),
            font=("bold", 10),
            anchor="w",
        ).grid(row=4, column=0, sticky="ew")
        Label(marketing_tab, text=tl("options.mcaddon:storeArt.desc"), anchor="w").grid(
            row=5, column=0, sticky="ew"
        )
        self.store_art_list = Listbox(marketing_tab).grid(
            row=6, column=0, pady=(0, 20), sticky="ew"
        )
        self.store_art_btn = Button(marketing_tab, text=tl("gui.choose")).grid(
            row=6, column=1, pady=(0, 20), sticky="s"
        )

        tabs.add(marketing_tab, text=tl("menu.mcaddon:packager.marketing"))

        tabs.grid_columnconfigure(0, weight=1)
        tabs.grid(row=0, column=0, sticky="nesw")

        Button(self, text=tl("menu.mcaddon:packager.package"), command=build).grid(
            row=1, column=0, pady=20, padx=20, sticky="e"
        )
