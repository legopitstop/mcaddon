from .component import ItemComponent

__all__ = ["ItemTagsComponent"]

class ItemTagsComponent(ItemComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/examples/itemcomponents/minecraft_tags)
    """

    tags: list[str] = ...

    def add(self, *tag: str) -> "ItemTagsComponent": ...
    def remove(self, tag: str) -> "ItemTagsComponent": ...
