__all__ = ["EmitterShapeDiscComponent"]

from typing import Tuple, Optional, ClassVar
from molang.dsl import MolangExpr
from mcaddon.library.constants import DiscPlane, DiscDirection
from .component import ParticleComponent


@ParticleComponent.register
class EmitterShapeDiscComponent(ParticleComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponents/minecraftemitter_disc)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:emitter_shape_disc"

    radius: float | MolangExpr
    direction: (
        Tuple[float | MolangExpr, float | MolangExpr, float | MolangExpr]
        | DiscDirection
    )
    offset: Optional[
        Tuple[float | MolangExpr, float | MolangExpr, float | MolangExpr]
    ] = None
    surface_only: Optional[bool] = None
    plane_normal: Optional[DiscPlane] = None
