__all__ = ["EntityVariableMaxAutoStepComponent"]

from .component import EntityComponent
from typing import ClassVar


@EntityComponent.register
class EntityVariableMaxAutoStepComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_variable_max_auto_step)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:variable_max_auto_step"

    base_value: float = 0.5625
    controlled_value: float = 0.5625
    jump_prevented_value: float = 0.5625
