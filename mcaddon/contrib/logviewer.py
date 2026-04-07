"""
Log Viewer for Minecraft Bedrock Edition logs using tkinter.
"""

__all__ = ["LogViewer", "LogViewerDefinition"]

# TODO:
# - Type Filter: Json, Texture, Scripting, Recipes, Molang, Block
# - Log Level: Verbose, Info, Warn
# - Cache highlighting tags.

from typing import Optional, List, Tuple, Set, Callable, cast
from tkinter import Tk, Text, Button, Entry, Label, Frame, StringVar, Menu
from pydantic import Field
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from mclang import tl
from mcaddon.core.base import BaseModel
import webbrowser
import time
import mcpath
import os
import re


class LogViewerDefinition(BaseModel):
    name: str
    items: Set[str] = Field(default_factory=set)
    command: Optional[Callable[[str], None]] = None

    def __hash__(self) -> int:
        return hash(self.name)


class LogViewer(Tk, FileSystemEventHandler):
    def __init__(self, path: Optional[str] = None):
        super().__init__()
        self.title(tl("menu.mcaddon:log_viewer"))

        # Variables
        self.FIND = StringVar()
        self.FIND_RESULTS = StringVar(value=tl("menu.mcaddon:log_viewer.no_results"))
        self.matches: List[Tuple[str, str]] = []
        self.match_index = 0
        self.query = ""

        self.body()

        types = {
            "Texture",
            "Actor",
            "Scripting",
            "Texture",
            "Components",
            "Recipes",
            "Json",
            "Molang",
            "Blocks",
            "Items",
        }
        levels = {"inform", "error", "warning", "verbose"}

        self.definitions: Set[LogViewerDefinition] = set([])
        self.styles = {
            "time": r"^\d{2}:\d{2}:\d{2}",
            "type": r"^[^\[]*(\[[^\]]+\])",
            "level": r"^[^\[]*\[[^\]]+\](\[[^\]]+\])",
            "string": r'"(?:\\.|[^"\\\n])*"' + "|" + r"'(?:\\.|[^'\\\n])*'",
            "link": r'https?://[^\s"\']+',
            "uuid": r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
        }

        self.styles.update({f"type.{x.upper()}": f"\\[{x}\\]" for x in types})
        self.styles.update({f"level.{x.upper()}": f"\\[{x}\\]" for x in levels})
        for v in self.definitions:
            tagName = f"definition.{v.name.upper()}"
            self.styles[tagName] = f"\\b({'|'.join(re.escape(e) for e in v.items)})\\b"
            if not v.command:
                continue

            def _on_enter(event: object) -> None:
                self.text.config(cursor="hand2")

            def _on_leave(event: object) -> None:
                self.text.config(cursor="")

            def _make_def_cb(definition: LogViewerDefinition, tag: str):
                def _cb(event: object) -> None:
                    self._definition_cb(event, tag, definition)

                return _cb

            self.text.tag_bind(tagName, "<Enter>", _on_enter)
            self.text.tag_bind(tagName, "<Leave>", _on_leave)
            self.text.tag_bind(tagName, "<Control-1>", _make_def_cb(v, tagName))

        # Load file
        self.last_modified = time.time()
        self.end_line: int = 0
        self.lines: List[str] = []
        self.path = mcpath.bedrockGDK.get_logs_dir() if path is None else path
        self.fp = self.get_latest_log()
        if self.fp:
            self.load()
            self._start()

        # Menu
        self.menu = Menu(self)
        self.menu.add_command(label=tl("gui.clear"), command=self._clear)
        self.menu.add_command(label=tl("gui.copy"), command=self._copy)

        self.configure(menu=self.menu, bg="#272727")

        # Manual refresh
        self.bind("<F5>", lambda e: self.load())
        self.bind("<Control-f>", lambda e: self._toggle_find())

        self.text.tag_config("time", foreground="#6B7280")

        self.text.tag_config("type", foreground="#2980B9")
        self.text.tag_config("type.TEXTURE", foreground="#9B59B6")
        self.text.tag_config("type.ACTOR", foreground="#16A085")
        self.text.tag_config("type.UI", foreground="#E67E22")
        self.text.tag_config("type.SCRIPTING", foreground="#10B981")
        self.text.tag_config("type.RECIPES", foreground="#F97316")
        self.text.tag_config("type.JSON", foreground="#3B82F6")
        self.text.tag_config("type.MOLANG", foreground="#8B5CF6")
        self.text.tag_config("type.BLOCKS", foreground="#16A34A")
        self.text.tag_config("type.ITEMS", foreground="#B45309")

        self.text.tag_config("level", foreground="black", background="white")
        self.text.tag_config("level.INFORM", foreground="#1E90FF", background="#C7E2FF")
        self.text.tag_config("level.ERROR", foreground="#FF2D2D", background="#FFD1D1")
        self.text.tag_config(
            "level.WARNING", foreground="#FFB000", background="#FFE3A3"
        )
        self.text.tag_config(
            "level.VERBOSE", foreground="#7F8C8D", background="#E6E8EA"
        )
        self.text.tag_config("string", foreground="#CE9178")

        self.text.tag_config(
            "link",
            foreground="#2563EB",
            underline=True,
        )
        self.text.tag_bind("link", "<Control-Button-1>", self._tag_link)
        self.text.tag_bind(
            "link", "<Enter>", lambda e: self.text.config(cursor="hand2")
        )
        self.text.tag_bind("link", "<Leave>", lambda e: self.text.config(cursor=""))
        self.text.tag_config("uuid", foreground="#0EA5A5")

        self.text.tag_config("definition.ITEM", foreground="#ff7b72")

    def _definition_cb(
        self, event, tagName: str, definition: LogViewerDefinition
    ) -> None:
        if not definition.command:
            return
        v = self.get_tag_value(tagName, event)
        if v is None:
            return
        definition.command(v)

    def get_tag_value(self, tagName: str, event) -> Optional[str]:
        index = self.text.index(f"@{event.x},{event.y}")
        tags = self.text.tag_names(index)
        if tagName in tags:
            ranges = self.text.tag_ranges(tagName)
            for i in range(0, len(ranges), 2):
                start, end = ranges[i], ranges[i + 1]
                if self.text.compare(start, "<=", index) and self.text.compare(
                    index, "<", end
                ):
                    return self.text.get(start, end)
        return None

    def _tag_link(self, event) -> None:
        index = self.text.index(f"@{event.x},{event.y}")
        tags = self.text.tag_names(index)
        if "link" in tags:
            ranges = self.text.tag_ranges("link")
            for i in range(0, len(ranges), 2):
                start, end = ranges[i], ranges[i + 1]
                if self.text.compare(start, "<=", index) and self.text.compare(
                    index, "<", end
                ):
                    link_text = self.text.get(start, end)
                    webbrowser.open(link_text)
                    break

    def _close_find(self) -> None:
        self._clear_highlight()
        self.find.grid_forget()

    def _toggle_find(self) -> None:
        if self.find.winfo_viewable():
            self._close_find()
        else:
            self.find_entry.focus_set()
            self.find.grid(row=0, column=0, sticky="e")

    def _start(self) -> None:
        if self.fp:
            self.observer = Observer()
            self.observer.schedule(self, path=os.path.dirname(self.fp), recursive=False)
            self.observer.start()

    def _clear_highlight(self) -> None:
        self.text.tag_remove("highlight", "1.0", "end")
        self.text.tag_remove("current", "1.0", "end")
        self.matches.clear()
        self.match_index = 0

    def search(self) -> None:
        query = self.FIND.get()
        if not query or query == self.query:
            return

        self._clear_highlight()

        self.FIND_RESULTS.set(tl("menu.mcaddon:log_viewer.no_results"))

        start = "1.0"
        count = 0
        while True:
            pos = self.text.search(query, start, stopindex="end", nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(query)}c"
            self.matches.append((pos, end))
            self.text.tag_add("highlight", pos, end)
            start = end
            count += 1

        self.FIND_RESULTS.set(tl("menu.mcaddon:log_viewer.results", "", str(count)))
        self.text.tag_config("highlight", background="yellow", foreground="black")
        self.text.tag_config("current", background="orange", foreground="black")
        self.query = query

    def show_next(self) -> None:
        if not self.matches:
            return

        self.text.tag_remove("current", "1.0", "end")
        start, end = self.matches[self.match_index]
        self.text.tag_add("current", start, end)
        self.text.see(start)
        self.match_index = (self.match_index + 1) % len(self.matches)
        self.FIND_RESULTS.set(
            tl(
                "menu.mcaddon:log_viewer.results",
                str(self.match_index + 1),
                str(len(self.matches)),
            )
        )

    def show_prev(self) -> None:
        if not self.matches:
            return

        self.text.tag_remove("current", "1.0", "end")
        start, end = self.matches[self.match_index]
        self.text.tag_add("current", start, end)
        self.text.see(start)
        self.match_index = (self.match_index - 1) % len(self.matches)
        self.FIND_RESULTS.set(
            tl(
                "menu.mcaddon:log_viewer.results",
                str(self.match_index + 1),
                str(len(self.matches)),
            )
        )

    def on_modified(self, event) -> None:
        if event.src_path == self.fp:
            now = time.time()
            if now - self.last_modified > 0.5:
                self.last_modified = now
                self.load()

    def _clear(self) -> None:
        text = self.text.get(0.0, "end")
        self.end_line += len(text.splitlines())
        self.draw()

    def _copy(self) -> None:
        content = self.text.get(0.0, "end")
        self.clipboard_clear()
        self.clipboard_append(content)

    def draw(self) -> None:
        self.clear_style()
        self.text.configure(state="normal")
        self.text.delete(0.0, "end")
        self.text.insert(0.0, "\n".join(self.lines[self.end_line :]))
        self.text.configure(state="disabled")
        self.apply_style()

    def load(self) -> None:
        if self.fp and os.path.isfile(self.fp):
            with open(self.fp) as fd:
                self.lines = fd.read().replace("\n\n", "\n").splitlines()
                self.draw()

    def body(self) -> None:
        self.text = Text(self, bd=0, bg="#272727", font=("Consolas", 12), fg="white")
        self.image_references: List[str] = []
        self.text.grid(row=1, column=0, sticky="nesw")

        # Find
        self.find = Frame(self, cursor="arrow")
        self.find.bind("<Escape>", lambda e: self._toggle_find())
        self.find_entry = Entry(self.find, textvariable=self.FIND)
        self.find_entry.bind("<KeyRelease>", lambda e: self.search())
        self.find_entry.bind("<Return>", lambda e: self.show_next())
        self.find_entry.grid(row=0, column=0)
        Label(self.find, textvariable=self.FIND_RESULTS).grid(row=0, column=1)
        Button(self.find, text="↑", command=self.show_prev, width=2).grid(
            row=0, column=2
        )
        Button(self.find, text="↓", command=self.show_next, width=2).grid(
            row=0, column=3
        )

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def get_latest_log(self) -> Optional[str]:
        logs: List[Tuple[datetime, str]] = []
        pattern = re.compile(r"ContentLog(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})")

        if self.path is None:
            raise Exception(f"Path not found '{self.path}'")
        for root, dirs, files in os.walk(self.path):
            for file in files:
                match = pattern.match(file)
                if match:
                    timestamp_str: str = cast(str, match.group(1))
                    try:
                        timestamp = datetime.strptime(
                            timestamp_str, "%Y-%m-%d_%H-%M-%S"
                        )
                        full_path = os.path.join(root, file)
                        logs.append((timestamp, full_path))
                    except ValueError:
                        continue  # skip malformed timestamps

        if not logs:
            return None  # or raise an exception

        # Get the path with the latest timestamp
        latest_log = max(logs, key=lambda x: x[0])[1]
        return cast(Optional[str], latest_log)

    def clear_style(self):
        for x in self.styles.keys():
            self.text.tag_remove(x, "1.0", "end")

    def apply_style(self):
        content = self.text.get("1.0", "end-1c")

        for k, v in self.styles.items():
            pattern = re.compile(v, re.MULTILINE)
            for m in pattern.finditer(content):
                if m.lastindex:
                    start_pos = m.start(1)
                    end_pos = m.end(1)
                else:
                    start_pos = m.start()
                    end_pos = m.end()
                self.text.tag_add(k, f"1.0+{start_pos}c", f"1.0+{end_pos}c")
