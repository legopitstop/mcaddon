__all__ = [
    "DestructionParticlesComponent",
]

from .component import BlockComponent
from typing import ClassVar

from mcaddon.library.constants import TintMethod


@BlockComponent.register
class DestructionParticlesComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destruction_particles)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:destruction_particles"

    particle_count: int
    texture: str
    tint_method: TintMethod
