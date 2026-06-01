__all__ = [
    "Block",
    "BlockDescription",
    "BlockComponentSet",
    "BlockProperty",
    "BlockPermutation",
]

from molang.dsl import MolangExpr
from typing import Any, ClassVar, Dict, Optional, List, cast
from pydantic import Field, ValidationError, field_validator

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from mcaddon.core.base import (
    BaseComponent,
    BaseModel,
    ComponentSet,
    CustomComponent,
    NumberMinMax,
)
from mcaddon.core.file import ResourceFile
from mcaddon.library.pack import behaviorpack
from mcaddon.library.common import BaseDescription, MenuCategory
from .component import BlockComponent
from .tag import BlockTagComponent
from .trait import BlockTrait


class BlockProperty(BaseModel):
    type: str = "set"
    values: NumberMinMax


class BlockDescription(BaseDescription):
    states: Dict[str, BlockProperty | List[str | bool | int]] = Field(
        default_factory=dict
    )
    traits: ComponentSet[BlockTrait] = Field(default_factory=ComponentSet)
    menu_category: Optional[MenuCategory] = None

    TRAIT_TYPE: ClassVar[type[BaseComponent]] = BlockTrait

    @classmethod
    def model_traits(cls, obj):
        traits = {}
        all = getattr(cls.TRAIT_TYPE, "__all__")

        for id, v in obj.items():
            trait = all.get(id)
            if trait is None:
                raise ValueError(f"Unknown {cls.TRAIT_TYPE.__name__} '{id}'")
            try:
                traits[id] = trait.model_validate(v)
            except ValidationError as err:
                print(id)
                raise err
        return traits

    @field_validator("traits", mode="before", check_fields=False)
    @classmethod
    def coerce_components(cls, obj):
        return cls.model_traits(obj)

    def add_state(
        self, name: str, property: BlockProperty | List[str | bool | int]
    ) -> Self:
        self.states[name] = property
        return self

    def add_trait(self, trait: BlockTrait) -> Self:
        self.traits.add(trait)
        return self


class BlockComponentSet(ComponentSet[BlockComponent]):

    @classmethod
    def validate(cls, value: Any) -> "BlockComponentSet":
        if not isinstance(value, dict):
            raise TypeError("ComponentSet must be a dict")
        # out: Set[BaseComponent] = set([])
        out = BlockComponentSet()
        for id, data in value.items():
            if id.startswith("tag:"):
                out.add(BlockTagComponent(tag=id.replace("tag:", ""), value=True))
                continue
            component = cls.__component_type__.__all__.get(id)
            if component is None:
                if id.startswith("minecraft:"):
                    raise TypeError(
                        f"{cls.__component_type__.__name__} '{id}' not found"
                    )
                else:
                    # Custom
                    component = CustomComponent
                    component.COMPONENT_ID = id

            out.add(cast(BlockComponent, component.model_validate(data)))
        return out

    @classmethod
    def serialize(cls, value: Any) -> Dict[str, Any]:
        if not isinstance(value, (set, ComponentSet)):
            raise TypeError(f"value must be a set, but got '{type(value)}'")
        result: Dict[str, Any] = {}
        for component in value:
            if isinstance(component, BlockTagComponent):
                result[f"tag:{component.tag}"] = {}
                continue
            result[component.type_id()] = component.model_dump(exclude_none=True)
        return result


class BlockPermutation(BaseModel):
    condition: MolangExpr | bool
    components: BlockComponentSet = Field(default_factory=BlockComponentSet)

    def add(self, component: BlockComponent) -> Self:
        self.components.add(component)
        return self


@behaviorpack("blocks")
class Block(ResourceFile):
    """
    Defines a block
    """

    TYPE_ID = "minecraft:block"

    description: BlockDescription = BlockDescription(identifier="minecraft:air")
    components: BlockComponentSet = Field(default_factory=BlockComponentSet)
    permutations: List[BlockPermutation] = Field(default_factory=list)

    @property
    def id(self) -> str:
        return self.description.identifier

    def get_tags(self) -> List[str]:
        return [x.tag for x in self.components if isinstance(x, BlockTagComponent)]
