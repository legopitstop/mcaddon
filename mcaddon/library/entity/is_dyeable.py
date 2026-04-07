__all__ = ["EntityIsDyeableComponent"]

from typing import Optional, ClassVar
from .component import EntityComponent


@EntityComponent.register
class EntityIsDyeableComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_dyeable)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:is_dyeable"

    interact_text: Optional[str] = None
