__all__ = ["EntityPropertiesCondition"]

from typing import Dict
from pydantic import Field
from .base import LootCondition, BaseLootCondition


@LootCondition.register
class EntityPropertiesCondition(BaseLootCondition):
    TYPE_ID = "minecraft:entity_properties"
    condition: str = TYPE_ID

    entity: str
    properties: Dict[str, str | bool] = Field()
