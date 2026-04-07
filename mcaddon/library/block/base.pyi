from .component import BlockComponent
from .trait import BlockTrait
from mcaddon.core.base import BaseModel, ComponentSet
from mcaddon.core.file import ResourceFile
from mcaddon.library.common import BaseDescription, MenuCategory
from molang.dsl import MolangExpr
from typing import Any, List

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

__all__ = ["Block", "BlockDescription", "BlockComponentSet"]

class BlockProperty(BaseModel):
    type: str

class BlockDescription(BaseDescription):
    states: dict[str, BlockProperty | list[str | bool | int]] = ...
    traits: ComponentSet[BlockTrait] = ...
    menu_category: MenuCategory | None = ...

    @classmethod
    def model_traits(cls, obj): ...
    @classmethod
    def coerce_components(cls, obj): ...
    def add_state(
        self, name: str, property: BlockProperty | List[str | bool | int]
    ) -> Self: ...
    def add_trait(self, trait: BlockTrait) -> Self: ...

class BlockComponentSet(ComponentSet[BlockComponent]):
    @classmethod
    def validate(cls, value: Any) -> "BlockComponentSet": ...
    @classmethod
    def serialize(cls, value: Any) -> dict[str, Any]: ...

class BlockPermutation(BaseModel):
    condition: MolangExpr | bool
    components: BlockComponentSet = ...

    def add(self, component: BlockComponent) -> Self: ...

class Block(ResourceFile):
    """
    Defines a block
    """

    description: BlockDescription = ...
    components: BlockComponentSet = ...
    permutations: list[BlockPermutation] = ...
    @property
    def id(self) -> str: ...
    def get_tags(self) -> list[str]: ...
