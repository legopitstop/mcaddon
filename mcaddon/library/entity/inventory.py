__all__ = ["EntityInventoryComponent"]

from enum import Enum
from typing import ClassVar
from .component import EntityComponent


class ContainerType(Enum):
    HORSE = "horse"
    MINECART_CHEST = "minecart_chest"
    CHEST_BOAT = "chest_boat"
    MINECART_HOPPER = "minecart_hopper"
    INVENTORY = "inventory"
    HOPPER = "hopper"
    NONE = "none"


@EntityComponent.register
class EntityInventoryComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_inventory)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:inventory"

    additional_slots_per_strength: int = 0
    can_be_siphoned_from: bool = False
    container_type: ContainerType = ContainerType.NONE
    inventory_size: int = 5
    private: bool = False
    restrict_to_owner: bool = False
