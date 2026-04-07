"""
A chooser for worlds and packs using customtkinter
"""

__all__ = ["CTkChooser", "CTkPackButton", "ctkaskpack"]

from typing import Optional, Tuple, List
from customtkinter import (
    CTk,
    CTkFont,
    CTkLabel,
    CTkFrame,
    CTkButton,
    CTkToplevel,
    StringVar,
    CTkScrollableFrame,
    CTkImage,
)
from tkinter import _get_temp_root, _destroy_temp_root  # type: ignore
from tkinter.simpledialog import _place_window, _setup_dialog  # type: ignore
from PIL import ImageTk
from mclang import tl
from pathlib import Path
import re

from mcaddon import ResourceOutline, limit_lines
from .chooser import BaseChooser, PackChooser, WorldChooser


class CTkDialog(CTkToplevel):
    def __init__(self, parent, title=None):
        master = parent
        if master is None:
            master = _get_temp_root()

        CTkToplevel.__init__(self, master)

        self.withdraw()
        if parent is not None and parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        _setup_dialog(self)
        self.parent = parent
        self.result = None

        body = CTkFrame(self, fg_color="transparent")
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if self.initial_focus is None:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        _place_window(self, parent)

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def destroy(self):
        self.initial_focus = None
        CTkToplevel.destroy(self)
        _destroy_temp_root(self.master)

    # construction hooks

    def body(self, master) -> Optional[CTk]:
        pass

    def buttonbox(self) -> None:

        box = CTkFrame(self, fg_color="transparent")

        w = CTkButton(box, text="OK", width=10, command=self.ok)
        w.pack(side="left", padx=5, pady=5)
        w = CTkButton(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    # standard button semantics

    def ok(self, event=None) -> None:
        if not self.validate() and self.initial_focus is not None:
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None) -> None:
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    # command hooks

    def validate(self) -> bool:
        return True

    def apply(self):
        pass


class CTkChooser(CTkDialog, BaseChooser):
    def __init__(
        self,
        title: str,
        prompt: str,
        resources_path: Optional[str] = None,
        initial: Optional[str] = None,
        parent=None,
    ):
        BaseChooser.__init__(self, resources_path, initial)
        self.prompt = prompt
        self.icon_cache: List[ImageTk.PhotoImage] = []
        self.resources = self.get_items()
        CTkDialog.__init__(self, parent, title)

    def render_items(self) -> None:
        self.icon_cache = []

        for child in self.items_frame.winfo_children():
            child.destroy()

        # Render items
        for row, resource in enumerate(self.sorted(self.resources)):
            border_width = (
                2 if Path(resource.path or "") == Path(self.selected or "") else 0
            )
            f = CTkFrame(
                self.items_frame, border_color="yellow", border_width=border_width
            )
            icon = resource.icon
            if icon is not None:
                img = CTkImage(icon, icon, size=(64, 64))
                CTkLabel(f, text="", image=img).grid(
                    row=0, column=0, rowspan=2, sticky="w", pady=5, padx=5
                )

            name = CTkLabel(
                f,
                text=re.sub(r"§.", "", resource.name),
                font=CTkFont(weight="bold"),
                anchor="w",
                wraplength=300,
                justify="left",
            )
            name.grid(row=0, column=1, sticky="w", padx=4)
            desc = CTkLabel(
                f,
                text=limit_lines(re.sub(r"§.", "", resource.description or ""), 2),
                anchor="w",
                wraplength=300,
                justify="left",
            )
            desc.grid(row=1, column=1, sticky="w", padx=4, pady=(0, 4))

            f.grid_rowconfigure(0, weight=1)
            f.grid(row=row, column=0, sticky="ew", pady=5, ipadx=5, ipady=5)
            f.bind("<Button-1>", lambda e, pack=resource: self.select(pack.path))
            name.bind("<Button-1>", lambda e, pack=resource: self.select(pack.path))
            desc.bind("<Button-1>", lambda e, pack=resource: self.select(pack.path))

    def body(self, master) -> Optional[CTk]:
        self.geometry("400x300")
        master.pack(padx=5, pady=5, expand=1, fill="both")

        # widgets
        if self.prompt:
            CTkLabel(master, text=self.prompt).grid(row=0, column=0)

        self.items_frame = CTkScrollableFrame(master)

        self.render_items()

        self.items_frame.grid(row=1, column=0, sticky="nesw")
        self.items_frame.grid_rowconfigure(0, weight=1)
        self.items_frame.grid_columnconfigure(0, weight=1)

        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # refresh
        self.bind_all("<F5>", self.reload)

        return master

    def validate(self) -> bool:
        self.result = self.getresult()
        return True

    def getresult(self) -> Optional[ResourceOutline]:
        if self.selected is None:
            return None

        for p in self.resources:
            if Path(p.path or "") == Path(self.selected):
                return p
        return None

    def reload(self, e=None) -> None:
        self.resources = self.get_items()
        self.render_items()

    def _up(self, e=None) -> None:
        if self.selected is None:
            return
        keys = [x.path for x in self.resources]
        try:
            idx = keys.index(self.selected)
            id = keys[idx - 1] if idx - 1 >= 0 else None
            if id is None:
                return
            self.select(id)
        except ValueError:
            return None

    def _down(self, e=None) -> None:
        if self.selected is None:
            return
        keys = [x.path for x in self.resources]
        try:
            idx = keys.index(self.selected)
            id = keys[idx + 1] if idx + 1 < len(keys) else None
            if id is None:
                return
            self.select(id)
        except ValueError:
            return None

    def buttonbox(self) -> None:
        self.bind("<Up>", self._up)
        self.bind("<Down>", self._down)
        return CTkDialog.buttonbox(self)


class CTkPackChooser(CTkChooser, PackChooser):
    def __init__(self, **options):  # TODO: pack_type
        if "title" not in options:
            options["title"] = tl("menu.mcaddon:pack_chooser")

        if "prompt" not in options:
            options["prompt"] = tl("menu.mcaddon:pack_chooser.prompt")

        CTkChooser.__init__(self, **options)


class CTkWorldChooser(CTkChooser, WorldChooser):
    def __init__(self, **options):
        if "title" not in options:
            options["title"] = tl("menu.mcaddon:world_chooser")

        if "prompt" not in options:
            options["prompt"] = tl("menu.mcaddon:world_chooser.prompt")

        CTkChooser.__init__(self, **options)


def ctkaskpack(**options) -> Optional[ResourceOutline]:
    d = CTkPackChooser(**options)
    return d.result


def ctkaskworld(**options) -> Optional[ResourceOutline]:
    d = CTkWorldChooser(**options)
    return d.result


class CTkPackButton(CTkButton):
    def __init__(
        self,
        master=None,
        variable: Optional[StringVar] = None,
        packs_path: Optional[str] = None,
        icon_size: Tuple[int, int] = (32, 32),
        no_pack_msg: str = "No pack chosen",
        compound: str = "left",
        **kw
    ):
        self._DISPLAY = StringVar(value=no_pack_msg)
        self._PATH = StringVar() if variable is None else variable
        self.icon_size = icon_size
        self.packs_path = packs_path
        self.no_pack_msg = no_pack_msg
        self.selected = None
        if self._PATH.get():
            self.selected = ResourceOutline.from_path(self._PATH.get())
        CTkButton.__init__(
            self,
            master,
            textvariable=self._DISPLAY,
            command=self._callback,
            compound=compound,
            **kw
        )

    def select_pack(self, pack: Optional[ResourceOutline]) -> None:
        if pack is None:
            self.selected = None
            self._PATH.set("")
            self._DISPLAY.set(self.no_pack_msg)
            self.configure(image="")
            return

        self.selected = pack
        self._DISPLAY.set(pack.name)
        self._PATH.set("" if pack.path is None else pack.path)

        if self.selected.icon is None:
            self._img = None
            self.configure(image="")
            return

        self._img = ImageTk.PhotoImage(self.selected.icon.resize(self.icon_size))
        self.configure(image=self._img)

    def _callback(self) -> None:
        pack = ctkaskpack(packs_path=self.packs_path, initial_pack=self.selected)
        self.select_pack(pack)
