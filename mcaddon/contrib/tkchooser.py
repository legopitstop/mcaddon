"""
A chooser for worlds and packs using tkinter
"""

__all__ = ["TkChooser", "PackButton", "askpack"]

from typing import Optional, Tuple, Literal, List
from tkinter import Label, Frame, Canvas, Scrollbar, Button, StringVar
from tkinter.simpledialog import Dialog
from PIL import ImageTk
from mclang import tl
from pathlib import Path
import re

from mcaddon import ResourceOutline, limit_lines
from .chooser import BaseChooser, PackChooser, WorldChooser


class ScrollableFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = Canvas(self, width=0, height=0, bg="white")
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class TkChooser(Dialog, BaseChooser):
    def __init__(
        self,
        title: str,
        prompt: str,
        resources_path: Optional[str] = None,
        parent=None,
        initial: Optional[str] = None,
        verbose: bool = False,
    ):
        BaseChooser.__init__(self, resources_path, initial)
        self.verbose = verbose
        self.prompt = prompt
        self.icon_cache: List[ImageTk.PhotoImage] = []
        self.resources = self.get_items()
        Dialog.__init__(self, parent, title)

    def render_items(self):
        self.icon_cache = []

        for child in self.items_frame.scrollable_frame.winfo_children():
            child.destroy()

        # Render items
        for row, resource in enumerate(self.sorted(self.resources)):
            bg = (
                "yellow"
                if Path(resource.path or "") == Path(self.selected or "")
                else "white"
            )
            f = Frame(self.items_frame.scrollable_frame, bg=bg)
            icon = resource.icon
            if icon is not None:
                icon = icon.resize((64, 64))
                self.icon_cache.append(ImageTk.PhotoImage(icon))
                Label(f, image=self.icon_cache[-1]).grid(
                    row=0, column=0, rowspan=2, sticky="w"
                )

            name = Label(
                f,
                text=re.sub(r"§.", "", resource.name),
                font=("bold"),
                bg=bg,
                anchor="w",
                wraplength=300,
                justify="left",
            )
            name.grid(row=0, column=1, sticky="ew")
            desc = Label(
                f,
                text=limit_lines(re.sub(r"§.", "", resource.description or ""), 2),
                bg=bg,
                anchor="w",
                wraplength=300,
                justify="left",
            )
            desc.grid(row=1, column=1, sticky="ew")

            f.grid_rowconfigure(0, weight=1)
            f.grid_columnconfigure(1, weight=1)
            f.grid(row=row, column=0, sticky="ew")

            def _bind_handler(event, _pack=resource):
                self.select(_pack.path)

            f.bind("<Button-1>", _bind_handler)
            name.bind("<Button-1>", _bind_handler)
            desc.bind("<Button-1>", _bind_handler)

    def body(self, master):
        self.geometry("400x300")
        master.pack(padx=5, pady=5, expand=1, fill="both")

        # widgets
        if self.prompt:
            Label(master, text=self.prompt).grid(row=0, column=0)

        self.items_frame = ScrollableFrame(master)

        self.render_items()

        self.items_frame.grid(row=1, column=0, sticky="nesw")
        self.items_frame.grid_rowconfigure(0, weight=1)
        self.items_frame.grid_columnconfigure(0, weight=1)

        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # refresh
        self.bind_all("<F5>", self.reload)

    def reload(self, e=None) -> None:
        self.resources = self.get_items()
        self.render_items()

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
        return Dialog.buttonbox(self)


class TkPackChooser(TkChooser, PackChooser):
    def __init__(self, **options):
        if "title" not in options:
            options["title"] = tl("menu.mcaddon:pack_chooser")

        if "prompt" not in options:
            options["prompt"] = tl("menu.mcaddon:pack_chooser.prompt")

        TkChooser.__init__(self, **options)


class TkWorldChooser(TkChooser, WorldChooser):
    def __init__(self, **options):
        if "title" not in options:
            options["title"] = tl("menu.mcaddon:world_chooser")

        if "prompt" not in options:
            options["prompt"] = tl("menu.mcaddon:world_chooser.prompt")

        TkChooser.__init__(self, **options)


def askpack(**options) -> Optional[ResourceOutline]:
    """Display dialog window for selection of a pack.

    Convenience wrapper for the PackChooser class.  Displays the pack
    chooser dialog.
    """

    d = TkPackChooser(**options)
    return d.result


def askworld(**options) -> Optional[ResourceOutline]:
    """Display dialog window for selection of a world.

    Convenience wrapper for the PackChooser class.  Displays the world
    chooser dialog.
    """

    d = TkWorldChooser(**options)
    return d.result


class PackButton(Button):
    def __init__(
        self,
        master=None,
        variable: Optional[StringVar] = None,
        packs_path: Optional[str] = None,
        icon_size: Tuple[int, int] = (32, 32),
        no_pack_msg: str = "No pack chosen",
        compound: Literal["top", "left", "center", "right", "bottom", "none"] = "left",
        **kw,
    ):
        self._DISPLAY = StringVar(value=no_pack_msg)
        self._PATH = StringVar() if variable is None else variable
        self.icon_size = icon_size
        self.packs_path = packs_path
        self.no_pack_msg = no_pack_msg
        self.selected = None
        if self._PATH.get():
            self.selected = ResourceOutline.from_path(self._PATH.get())
        Button.__init__(
            self,
            master,
            textvariable=self._DISPLAY,
            command=self._callback,
            compound=compound,
            **kw,
        )
        # Select initial pack (if any). Use `self.selected` to avoid
        # clashing with the tkinter `pack` method.
        self.select_pack(self.selected)

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
        pack = askpack(packs_path=self.packs_path, initial_pack=self.selected)
        self.select_pack(pack)
