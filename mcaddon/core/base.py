__all__ = [
    "BaseModel",
    "Version",
    "NumberRange",
    "ItemStack",
    "BlockState",
    "BaseComponent",
    "BlockLike",
    "ItemLike",
    "Number",
    "Identifier",
    "BlockTags",
    "ValueComponent",
    "NumberMinMax",
    "NumberMinMaxRange",
    "MolangColor",
    "ComponentSet",
    "Ingredient",
    "ItemResult",
    "TypedModel",
    "BaseTypedModel",
    "ItemTags",
    "CustomComponent",
    "Molang",
    "VersionedExpr",
]

from abc import ABC
from molang.dsl import MolangExpr
from typing import (
    Optional,
    Dict,
    ClassVar,
    Tuple,
    Any,
    Type,
    Generic,
    TypeVar,
    Set,
)
from pydantic import (
    BaseModel as _BaseModel,
    ConfigDict,
    Field,
)
from pydantic_core import core_schema

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from .utils import namespaced
from .types import Number


class BaseModel(_BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="forbid")


# TODO: [major, minor, patch] "major.minor.patch"
# class Version(BaseModel):
#     major: int
#     minor: int
#     patch: int

#     @classmethod
#     def parse(cls, value: Any) -> 'Version':
#         return Version(major=1, minor=0, patch=0)

Version = Tuple[int, int, int] | str

# TODO: "namespace:path"
# class Identifier(BaseModel):
#     namespace: str
#     path: str

#     @classmethod
#     def parse(cls, value:Any) -> 'Identifier':
#         return Identifier(namespace='minecraft', path='air')

Identifier = str


class ItemResult(BaseModel):
    item: str
    result_item: Optional[str] = None


# TODO: [min, max] {min: 0, max: 0}
class NumberMinMax(BaseModel):
    min: Optional[Number] = None
    max: Optional[Number] = None


# TODO: [range_min, range_max] {range_min: 0, range_max: 0}
class NumberMinMaxRange(BaseModel):
    range_min: Number
    range_max: Number


NumberRange = Tuple[Number, Number] | NumberMinMax | NumberMinMaxRange


class VersionedExpr(BaseModel):
    expression: MolangExpr
    version: int


Molang = MolangExpr | VersionedExpr


class MolangColor(BaseModel):
    r: MolangExpr | Number
    g: MolangExpr | Number
    b: MolangExpr | Number
    a: MolangExpr | Number


class ItemStack(BaseModel):
    item: str
    data: Optional[int] = None
    count: Optional[int] = None


class ItemTags(BaseModel):
    tags: MolangExpr


ItemLike = ItemStack | str | ItemTags


class Ingredient(BaseModel):
    item: Optional[str] = None
    tag: Optional[str] = None
    count: Optional[int] = None
    data: Optional[int] = None


class BlockState(BaseModel):
    name: str
    states: Optional[Dict[str, str | Number]] = Field(default_factory=dict)


class BlockTags(BaseModel):
    tags: MolangExpr


BlockLike = BlockState | BlockTags | str


class StatusEffect(BaseModel):
    id: int


class BaseComponent(BaseModel):
    """
    Common class for component like objects.
    """

    COMPONENT_ID: ClassVar[str] = "minecraft:unknown"
    format_version: ClassVar[Optional[str]] = None

    __all__: ClassVar[Dict[str, Type["BaseComponent"]]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__all__ = {}

    @classmethod
    def type_id(cls) -> str:
        return cls.COMPONENT_ID

    def __hash__(self) -> int:
        return hash(self.type_id())

    # TODO: Add option to "replace" already registered components.
    @classmethod
    def register(cls, clazz: type[Self]) -> type[Self]:
        def wrapper() -> type[Self]:
            if hasattr(cls, "__all__"):
                all = getattr(cls, "__all__")
                if clazz.type_id() in all:
                    msg = f"{cls.__name__} '{clazz.type_id()}' was already registered!"
                    raise Exception(msg)
                all[clazz.type_id()] = clazz
            return clazz

        return wrapper()


class CustomComponent(BaseComponent):
    model_config: ClassVar[ConfigDict] = ConfigDict(extra="allow")


class TypedModel(ABC, BaseModel):
    """
    Model instance for BaseTypedModel
    """

    TYPE_ID: ClassVar[str] = "unknown"
    type: str = TYPE_ID

    def __hash__(self) -> int:
        return hash(self.TYPE_ID)


class BaseTypedModel:
    """
    Common class for `{"type": "TYPE_ID", ...}` like objects
    """

    __all__: ClassVar[Dict[str, Type["TypedModel"]]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__all__ = {}

    @classmethod
    def register(cls, clazz: Type[TypedModel]) -> Type[TypedModel]:
        """
        Register a new modal type.
        """

        def wrapper() -> Type[TypedModel]:
            if hasattr(cls, "__all__"):
                all = getattr(cls, "__all__")
                if clazz.TYPE_ID in all:
                    msg = f"{cls.__name__} '{clazz.TYPE_ID}' was already registered!"
                    raise Exception(msg)
                all[clazz.TYPE_ID] = clazz
            return clazz

        return wrapper()

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler):
        choices = {}

        for id, c in cls.__all__.items():
            choices[namespaced(id)] = handler(c)
        union = core_schema.tagged_union_schema(
            choices=choices,
            discriminator="type",
        )

        return core_schema.chain_schema(
            [
                core_schema.no_info_plain_validator_function(
                    lambda e: namespaced(e, "type")
                ),
                union,
            ]
        )


class ValueComponent:
    """
    Helper class for simple value components
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, _source, handler):
        schema = handler(_source)
        return core_schema.no_info_wrap_validator_function(
            cls._wrap_parse,
            schema,
        )

    @classmethod
    def _wrap_parse(cls, v, handler):
        if not isinstance(v, dict):
            v = {"value": v}
        return handler(v)


T = TypeVar("T", bound=BaseComponent)


class ComponentSet(Generic[T]):
    """
    Class for a collection of BaseComponent's
    """

    __component_type__: Type[T]

    def __init__(self):
        self.__items = set([])

    def __iter__(self):
        return self.__items.__iter__()

    def __len__(self) -> int:
        return self.__items.__len__()

    def add(self, *elements: T) -> Self:
        self.__items.update(elements)
        return self

    def remove(self, element: T) -> Self:
        self.__items.remove(element)
        return self

    def clear(self) -> Self:
        self.__items.clear()
        return self

    def get(self, component_id: str) -> Optional[T]:
        id = namespaced(component_id)
        print(id)
        return None

    def __repr__(self) -> str:
        return str(self.__items)

    def __class_getitem__(cls, item):
        namespace = dict(cls.__dict__)
        namespace["__component_type__"] = item
        return type(
            f"{cls.__name__}[{getattr(item, '__name__', repr(item))}]",
            (cls,),
            namespace,
        )

    @classmethod
    # def validate(cls, value: Any) -> ComponentSet[T]:
    def validate(cls, value: Any) -> "ComponentSet[T]":
        if not isinstance(value, dict):
            raise TypeError("ComponentSet must be a dict")
        out: Set[BaseComponent] = set([])
        for id, data in value.items():
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
            out.add(component.model_validate(data))

        result = ComponentSet[T]()
        result.__items = out
        return result

    @classmethod
    def serialize(cls, value: Any) -> Dict[str, Any]:
        if not isinstance(value, (set, ComponentSet)):
            raise TypeError(f"value must be a set, but got '{type(value)}'")
        return {
            component.COMPONENT_ID: component.model_dump(exclude_none=True)
            for component in value
        }

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler):
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls.serialize
            ),
        )
