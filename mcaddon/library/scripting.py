__all__ = ["ScriptFile"]

from typing import ClassVar
from py_mini_racer import MiniRacer

from mcaddon.core.file import File
from .pack import behaviorpack


@behaviorpack("scripts")
class ScriptFile(File):
    extension: ClassVar[str] = ".js"
    ctx = MiniRacer()

    def __init__(self, code: str):
        self.code = code

    def __exit__(self, a, b, c):
        self.ctx.close()
        File.__exit__(self, a, b, c)

    @classmethod
    def loads(cls, code: str) -> "ScriptFile":
        self = cls.__new__(cls)
        self.code = code
        return self

    def dumps(self, *args, **kw) -> str:
        return self.code

    def __call__(self):
        return self.ctx.eval(self.code)
