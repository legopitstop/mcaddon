from .component import BlockComponent
from mcaddon.library.constants import TintMethod

__all__ = ["DestructionParticlesComponent"]

class DestructionParticlesComponent(BlockComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destruction_particles)
    """

    particle_count: int
    texture: str
    tint_method: TintMethod
