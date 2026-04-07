__all__ = [
    "BlockLiquidDetectionComponent",
]

from typing import List, ClassVar, Optional
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import LiquidTouchBehavior, DirectionAll
from .component import BlockComponent


class DetectionRule(BaseModel):
    can_contain_liquid: bool = False
    on_liquid_touches: Optional[LiquidTouchBehavior] = None
    stops_liquid_flowing_from_direction: List[DirectionAll] = Field(
        default_factory=list
    )
    liquid_type: str = "water"

    def add(self, direction: DirectionAll) -> "DetectionRule":
        self.stops_liquid_flowing_from_direction.append(direction)
        return self


@BlockComponent.register
class BlockLiquidDetectionComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_liquid_detection)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:liquid_detection"

    detection_rules: List[DetectionRule] = Field(default_factory=list)

    def add(self, detection_rule: DetectionRule) -> "BlockLiquidDetectionComponent":
        self.detection_rules.append(detection_rule)
        return self
