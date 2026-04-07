__all__ = ["LocaleText"]

from typing import ClassVar
import mclang

from mcaddon.core.file import TextFile
from .pack import basepack


@basepack("texts")
class LocaleText(TextFile):
    extension: ClassVar[str] = ".lang"
    texts = mclang.Lang()

    @classmethod
    def loads(cls, obj: str, *args, **kw) -> "LocaleText":
        self = cls.__new__(cls)
        obj = obj.lstrip("\ufeff")  # remove BOM
        res = mclang.loads(obj)
        self.texts.update(res)
        return self

    def dumps(self, *args, **kw) -> str:
        return self.texts.dumps(*args, **kw)

    def translate(self, __key: str, *subs: str, fallback: str | None = None) -> str:
        return self.texts.translate(__key, *subs, fallback=fallback)

    tl = translate
