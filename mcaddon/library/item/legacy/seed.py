__all__ = ["ItemSeedComponent"]

from typing import List, Optional, ClassVar
from pydantic import Field
from ..component import ItemComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use ItemBlockPlacerComponent instead.")
@ItemComponent.register
class ItemSeedComponent(ItemComponent):
    """
    Use minecraft:block_placer in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:seed"

    crop_result: str
    plant_at: List[str] | str = Field(default_factory=list)
    plant_at_any_solid_surface: Optional[bool] = None
    plant_at_face: Optional[str] = None
