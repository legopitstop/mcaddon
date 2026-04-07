__all__ = ["EntityEntityArmorEquipmentSlotMappingComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityEntityArmorEquipmentSlotMappingComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_entity_armor_equipment_slot_mapping)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:entity_armor_equipment_slot_mapping"

    armor_slot: str
