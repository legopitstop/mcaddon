__all__ = ["EntityPropertiesCondition"]

from typing import Dict, ClassVar
from pydantic import Field

from .base import LootCondition, BaseLootCondition


@LootCondition.register
class EntityPropertiesCondition(BaseLootCondition):
    TYPE_ID: ClassVar[str] = "minecraft:entity_properties"
    condition: str = TYPE_ID

    entity: str
    properties: Dict[str, str | bool] = Field()
