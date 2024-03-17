from typing import Self

from .util import Misc


class LiteralContent(str):
    def jsonify(self) -> dict:
        data = {"text": str(self)}
        return data


class Text(Misc):
    @property
    def content(self) -> LiteralContent:
        return getattr(self, "_content")

    @content.setter
    def content(self, value):
        self.on_update("content", value)
        setattr(self, "_content", value)

    @classmethod
    def literal(cls, text: str) -> Self:
        self = cls.__new__(cls)
        self.content = LiteralContent(text)
        return self

    def jsonify(self) -> dict:
        data = {"rawtext": [self.content.jsonify()]}
        return data
