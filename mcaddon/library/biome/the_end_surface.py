__all__ = [
    "BiomeTheEndSurfaceComponent",
]

from typing import ClassVar
from .component import BiomeComponent
from deprecated import deprecated


@deprecated("This component is deprecated, use BiomeSurfaceBuilderComponent instead.")
@BiomeComponent.register
class BiomeTheEndSurfaceComponent(BiomeComponent):
    """
    Use minecraft:surface_builder in newer format versions.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:the_end_surface"
    format_version = "<1.20.60"
