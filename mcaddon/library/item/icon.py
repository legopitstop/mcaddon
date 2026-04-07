"""Item icon component parsing helpers."""

__all__ = [
    "ItemIconComponent",
]

from typing import Dict, Optional, ClassVar
from pydantic import Field
from pydantic_core import core_schema

from mcaddon.core.base import ValueComponent
from .component import ItemComponent


@ItemComponent.register
class ItemIconComponent(ItemComponent, ValueComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_icon)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:icon"

    textures: Dict[str, str] = Field(default_factory=dict)
    texture: Optional[str] = Field(default=None, deprecated=True)

    def add(self, texture: str, key: Optional[str] = None) -> "ItemIconComponent":
        self.textures[key or "default"] = texture
        return self

    @classmethod
    def __get_pydantic_core_schema__(cls, _source, handler):
        schema = handler(_source)
        return core_schema.no_info_wrap_validator_function(
            cls._wrap_parse,
            schema,
        )

    @classmethod
    def _wrap_parse(cls, v, handler):
        if isinstance(v, str):
            v = {"textures": {"default": v}}
        elif isinstance(v, dict):
            if "textures" in v:
                pass
            elif "texture" in v and isinstance(v.get("texture"), str):
                tex = v.get("texture")
                rest = {k: val for k, val in v.items() if k != "texture"}
                v = {"textures": {"default": tex}, **rest}
            else:
                if all(
                    isinstance(k, str) and isinstance(val, str) for k, val in v.items()
                ):
                    v = {"textures": v}
        return handler(v)
