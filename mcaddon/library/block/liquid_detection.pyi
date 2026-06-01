from .component import BlockComponent
from mcaddon.core.base import BaseModel
from mcaddon.library.constants import DirectionAll, LiquidTouchBehavior

__all__ = ["BlockLiquidDetectionComponent", "ItemDetectionRule"]

class ItemDetectionRule(BaseModel):
    can_contain_liquid: bool = ...
    on_liquid_touches: LiquidTouchBehavior = ...
    stops_liquid_flowing_from_direction: list[DirectionAll] = ...
    liquid_type: str = ...

    def add(self, direction: DirectionAll) -> "ItemDetectionRule": ...

class BlockLiquidDetectionComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_liquid_detection)
    """

    detection_rules: list[ItemDetectionRule] = ...

    def add(
        self, detection_rule: ItemDetectionRule
    ) -> "BlockLiquidDetectionComponent": ...
