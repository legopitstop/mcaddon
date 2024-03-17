"""
Simple app to render JSON UIs without having to start the game.
"""

from tkinter import Tk, Listbox, Toplevel
from tkinter.scrolledtext import ScrolledText
import os
import glob
import commentjson

from ..experimental import UIGlobalVariables, UIDefs


class PreviewWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("UI Preview")
        self.geometry("700x700")


class UICreator(Tk):
    def __init__(self, directory: str):
        Tk.__init__(self)
        self.title("UI Creator")
        self.geometry("700x500")

        # Variables
        self.preview = PreviewWindow(self)
        self.global_variables = UIGlobalVariables()
        self.defs = UIDefs()
        self.directory = directory
        self.files = []

        # Widgets
        self.outliner = Listbox(self, width=50)
        self.outliner.bind("<<ListboxSelect>>", self.onselect)
        self.outliner.grid(row=0, column=0, sticky="ns")

        self.text = ScrolledText(self, state="disabled")
        self.text.grid(row=0, column=1, sticky="nesw")

        # Responsive
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Keybinds
        self.bind("<F5>", lambda e: self.refresh_files())

        self.load_files()

    def onselect(self, e):
        w = e.widget
        index = int(w.curselection()[0])
        fp = w.get(index)
        self.close_file()
        self.open_file(fp)

    def open_file(self, fp: str):
        self.text.configure(state="normal")
        self.text.delete(0.0, "end")
        with open(os.path.join(self.directory, fp)) as fd:
            content = commentjson.load(fd)
            self.text.insert(0.0, commentjson.dumps(content, indent=4))

    def close_file(self):
        self.text.delete(0.0, "end")
        self.text.configure(state="disabled")

    def load_files(self):
        self.files = [
            os.path.relpath(fp, self.directory)
            for fp in glob.glob(self.directory + "/**/*.json", recursive=True)
        ]
        for f in self.files:
            self.outliner.insert("end", f)

    def refresh_files(self):
        self.outliner.delete(0, "end")
        self.files = []
        self.load_files()


if __name__ == "__main__":
    app = UICreator()
    app.mainloop()
