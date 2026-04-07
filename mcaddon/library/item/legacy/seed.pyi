from ..component import ItemComponent

__all__ = ["ItemSeedComponent"]

class ItemSeedComponent(ItemComponent):
    """
    Use minecraft:block_placer in newer format versions.
    """

    crop_result: str
    plant_at: list[str] | str = ...
    plant_at_any_solid_surface: bool | None = ...
    plant_at_face: str | None = ...
