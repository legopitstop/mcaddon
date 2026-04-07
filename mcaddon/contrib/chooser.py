"""
A generic chooser for worlds and packs
"""

__all__ = ["BaseChooser", "WorldChooser", "PackChooser"]

from abc import ABC
from typing import Optional, Set, List
import mcpath

from mcaddon import ResourceOutline


class BaseChooser(ABC):
    """
    Common code for choosers
    """

    def __init__(
        self,
        resources_path: Optional[str] = None,
        initial: Optional[str] = None,
    ):
        self.resources_path: str = resources_path or "rp"
        self.selected = initial

    def sorted(self, items: Set[ResourceOutline]) -> List[ResourceOutline]:
        return sorted(list(items), key=lambda u: u.name)

    def select(self, path: Optional[str]) -> None:
        if path is None:
            return

        self.selected = path
        self.render_items()

    # Hooks

    def get_items(self) -> Set[ResourceOutline]:
        return set([])

    def render_items(self) -> None: ...


class WorldChooser(BaseChooser, ABC):
    def get_items(self) -> Set[ResourceOutline]:
        return {ResourceOutline.from_path(p) for p in mcpath.bedrockGDK.get_worlds()}


class PackChooser(BaseChooser, ABC):
    def get_items(self) -> Set[ResourceOutline]:
        packs: Set[ResourceOutline] = set([])
        match self.resources_path.lower():
            case "resource_packs" | "rp":
                packs = {
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_resource_packs()
                }
            case "behavior_packs" | "bp":
                packs = {
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_behavior_packs()
                }

            case "development_resource_packs" | "dev-rp":
                packs = {
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_development_resource_packs()
                }
            case "development_behavior_packs" | "dev-bp":
                packs = {
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_development_behavior_packs()
                }
            case "development_skin_packs" | "dev-sp":
                packs = {
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_development_skin_packs()
                }
            case "all-rp":
                dev = [
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_development_resource_packs()
                ]
                pks = [
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_resource_packs()
                ]
                packs = set([*dev, *pks])
            case "all-bp":
                dev = [
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_development_behavior_packs()
                ]
                pks = [
                    ResourceOutline.from_path(p)
                    for p in mcpath.bedrockGDK.get_behavior_packs()
                ]
                packs = set([*dev, *pks])
            case _:
                for pack in ResourceOutline.find_packs(self.resources_path, False):
                    packs.add(pack)
        return packs
