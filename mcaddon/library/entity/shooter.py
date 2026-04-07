__all__ = ["EntityShooterComponent"]

from typing import Any, List, Optional, ClassVar
from pydantic import Field
from mcaddon.core.base import BaseModel
from mcaddon.library.filter import Filter
from .component import EntityComponent


class ShooterProjectile(BaseModel):
    def_: str = Field(alias="def")
    aux_val: int = -1
    filters: List[Filter] | Filter = Field(default_factory=list)
    lose_target: Optional[bool] = None
    chance: Optional[float] = None


@EntityComponent.register
class EntityShooterComponent(EntityComponent):
    """
    [Info](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_shooter)
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:shooter"

    aux_val: int = -1
    def_: str = Field(alias="def")
    magic: bool = False
    power: float = 0
    projectiles: List[ShooterProjectile] = Field(default_factory=list)
    sound: Optional[str] = None

    def model_dump(self, *args, **kw) -> dict[str, Any]:
        kw["by_alias"] = True
        return super().model_dump(*args, **kw)
